"""First step in data handling."""
# TODO update lines using where() so that names work

from os import mkdir
from os.path import join
from snprocess.model import plink, read_snp_data, clean
from snprocess.model import read_from_output as read
from snprocess.model import run_command as bash
import snprocess.graph as g
import pandas as pd
import json

def QC_1(verbose, opts):
    """
    Handle data from /PRS/phase3/scripts/QC_1.sh.
    inDir: input files directory, relative link
    outDir: input files directory, relative link
    inFile: format for input file
    """
    # args vary by phase, make a driver file to manage this TODO
    try:
        mkdir(join(outDir))
    except:
        pass
    with open("markup.json", 'w') as markup:
        inDir = opts['fileroute'] + opts['inDir']
        inFile = inDir + opts['inFile']
        # outDir = opts['fileroute'] + opts['outDir']
        outDir = opts['outDir']
        
        ####################################################
        # STEP 1: check missingness and generate plots
        plink(" --bfile {} --missing --out {}plink".format(inFile, outDir))

        imiss = read_snp_data(outDir, "plink.imiss", head=0)
        lmiss = read_snp_data(outDir, "plink.lmiss", head=0)
        g.hist_miss(imiss, lmiss, outDir)
        # bash("/usr/bin/Rscript --no-save hist_miss.R {}plink.imiss {}plink.lmiss {}".format(outDir,outDir,outDir))

        ####################################################
        # STEP 2: remove individuals with high missingness.. They recommend using a less stringent filter and then following it with a more stringent filter. Even the more stringent filter is more relaxed than Srijan's
        # Also, they filter on SNP missingness and indivudal missingness. Srijan first filters on individual missingness and then on SNPs much later

        # filter SNPs at 0.01
        plink(" --bfile {} --geno {} --make-bed --out {}plink".format(inFile, opts['geno'], outDir))

        # filter individuals at 0.05
        plink(" --bfile {}plink --mind {} --make-bed --out {}plink".format(outDir, opts['mind'], outDir))

        ####################################################
        # STEP 3: sexcheck
        plink(" --bfile {}plink --check-sex --out {}plink".format(outDir, outDir))

        # visualize the sex check
        sc = read_snp_data(outDir, "plink.sexcheck", head=0)
        g.sexcheck(sc, outDir)
        # bash("/usr/bin/Rscript --no-save {}sex_check.R {}plink.sexcheck {}".format(outDir, outDir, outDir))
        json.dump('{}sexcheck.pdf'.format(outDir), markup)

        # remove individuals with problematic sex
        # TODO add write to file
        output = bash('grep PROBLEM {}plink.sexcheck'.format(outDir))
        output = read(output,'PROBLEM')
        sd_df =  pd.DataFrame({0: output[0],1: output[1]})
        sd_df.to_csv(sep="\t",path_or_buf='{}sex_discrepency.txt'.format(outDir),index=False)

        # bash('awk \'{{print $1, $2}}\' awkout.txt > {}sex_discrepency.txt'.format(outDir))

        plink(" -bfile {}plink --remove {}sex_discrepency.txt --make-bed --out {}plink".format(outDir, outDir, outDir))

        # impute sex... (not sure why this is necessary). NOT RUNNING IT
        #plink -bfile ${outFile}_5 --impute-sex --make-bed --out ${outFile}_6

        ####################################################
        # STEP 4: select autosomal SNPs only an filter out SNPs with low minor allele frequency (MAF)

        # select autosomal SNPs only, ie from chr 1 to 22
        # bash("awk '{ if ($1 >= 1 && $1 <= 22) print $2 }' plink.bim > {}snp_1_22.txt".format(outDir))
        output = read_snp_data(outDir, "plink.bim")
        output = output[1][(output[0] >= 1) & (output[0] <= 22)]
        output.to_csv(sep="\t",path_or_buf='{}snp_1_22.txt'.format(outDir),index=False)

        # TODO question 1
        plink(" --bfile {}plink --extract {}snp_1_22.txt --make-bed --out {}plink".format(outDir, outDir, outDir))

        # generate plot of MAF distribution
        plink(" --bfile {}plink --freq --out {}MAF_check".format(outDir, outDir))

        #visualize it
        bash("/usr/bin/Rscript --no-save MAF_check.R {}MAF_check. {}".format(outDir, outDir))

        # remove SNPs with low MAF... major point of diversion. Srijan's MAF filtering crieria is VERY small. 0.005 vs what they recommend here of 0.05. I'll go midway with 0.01.
        # maf filter at 0.005
        plink(" --bfile {}plink --maf {} --make-bed --out {}plink".format(outDir, opts['maf'], outDir))

        ####################################################
        # STEP 5: Delete SNPs not in the Hardy-WEinberg equilibrium (HWE)

        plink(" --bfile {}plink --hardy --out {}plink".format(outDir, outDir))

        # select SNPs with HWE p-value below 0.00001
        # bash("awk '{ if ($9 < 0.0001) print $0 }' {}.hwe > {}zoomhwe.hwe".format(outFile, outDir))
        output = read_snp_data(outDir, "plink.hwe",head=0)
        output = output[output.columns[0]][(output[output.columns[8]] < .0001)]
        output.to_csv(sep="\t",path_or_buf='{}zoom.hwe'.format(outDir),index=False)
        # TODO
        # bash("/usr/bin/Rscript --no-save hwe.R plink.hwe {}zoom.hwe {}foo".format(outDir,outDir))

        # now delete them. We don'd have cae / controls, so filter all at 1e-10
        # this is again a departure from Yu's pipeline as they filter at 1e-6
        #plink --bfile ${outFile}_7 --hwe 1e-6 --make-bed --out ${outFile}_8
        plink(" --bfile {}plink --hwe 1e-10 --hwe-all --make-bed --out {}plink".format(outDir, outDir))

        ############################################################
        # STEP 6: Heterozygosity and LD Pruning

        # so first with heterzygosity rate. Remove individuals with a heterozygosity rate of more than 3 sd from the mean
        # heterozygosity: carrying two different alleles of a SNP. Low indicates inbreeding, high indicates low samples quality
        # exclude inversion regions (high LD regions).
        # Linkage Disequilibrium (LD) a measure of non-random association between alleles at different loci in the same chromosome.
        # SNPs are in LD when the frequency of association of their alleles is higher than expected under random assortment.
        # To calculate LD, we use the following parameters: window size=50, shift size=5, pairwise SNP-SNP r^2 metric=0.2
        # Yu's parameters are 100, 25, 0.5. Given the small sample sizes we are dealing with, Yu's parameters, particularly for r^2
        # make more sense. More SNPs would be excluded with r^2=0.2

        plink(" --bfile {}plink --indep-pairwise {} {} {} --out {}indepSNP".format(outDir, opts['indep_pairwise'][0], opts['indep_pairwise'][1], opts['indep_pairwise'][2], outDir))

        # get the pruned data set
        plink(" --bfile {}plink --extract {}indepSNP.prune.in --het --out {}R_hetCheck".format(outDir, outDir, outDir))

        # plot the heterogygosity rate
        # TODO
        # bash("/usr/bin/RScript --no-save heterogygosity_rate.R {}R_hetCheck {}".format(outDir, outDir))

        # list the individuals more than 3 sd away from the heterozygosity rate mean.
        # TODO
        # bash("/usr/bin/Rscript --no-save heterozygosity_outliers.R {}R_hetCheck {}".format(outDir, outDir))

        # need to exclude these individuals from the analysis.
        # TODO
        # bash('''sed 's/"// g' {}fail-het-qc.txt | awk '{print $1, $2}' > {}het-fail-ind.txt'''.format(outDir, outDir))

        # plink(" --bfile plink --remove {}het-fail-ind.txt --make-bed".format(outDir))

        ############################################################
        # STEP 7: Relatedness

        # This step isn't there in Yu's workflow, because it shouldn't really be necessary.
        # relatedness @0.2
        plink(" --bfile {}plink --extract {}indepSNP.prune.in --genome --min {} --out {}pihat_min0.2".format(outDir, outDir, opts['relatedness'], outDir))

        # visualize relations. But there will be none! or should be none!
        # bash("awk '{ if ($8 > 0.9) print $0}' {}pihat_min0.2.genome > {}zoom_pihat.genome".format(outDir, outDir))
        output = read_snp_data(outDir, "pihat_min0.2.genome", head=0)
        output = output[output.columns[0]][(output[output.columns[7]] > 0.9)]
        output.to_csv(sep="\t",path_or_buf='{}zoom_pihat.genome'.format(outDir),index=False)
        
        # TODO
        # bash("/usr/bin/Rscript --no-save relatedness.R {}pihat_min0.2.genome {}zoom_pihat.genome {}".format(outDir, outDir, outDir))

        # we shouldn't have any parent offspring relationships! but let's see if anything pops up
        # bash("awk '{ if ($8 > 0.9) print $0 }' {}pihat_min0.2.genome > {}zoom_pihat.genome".format(outDir, outDir))
        # output = pd.read_csv(delimiter="\t",filepath_or_buffer="{}pihat_min0.2.genome".format(outDir), header=None)
        # TODO duplicate lines?

        # visualize
        # bash("/usr/bin/Rscript --no-save relatedness.R {}pihat_min0.2.genome {}zoom_pihat.genome {}".format(outDir, outDir, outDir))


        #if there is anyone with a piHat more than 0.2, remove them!


        clean()

