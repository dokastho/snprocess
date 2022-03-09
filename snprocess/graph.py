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

def sexcheck(df, outputDir):
    gender = os.path.join(outputDir + "Gender_check.pdf")
    women = os.path.join(outputDir + "Women_check.pdf")
    men = os.path.join(outputDir + "Men_check.pdf")

    col = df.columns[5]

    plt.hist(df[col], label = "Gender")
    plt.xlabel("F")
    plt.savefig(gender)

    m = df[df['PEDSEX'] == 1]
    f = df[df['PEDSEX'] == 2]

    plt.hist(m[col], label = "Men")
    plt.xlabel("F")
    plt.savefig(men)

    plt.hist(f[col], label = "Women")
    plt.xlabel("F")
    plt.savefig(women)