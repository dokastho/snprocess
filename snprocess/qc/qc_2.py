"""File for second qc method."""

from snprocess.qc.model import plink
import pandas as pd
from pathlib import Path


def QC_2(opts):
    """Second and final step of QC.
    
    Impetus on results."""

    data = {}
    
    outFile = opts["1kg_outfile"]
    
    if not Path.is_file(outFile):
        g1k = opts["1kg_plinkfile"]
        # Name missing SNPs
        _, data = plink("--bfile {} --set-missing-var-ids @:#[b37]\$1,\$2 --make-bed".format(g1k,), data)
        # Filter variants
	    # Remove variants based on missing genotype data
        _, data = plink("--bfile plink --geno 0.2 --allow-no-sex --make-bed", data)
        # Remove individuals based on missing genotype data
        _, data = plink("--bfile plink --mind 0.2 --allow-no-sex --make-bed", data)
        # Remove variants again
        _, data = plink("--bfile plink --geno 0.02 --allow-no-sex --make-bed", data)
        # Remove geno again
        _, data = plink("--bfile plink --mind 0.02 --allow-no-sex --make-bed", data)
        # Remove based on MAF
        _, data = plink("--bfile plink --maf 0.05 --allow-no-sex --make-bed", data)
        # Filter on HWE
        _, data = plink("--bfile plink--hwe 0.001 --allow-no-sex --make-bed", data)

    print("Extracting variants from the data and from 1kG.")
    # extract variants present in our data and use them to extract variants in the 1K data
    
    return data