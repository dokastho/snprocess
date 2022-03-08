import os
import matplotlib

def hist_miss(indmiss, snpmiss, outputDir):
    """
    indmiss: table
    snpmiss: table
    """
    o = os.path(outputDir + "Hist-individualMissingness.pdf")
    