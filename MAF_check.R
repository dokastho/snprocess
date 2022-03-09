#!/garage/akil_lab/R-3.5.3/bin/Rscript

# needs the individual missing file (*.imiss) and
# the SNP missing file (*.rmiss) and the output directory
args <- commandArgs(trailingOnly = TRUE)

maf_freq <- read.table(paste0(args[1], "frq"), header = TRUE, as.is = TRUE)

pdf(paste0(args[2], "MAF_distribution.pdf"))
hist(maf_freq[, 5], main = "MAF distribution", xlab = "MAF")
dev.off()