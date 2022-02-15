#!/garage/akil_lab/R-3.5.3/bin/Rscript

# Needs the pruned data and the output directory
args <- commandArgs(trailingOnly = TRUE)

het <- read.table(args[1], head=TRUE)
het$HET_RATE <- (het$"N.NM." - het$"O.HOM.") / het$"N.NM."
het_fail <- subset(het, (het$HET_RATE < mean(het$HET_RATE)-3*sd(het$HET_RATE)) | (het$HET_RATE > mean(het$HET_RATE)+3*sd(het$HET_RATE)));
het_fail$HET_DST = (het_fail$HET_RATE-mean(het$HET_RATE))/sd(het$HET_RATE);

write.table(het_fail, paste0(args[2], "fail-het-qc.txt"), row.names=FALSE)
