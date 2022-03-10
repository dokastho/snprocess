"""Run all scripts on all phases"""
import pathlib
from snprocess.qc.qc_1 import QC_1
from snprocess.qc.qc_2 import QC_2
from snprocess.model import make_bed, md
import click
import json
import glob


@click.command()
@click.argument('phase', type=click.INT)
@click.option('-v', '--verbose', type=click.BOOL, help='Log verbose output')
@click.option('-s', '--settings', type=click.STRING, help='input json for custom settings')
def main(phase, verbose, settings):
    """
    Run all scripts on 'Phase' passed in as argument. Input 0 to run on all phases
    """

    markup = {
        "phases": []
    }

    if settings is None:
        settings = "default.json"
    settings = json.load(open(settings))

    phases = glob.glob(settings['fileroute'] + 'Phase*')

    if phase != 0:
        phases = [phases[phase - 1]]

    for i, ph in enumerate(phases):
        phase = i + 1
        ph += "/"
        if phase == 0:
            inDir = "input/"
        else:
            inDir = "data/input/"
            make_bed(ph + inDir, "Reports")
        inDir = ph + inDir

        p = QC_1(verbose, settings, phase, inDir)
        markup['phases'].append(p)
    
    json.dump(markup, open("context.json", "w"), indent = 4)
    op = pathlib.Path(settings['outDir'])
    md(op/"report.html")

if __name__ == "__main__":
    main()
