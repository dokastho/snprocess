"""Shared methods for the snprocess package."""

import snprocess
import subprocess
import pandas as pd

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
    run_command("plink --bfile {} --make-bed --out {}".format(inFileLink,inFileLink + "_binary"))
    return inFile + "_binary"

def plink(cmd):
    """Run a plink command using run_command."""
    return run_command("./bin/plink" + cmd)

def read_from_output(output, key):
    """Return a dataframe from command output, rows and cols established using KEY"""
    output = output.split()
    rows = output.count(key)
    cols = int(len(output) / rows)
    output = [output[i:i + cols] for i in range(0, len(output), cols)]
    output = pd.DataFrame(output)
    return output