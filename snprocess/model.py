"""Shared methods for the snprocess package."""

import snprocess
import subprocess
import pandas as pd
from pathlib import Path
from os import remove
import glob


def isfloat(val):
    res = val.replace('.', '', 1).isdigit()
    return res


def run_command(cmd):
    """Run a bash command and handle errors."""
    # might want to use subprocess.run instead
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = process.communicate()
    if process.returncode != 0:
        exit("{}: Process exited with error".format(cmd))
    return output[0]


def make_bed(inDir, inFile):
    """Convert SNP file to binary format. Return name of binary file."""
    inFileLink = inDir + inFile
    run_command(
        "plink --bfile {} --make-bed --out {}".format(inFileLink, inFileLink + "_binary"))
    return inFile + "_binary"


def plink(cmd):
    """Run a plink command using run_command."""
    return run_command("./bin/plink" + cmd)


def read_from_output(output, key, sep=" "):
    """Return a dataframe from command output, rows and cols established using KEY"""
    output = output.split()
    output = [(lambda elt: elt.decode("utf-8"))(elt) for elt in output]
    rows = output.count(key)
    cols = int(len(output) / rows)
    output = [output[i:i + cols] for i in range(0, len(output), cols)]
    output = pd.DataFrame(output)
    for col in range(len(output)):
        if output[col][0].isnumeric():
            output[col] = output[col].astype("int")
        elif isfloat(output[col][0]):
            output[col] = output[col].astype("float")
    return output


def read_snp_data(outDir, filename, head=None):
    return pd.read_csv(delim_whitespace=True, filepath_or_buffer=outDir + filename, header=head)


def clean(outDir):
    leftovers = glob.glob(outDir + "plink.*")
    for item in leftovers:
        remove(item)
