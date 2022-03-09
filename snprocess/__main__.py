"""Run all scripts on all phases"""
from snprocess.qc.qc_1 import QC_1
from snprocess.qc.qc_2 import QC_2
from snprocess.model import make_bed
import click
import json
import os
import glob


@click.command()
@click.argument('phase', type=click.INT, default = 0)
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
        phases = phases[phase]

    for ph in phases:
        if 'Phase1' in ph:
            inDir = "input/"
        else:
            inDir = "data/input/"
            make_bed(ph + inDir, "Reports")
        inDir = ph + inDir

    # Phase 1 #################################
    if phase == 1 or phase == 0:
        p = QC_1(verbose, settings, 1)
        markup['phases'].append(p)
        # QC_2()

    # Phase 2 #################################
    if phase == 2 or phase == 0:
        make_bed(opts['fileroute'] + "Phase2/data/input/", "Reports")
        p = QC_1(verbose, settings, 2)
        markup['phases'].append(p)
        # QC_2()
    
    json.dump(markup, open("context.json", "w"), indent = 4)

if __name__ == "__main__":
    main()
