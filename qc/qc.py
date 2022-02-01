"""First step in data handling"""

from os import mkdir
from os.path import join
from pandas_plink import read_plink, write_plink1_bin


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
    (bim, fam, bed) = read_plink(inFile, verbose=False)

