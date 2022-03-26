"""File for second qc method."""

from snprocess.qc.model import plink, read_snp_data, sort_duplicates
import pandas as pd
from pathlib import Path


def QC_2(opts, data):
    """Second and final step of QC.
    
    Impetus on results."""

    inDir = opts['fileroute'] + opts['inDir']
    # outDir = opts['fileroute'] + opts['outDir']
    outDir = opts['outDir']
    
    outFile = Path(opts["1kg_outfile"])

    if not Path.is_file(outFile):
        g1k = opts["1kg_plinkfile"]
        # Name missing SNPs
        _, data = plink("--bfile {} --set-missing-var-ids @:#[b37]\$1,\$2 --make-bed --out {}1kg_MDS".format(g1k, outDir,), data)
        # Filter variants
	    # Remove variants based on missing genotype data
        _, data = plink("--bfile {}1kg_MDS --geno 0.2 --allow-no-sex --make-bed --out {}1kg".format(outDir, outDir), data)
        # Remove individuals based on missing genotype data
        _, data = plink("--bfile {}1kg --mind 0.2 --allow-no-sex --make-bed --out {}1kg".format(outDir, outDir), data)
        # Remove variants again
        _, data = plink("--bfile {}1kg --geno 0.02 --allow-no-sex --make-bed --out {}1kg".format(outDir, outDir), data)
        # Remove geno again
        _, data = plink("--bfile {}1kg --mind 0.02 --allow-no-sex --make-bed --out {}1kg".format(outDir, outDir), data)
        # Remove based on MAF
        _, data = plink("--bfile {}1kg --maf 0.05 --allow-no-sex --make-bed --out {}1kg".format(outDir, outDir), data)
        # Filter on HWE
        _, data = plink("--bfile {}1kg --hwe 0.001 --allow-no-sex --make-bed --out {}1kg_MDS".format(outDir, outDir), data)

    print("Extracting variants from the data and from 1kg.")
    # extract variants present in our data and use them to extract variants in the 1K data
    
    # awk '{print $2}' ${qcOutFile}.bim > ${psDir}PopStrat_SNPs.txt
    output = read_snp_data(outDir, "plink.bim", head=0)
    output = output[output.columns[1]]
    output.to_csv(sep="\t", path_or_buf='{}PopStrat_SNPs.txt'.format(outDir), index=False)

    # plink --bfile ${plinkFile}_7 --extract ${psDir}PopStrat_SNPs.txt --make-bed --out ${psDir}1kg
    output, data = plink("--bfile {}1kg --extract {}PopStrat_SNPs.txt --make-bed --out {}1kg".format(outDir, outDir, outDir), data)

    # # extract variants presents in 1KG which are in our data
    # awk '{print $2}' ${psDir}1kg.bim > ${psDir}1kg_MDS_SNPs.txt
    output = read_snp_data(outDir, "1kg.bim", head=0)
    output = output[output.columns[1]]
    output.to_csv(sep="\t", path_or_buf='{}1kg_MDS_SNPs.txt'.format(outDir), index=False)

    # plink --bfile ${qcOutFile} --extract ${psDir}1kg_MDS_SNPs.txt --recode --make-bed --out ${psDir}PopStrat_MDS
    output, data = plink("--bfile plink --extract {}1kg_MDS_SNPs.txt --recode --make-bed --out {}PopStrat_MDS".format(outDir, outDir), data)

    # # the datasets have the same variants. Now make them have the same build
    # awk '{print $2,$4}' ${psDir}PopStrat_MDS.map > ${psDir}buildReport.txt
    output = read_snp_data(outDir, "PopStrat_MDS.map", head=0)
    output = output[[output.columns[1], output.columns[3]]]
    output.to_csv(sep="\t", path_or_buf='{}buildReport.txt'.format(outDir), index=False)
    # plink --bfile ${psDir}1kg --update-map ${psDir}buildReport.txt --make-bed --out ${psDir}1kg_1

    output, data = plink("--bfile {}1kg --update-map {}buildReport.txt --make-bed --out {}1kg".format(outDir, outDir, outDir), data)

    # # Now the code for merging the two data sets. Prior to merging, the steps are:
    # # 1. Make the genomes similar for all SNPs
    # # 2. Resolve strand issues
    # # 3. Remove SNPs which still differ between the two data sets

    # echo "Combining the data sets."
    # echo "Setting the reference genome"
    # # 1. Set reference genome
    # # The command will generate some warnings for impossible A1 allele assigments, but they now have the same reference genome for all SNPs
    # awk '{print $2, $5}' ${plinkFile}_1.bim > ${psDir}1kg_ref-list.txt
    output = read_snp_data(outDir, "1kg.bim", head=0)
    output = output[[output.columns[1], output.columns[4]]]
    output.to_csv(sep="\t", path_or_buf='{}1kg_ref-list.txt'.format(outDir), index=False)

    # plink --bfile ${psDir}PopStrat_MDS --reference-allele ${psDir}1kg_ref-list.txt --make-bed --out ${psDir}PopStrat-adj
    output, data = plink("--bfile {}PopStrat_MDS --reference-allele {}1kg_ref-list.txt --make-bed --out {}PopStrat-adj".format(outDir, outDir, outDir), data)

    # echo "Resolving strand issues"
    # # 2. Resolve Strand issues
    # # get the differences in the files
    # awk '{ print $2, $5, $6 }' ${plinkFile}_1.bim > ${psDir}1kg1_tmp
    output = read_snp_data(outDir, "1kg.bim", head=0)
    output = output[[output.columns[1], output.columns[4], output.columns[5]]]
    output.to_csv(sep="\t", path_or_buf='{}1kg1_tmp'.format(outDir), index=False)
    output = read_snp_data(outDir, "1kg1_tmp", head=0)
    cols = [output.columns[i] for i in [1, 4, 5]]
    output = output[cols]
    output.to_csv(sep="\t", path_or_buf='{}1kg1_tmp_nocols'.format(outDir), index=False)
    # awk '{ print $2, $5, $6 }' ${psDir}PopStrat-adj.bim > ${psDir}PopStrat-adj_tmp
    output = read_snp_data(outDir, "PopStrat-adj.bim", head=0)
    output = output[[output.columns[1], output.columns[4], output.columns[5]]]
    output.to_csv(sep="\t", path_or_buf='{}PopStrat-adj_tmp'.format(outDir), index=False)

    # sort ${psDir}1kg1_tmp ${psDir}PopStrat-adj_tmp | uniq -u > ${psDir}all_differences.txt # get uniquerows
    output = sort_duplicates(outDir, "PopStrat-adj_tmp", "1kg1_tmp_nocols")
    output.to_csv(sep="\t", path_or_buf='{}all_differences.txt'.format(outDir), index=False)

    # # Flip SNPs for resolving strand issues
    # awk '{ print $1 }' ${psDir}all_differences.txt | sort -u > ${psDir}flip_list.txt
    output = output[[output.columns[0]]]
    output = output.drop_duplicates()
    output.to_csv(sep="\t", path_or_buf='{}flip_list.txt'.format(outDir), index=False)
    # plink --bfile ${psDir}PopStrat-adj --flip ${psDir}flip_list.txt --reference-allele ${psDir}1kg_ref-list.txt --make-bed --out ${psDir}PopStrat_corrected
    output, data = plink("--bfile {}PopStrat-adj --flip {}flip_list.txt --reference-allele {}1kg_ref-list.txt --make-bed --out {}PopStrat_corrected".format(outDir, outDir, outDir, outDir), data)

    # # check for problematic SNPs after the flip
    # awk '{ print $2, $5, $6 }' ${psDir}PopStrat_corrected.bim > ${psDir}PopStrat_corrected_tmp
    output = read_snp_data(outDir, "PopStrat_corrected.bim", head=0)
    cols = [output.columns[i] for i in [1, 4, 5]]
    output = output[cols]
    output.to_csv(sep="\t", path_or_buf='{}PopStrat_corrected_tmp'.format(outDir), index=False)
    # sort ${psDir}1kg1_tmp ${psDir}PopStrat_corrected_tmp | uniq -u > ${psDir}uncorresponding_SNPs.txt
    output = sort_duplicates(outDir, "1kg1_tmp_nocols", "PopStrat_corrected_tmp")
    output.to_csv(sep="\t", path_or_buf='{}uncorresponding_SNPs.txt'.format(outDir), index=False)

    # # There aren't too many problematic SNPs left. Let's remove them
    # awk '{ print $1 }' ${psDir}uncorresponding_SNPs.txt | sort -u > ${psDir}SNPs_excluded.txt
    output = output[[output.columns[0]]]
    output = output.drop_duplicates()
    output.to_csv(sep="\t", path_or_buf='{}SNPs_excluded.txt'.format(outDir), index=False)
    # plink --bfile ${psDir}PopStrat_corrected --exclude ${psDir}SNPs_excluded.txt --make-bed --out ${psDir}PopStrat_MDS2
    output, data = plink("--bfile {}PopStrat_corrected --exclude {}SNPs_excluded.txt --make-bed --out {}PopStrat_MDS2".format(outDir, outDir, outDir), data)
    # plink --bfile ${psDir}1kg_1 --exclude ${psDir}SNPs_excluded.txt --make-bed --out ${psDir}1kg_2
    output, data = plink("--bfile {}1kg --exclude {}SNPs_excluded.txt --make-bed --out {}1kg".format(outDir, outDir, outDir), data)


    # # now merge them
    # plink --bfile ${psDir}PopStrat_MDS2 --bmerge ${psDir}1kg_2.bed ${psDir}1kg_2.bim ${psDir}1kg_2.fam --allow-no-sex --make-bed --out ${psDir}MDS_merge
    output, data = plink("--bfile {}PopStrat_MDS2 --bmerge {}1kg.bed {}1kg.bim {}1kg.fam --allow-no-sex --make-bed --out {}MDS_merge".format(outDir, outDir, outDir, outDir, outDir), data)

    # # Conduct MDS on pruned SNPs
    # plink --bfile ${psDir}MDS_merge --extract ${qcOutDir}indepSNP.prune.in --genome --out ${psDir}MDS_merge
    output, data = plink("--bfile {}MDS_merge --extract {}indepSNP.prune.in --genome --out {}MDS_merge".format(outDir, outDir,outDir), data)
    # plink --bfile ${psDir}MDS_merge --read-genome ${psDir}MDS_merge.genome --cluster --mds-plot 10 --out ${psDir}MDS_merge
    output, data = plink("--bfile {}MDS_merge --read-genome {}MDS_merge.genome --cluster --mds-plot 10 --out {}MDS_merge".format(outDir, outDir, outDir), data)

    # #### Plot it!

    # # Convert population codes into super-population codes (continents)
    # awk '{ print $1, $1, $2 }' ${panelFile} > ${psDir}race_1kg.txt
    # sed -i 's/JPT/ASN/g' ${psDir}race_1kg.txt
    # sed -i 's/ASW/AFR/g' ${psDir}race_1kg.txt
    # sed -i 's/CEU/EUR/g' ${psDir}race_1kg.txt
    # sed -i 's/CHB/ASN/g' ${psDir}race_1kg.txt
    # sed -i 's/CHD/ASN/g' ${psDir}race_1kg.txt
    # sed -i 's/YRI/AFR/g' ${psDir}race_1kg.txt
    # sed -i 's/LWK/AFR/g' ${psDir}race_1kg.txt
    # sed -i 's/TSI/EUR/g' ${psDir}race_1kg.txt
    # sed -i 's/MXL/AMR/g' ${psDir}race_1kg.txt
    # sed -i 's/GBR/EUR/g' ${psDir}race_1kg.txt
    # sed -i 's/FIN/EUR/g' ${psDir}race_1kg.txt
    # sed -i 's/CHS/ASN/g' ${psDir}race_1kg.txt
    # sed -i 's/PUR/AMR/g' ${psDir}race_1kg.txt

    # # create our own race file
    # awk '{ print $1, $2, "OWN" }' ${psDir}PopStrat_MDS.fam > ${psDir}raceFile.txt

    # # concatenate the race file
    # cat ${psDir}race_1kg.txt ${psDir}raceFile.txt | sed -e '1i\FID IID race' > ${psDir}raceFile2.txt

    # # generate plots
    # Rscript MDS_merge.R ${psDir}MDS_merge.mds ${psDir}raceFile2.txt ${psDir}

    return data