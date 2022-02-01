"""First step in data handling"""
# TODO update lines using where() so that names work

from os import mkdir
from os.path import join
from pandas_plink import read_plink, read_plink1_bin, write_plink1_bin
from allel import heterozygosity_expected as he, heterozygosity_observed as ho, GenotypeArray

# import matplotlib


def QC_0():
    """Create fam file with sex metadata and add to ped."""
    # ported from /clubhouse/scripts/
    pedFile = "../data/report/Reports.ped"
    famFile = "../data/report/Reports.fam"
    tmp = "../data/report/tmp.ped"


def QC_1():
    """Handle data from /PRS/phase1/scripts/QC_1.sh."""
    inDir = "../input/"
    outDir = "../qc/"

    mkdir(join(outDir))

    inFile = "merge"

    outFile = join(outDir, inFile)
    inFile = join(inDir, inFile)
    # read data into tuple
    # (bim, fam, bed) = read_plink(inFile, verbose=False)

    # TODO: hist miss

    # STEP 1: read data into a plink 1 binary file set
    G = read_plink1_bin(join(inDir, inFile), verbose=False)

    # STEP 2: Remove individuals with high missingness
    G = G.where(G.geno >= .1, drop=True)  # TODO debug this line
    G = G.where(G.mind >= .05, drop=True)  # TODO debug this line

    # STEP 3: remove individuals with problematic sex
    G = G.where(G.sex <= 1, drop=True)  # TODO debug this line

    # STEP 4: select autosomal SNPs only and remove low MAF
    G = G.where(G.snp <= 22 & G.snp >= 1, drop=True)
    G = G.where(G.snp <= .01, drop=True)

    # STEP 5: delete SNP's not in HWE
    G['ho'] = ho(GenotypeArray(G.))
