"""Shared methods for the snprocess package."""

import snprocess
import subprocess

def run_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()