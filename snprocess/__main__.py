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
@click.argument('settings', type=click.STRING)
@click.option('-v', '--verbose', type=click.BOOL, help='Log verbose output')
def main(verbose, settings):
    """
    Run all scripts on input supplied by json config file specified by SETTINGS
    """

    try:
        settings = json.load(open(settings))
    except:
        exit("Settings JSON does not exist. Exiting.")

    input = settings['fileroute'] + settings['inDir']

    inputFile = input + settings['inFile']

    flist = glob.glob(inputFile + "*")

    binary = True
    if len(flist) == 0:
        exit
    else:
        for fl in flist:
            if fl[-3:] == "bim":
                binary = True
                break
            binary = False

    if not binary:
        make_bed(input, settings['inFile'])

    markup = QC_1(settings)
    markup = QC_2(settings, markup)

    markup["settings"] = {}

    for item, val in settings.items():
        markup["settings"][item] = val

    json.dump(markup, open("snprocess/context.json", "w"), indent=4)
    op = pathlib.Path(settings['outDir'])
    md(op/"report.html")

if __name__ == "__main__":
    main()
