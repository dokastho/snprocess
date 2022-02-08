"""Shared methods for the snprocess package."""

import snprocess
import subprocess

def run_command(cmd):
    """Run a bash command and handle errors."""
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error is not None:
        exit("{}: Process exited with error".format(cmd))
    return output

def make_bed(inDir, inFile):
    """Convert SNP file to binary format. Return name of binary file."""
    inFileLink = inDir + inFile
    run_command("plink --bfile {} --make-bed --out {}".format(inFileLink,inFileLink + "_binary"))
    return inFile + "_binary"