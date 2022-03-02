#!/garage/akil_lab/R-3.5.3/bin/Rscript

# needs the individual missing file (*.imiss)
# and the SNP missing file (*.rmiss) and the output directory
args <- commandArgs(trailingOnly = TRUE)

hwe <- read.table(file = args[1], header = FALSE, sep = "")
# hwe <- read.table(file = "plink.hwe", header = TRUE, sep = "")

pdf(paste0(args[3], "HWE_Histogram.pdf"))
hist(hwe[, 9], main = "Histogram HWE")
dev.off()

# hwe_zoom <- read.table(file = args[2], header = TRUE)
hwe_zoom <- read.table(file = "zoom.hwe", header = TRUE)

pdf(paste0(args[3], "HWE_below_theshold_Histogram.pdf"))
# pdf(paste0("foo", "HWE_below_theshold_Histogram.pdf"))
hist(hwe_zoom[,9], main = "Histogram HWE: strongly deviating SNPs only")
dev.off()