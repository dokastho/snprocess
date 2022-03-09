from os.path import join
import matplotlib.pyplot as plt
import pandas


def hist_miss(indmiss: pandas.DataFrame, snpmiss: pandas.DataFrame, outputDir):
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
    plt.clf()

    plt.hist(snpmiss[snpCol])
    plt.title("Histogram SNP missingness")
    plt.savefig(snp, format="pdf")
    plt.clf()


def sexcheck(df: pandas.DataFrame, outputDir):
    gender = join(outputDir + "Gender_check.pdf")
    women = join(outputDir + "Women_check.pdf")
    men = join(outputDir + "Men_check.pdf")

    col = df.columns[5]

    plt.hist(df[col])
    plt.title("Gender")
    plt.xlabel("F")
    plt.savefig(gender)
    plt.clf()

    m = df[df['PEDSEX'] == 1]
    f = df[df['PEDSEX'] == 2]

    plt.hist(m[col])
    plt.title("Men")
    plt.xlabel("F")
    plt.savefig(men)
    plt.clf()

    plt.hist(f[col])
    plt.title("Women")
    plt.xlabel("F")
    plt.savefig(women)
    plt.clf()


def maf_check(df: pandas.DataFrame, outputDir):
    fig = join(outputDir + "MAF_distribution.pdf")

    col = df.columns[4]

    plt.hist(df[col])
    plt.title("MAF distribution")
    plt.xlabel("MAF")
    plt.savefig(fig)
    plt.clf()


def hwe(hwe_df: pandas.DataFrame, zoom: pandas.DataFrame, outputDir):
    fig = join(outputDir + "HWE_Histogram.pdf")

    col = hwe_df.columns[8]

    plt.hist(hwe_df[col])
    plt.title("Histogram HWE")
    plt.savefig(fig)
    plt.clf()

    fig = join(outputDir + "HWE_below_theshold_Histogram.pdf")

    col = zoom.columns[8]

    plt.hist(zoom[col])
    plt.title("Histogram HWE: strongly deviating SNPs only")
    plt.savefig(fig)
    plt.clf()


def heterozygosity_rate(df: pandas.DataFrame,outputDir):
    fig = join(outputDir + "heterozygosity.pdf")

    df["HET_RATE"] = (df['N.NM.'] - df['O.HOM.']) / df['N.NM.']

    plt.hist(df['HET_RATE'])
    plt.xlabel("Heterozygosity Rate")
    plt.ylabel("Frequency")
    plt.title("Heterozygosity Rate")
    plt.savefig(fig)
    plt.clf()
