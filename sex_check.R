#!/garage/akil_lab/R-3.5.3/bin/Rscript

# needs the individual missing file (*.imiss) and the SNP missing file (*.rmiss) and the output directory
args <- commandArgs(trailingOnly = TRUE)

gender <- read.table(args[1], header=TRUE, as.is=TRUE)

pdf(paste0(args[2], "Gender_check.pdf"))
hist(gender[,6],main="Gender", xlab="F")
dev.off()

pdf(paste0(args[2], "Men_check.pdf"))
male=subset(gender, gender$PEDSEX==1)
hist(male[,6],main="Men",xlab="F")
dev.off()

pdf(paste0(args[2], "Women_check.pdf"))
female=subset(gender, gender$PEDSEX==2)
hist(female[,6],main="Women",xlab="F")
dev.off()

