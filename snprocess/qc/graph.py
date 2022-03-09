import os
import matplotlib as plt

def hist_miss(indmiss, snpmiss, outputDir):
    """
    indmiss: table
    snpmiss: table
    """
    ind = os.path(outputDir + "Hist-individualMissingness.pdf")
    snp = os.path(outputDir + "Hist-snpMissingness.pdf")

    p1 = plt.pyplot.hist(indmiss[6], label="Histogram individual missingness" )
    p2 = plt.pyplot.hist(snpmiss[5], label="Histogram SNP missingness" )

    plt.pyplot.savefig(ind, p1, format = "pdf")
    plt.pyplot.savefig(snp, p2, format = "pdf")
