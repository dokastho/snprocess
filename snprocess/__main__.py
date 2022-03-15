"""Run all scripts on all phases"""
import pathlib
from snprocess.qc.qc_1 import QC_1
from snprocess.qc.qc_2 import QC_2
from snprocess.model import make_bed, md
import click
import json
import glob


@click.command()
@click.argument('settings', type=click.File)
@click.option('-v', '--verbose', type=click.BOOL, help='Log verbose output')
def main(folder, verbose, settings):
    """
    Run all scripts on input supplied by json config file specified by settings
    """

    markup = {}

    if settings is None:
        settings = "default.json"
    settings = json.load(open(settings))

    input = glob.glob(settings['fileroute'] + folder)[0]

    inputFile = glob.glob(input + "*.bed")
    if len(inputFile) == 0:
        inputFile = glob.glob(input + "*.fam")

        if len(inputFile) == 0:
            exit("""Input directory missing SNP data.
            
                    Valid formats: bim/bed, fam""")

        inputFile = inputFile.lstrip(".bed")
        make_bed(input, inputFile)

    else:
        inputFile = inputFile[0]
        inputFile = inputFile.lstrip(".bed")

    p = QC_1(verbose, settings, input)
    markup['phases'].append(p)

    json.dump(markup, open("context.json", "w"), indent=4)
    op = pathlib.Path(settings['outDir'])
    md(op/"report.html")


if __name__ == "__main__":
    main()
