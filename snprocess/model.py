import json
import jinja2
from snprocess.qc.model import plink
import glob
from os import remove


def make_bed(inDir, inFile):
    """Convert SNP file to binary format. Return name of binary file."""
    inFileLink = inDir + inFile
    plink(" --file {} --make-bed --out {}".format(inFileLink, inFileLink))


def md(output_path, context, path):
    # load the template environment
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path + "/templates"),
        autoescape=jinja2.select_autoescape(['html', 'xml']), )
    
    # get the template
    temp = template_env.get_template("report_template.html")
    
    # render the html report template
    output_path.write_text(temp.render(context))


def printdict(d : dict) -> str:
    """print a dict in a json-like format"""
    outstr = ""
    for item in d.keys():
        outstr += "\t" + item + ": " + str(d[item]) + "\n"
    return outstr

def clean(outDir):
    """Remove unnecesary files produced by QC."""
    leftovers = glob.glob(outDir + "plink.*")
    for item in leftovers:
        remove(item)
