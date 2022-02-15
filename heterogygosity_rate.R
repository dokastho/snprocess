#!/garage/akil_lab/R-3.5.3/bin/Rscript

# Needs the pruned data and the output directory
args <- commandArgs(trailingOnly = TRUE)

het <- read.table(file = args[1], header = TRUE)

pdf(paste0(args[2], "heterozygosity.pdf"))

het$HET_RATE <- (het$"N.NM." - het$"O.HOM.") / het$"N.NM."

hist(het$HET_RATE, xlab="Heterozygosity Rate", ylab="Frequency", main= "Heterozygosity Rate")

dev.off()
