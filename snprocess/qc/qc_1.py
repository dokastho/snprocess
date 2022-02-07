"""First step in data handling."""
# TODO update lines using where() so that names work

from os import mkdir
from os.path import join
import subprocess
import snprocess

def QC_1(inDir, outDir, inFile):
    """Handle data from /PRS/phase3/scripts/QC_1.sh."""
    """args vary by phase, make a driver file to manage this TODO"""
    mkdir(join(outDir))

    outFile = join(outDir, inFile)
    inFile = join(inDir, inFile)
    # read data into tuple
    # (bim, fam, bed) = read_plink(inFile, verbose=False)
    nextCommand = "plink --file ${inFile} --missing --out $outFile"
    snprocess.model.run_command(nextCommand)
    
    # TODO: hist miss

    # STEP 1: read data into a plink 1 binary file set

    # STEP 2: Remove individuals with high missingness

    # STEP 3: remove individuals with problematic sex

    # STEP 4: select autosomal SNPs only and remove low MAF

    # STEP 5: delete SNP's not in HWE
