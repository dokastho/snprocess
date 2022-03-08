#!/garage/akil_lab/R-3.5.3/bin/Rscript

# needs the individual missing file (*.imiss) and the SNP missing file (*.rmiss) and the output directory
args <- commandArgs(trailingOnly = TRUE)
print(args)

indmiss <- read.table(file = args[1], header = TRUE)
snpmiss <- read.table(file = args[2], header = TRUE)
# read data into R

pdf(paste0(args[3], "Hist-individualMissingness.pdf")) # indicates pdf format and gives title to file
hist(indmiss[, 6], main = "Histogram individual missingness") # selects column 6, names header of file
dev.off()

pdf(paste0(args[3], "Hist-snpMissingness.pdf"))
hist(snpmiss[, 5], main = "Histogram SNP missingness")
dev.off() # shuts down the current device