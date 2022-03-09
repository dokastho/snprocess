"""Run all scripts on all phases"""
from snprocess.qc.qc_1 import QC_1
from snprocess.qc.qc_2 import QC_2
from snprocess.model import make_bed
import click
import json


@click.command()
@click.argument('phase', type=click.INT, default = 0)
@click.option('-v', '--verbose', type=click.BOOL, help='Log verbose output')
def main(phase, verbose):
    """
    Run all scripts on 'Phase' passed in as argument. Input 0 to run on all phases
    """

    # Phase 1 #################################
    if phase == 1 or phase == 0:
        settings = json.load(open("phase1.json"))
        QC_1(verbose, settings)
        # QC_2()

    # Phase 2 #################################
    elif phase == 2 or phase == 0:
        inDir = "../data/input/"
        outDir = "../data/qc/"
        inFile = "Reports"
        inFile = make_bed(inDir, inFile)
        QC_1(inDir, outDir, inFile, verbose)
        # QC_2()

    # Phase 3 #################################
    elif phase == 3 or phase == 0:
        inDir = "../data/input/"
        outDir = "../data/qc/"
        inFile = "Reports"
        inFile = make_bed(inDir, inFile)
        QC_1(inDir, outDir, inFile, verbose)
        # QC_2()


if __name__ == "__main__":
    main()
