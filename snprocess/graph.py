from os.path import join
import matplotlib.pyplot as plt


def hist_miss(indmiss, snpmiss, outputDir):
    """
    indmiss: table
    snpmiss: table
    """
    ind = join(outputDir + "Hist-individualMissingness.pdf")
    snp = join(outputDir + "Hist-snpMissingness.pdf")

    indCol = indmiss.columns[5]
    snpCol = snpmiss.columns[4]

    plt.hist(indmiss[indCol])
    plt.title("Histogram individual missingness")
    plt.savefig(ind, format="pdf")
    plt.hist(snpmiss[snpCol])
    plt.title("Histogram SNP missingness")
    plt.savefig(snp, format="pdf")


def sexcheck(df, outputDir):
    gender = join(outputDir + "Gender_check.pdf")
    women = join(outputDir + "Women_check.pdf")
    men = join(outputDir + "Men_check.pdf")

    col = df.columns[5]

    plt.hist(df[col])
    plt.title("Gender")
    plt.xlabel("F")
    plt.savefig(gender)

    m = df[df['PEDSEX'] == 1]
    f = df[df['PEDSEX'] == 2]

    plt.hist(m[col])
    plt.title("Men")
    plt.xlabel("F")
    plt.savefig(men)

    plt.hist(f[col])
    plt.title("Women")
    plt.xlabel("F")
    plt.savefig(women)


def hwe(hwe_df, zoom, outputDir):
    fig = join(outputDir + "HWE_Histogram.pdf")

    col = hwe_df.columns[8]

    plt.hist(hwe_df[col], label = "Histogram HWE")