from qc.model import plink


def make_bed(inDir, inFile):
    """Convert SNP file to binary format. Return name of binary file."""
    inFileLink = inDir + inFile
    plink(" --file {} --make-bed --out {}merge".format(inFileLink, inDir))