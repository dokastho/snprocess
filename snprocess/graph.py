import os
import matplotlib.pyplot as plt

def hist_miss(indmiss, snpmiss, outputDir):
    """
    indmiss: table
    snpmiss: table
    """
    ind = os.path.join(outputDir + "Hist-individualMissingness.pdf")
    snp = os.path.join(outputDir + "Hist-snpMissingness.pdf")

    indCol = indmiss.columns[5]
    snpCol = snpmiss.columns[4]

    plt.hist(indmiss[indCol], label="Histogram individual missingness" )
    plt.savefig(ind, format = "pdf")
    plt.hist(snpmiss[snpCol], label="Histogram SNP missingness" )
    plt.savefig(snp, format = "pdf")
