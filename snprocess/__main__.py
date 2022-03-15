"""Run all scripts on all phases"""
import pathlib
from snprocess.qc.qc_1 import QC_1
from snprocess.qc.qc_2 import QC_2
from snprocess.model import make_bed, md
import click
import json
import pathlib
import glob

@click.command()
@click.argument('settings', type=click.File)
@click.option('-v', '--verbose', type=click.BOOL, help='Log verbose output')
def main(folder, verbose, settings):
    """
    Run all scripts on input supplied by json config file specified by settings
    """
    if settings is None:
        settings = "default.json"
    settings = json.load(open(settings))

    input = settings['fileroute'] + folder

    inputFile = input + settings['inFile']

    flist = glob.glob(inputFile)

    binary = True
    if len(flist) == 0:
        exit
    elif ".b" not in flist[0][-4]:
        binary = False
    
    if not binary:
        make_bed(input, inputFile)

    markup = QC_1(verbose, settings, input)

    json.dump(markup, open("context.json", "w"), indent=4)
    op = pathlib.Path(settings['outDir'])
    md(op/"report.html")


if __name__ == "__main__":
    main()
