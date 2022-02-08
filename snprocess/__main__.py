"""Run all scripts on all phases"""
from snprocess.qc import qc_1,qc_2
import click


@click.command()
@click.argument('phase', type=click.INT)
@click.option('-v', '--verbose', type=click.BOOL, help='Log verbose output')
def main(phase, inDir, file, outDir, verbose):
    """
    Run all scripts on 'Phase' passed in as argument. Input 0 to run all phases
    """
    if phase == 1 or phase == 0:
        inDir="../input/"
        outDir="../qc/"
        inFile="merge"
        qc_1(inDir, outDir, inFile, verbose)
    elif phase == 2 or phase == 0:
        inDir="../data/input/"
        outDir="../data/qc/"
        inFile="Reports"
        qc_1(inDir, outDir, inFile, verbose)
    elif phase == 3 or phase == 0:
        inDir="../data/input/"
        outDir="../data/qc/"
        inFile="Reports"
        qc_1(inDir, outDir, inFile, verbose)


if __name__ == "__main__":
    main()
