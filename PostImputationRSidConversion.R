library(data.table)
library(SNPlocs.Hsapiens.dbSNP144.GRCh37)

#fn <- "../../ref/PGC_UKB_depression_genome-wide.txt"
fn <- "../ref/PGC_UKB_23andMe_depression_genome-wide_chrbp_nomhc.assoc"
maf <- "../imputedFiles/allRsqMaf.info"
outFile <- "../ref/imputedGwasRefFileV2.txt"

gwas <- fread(fn)
maf <- fread(maf)

# maf snpid includes letters. remove it, but dont' because the original files still have those ids
maf$SNP1 <- sub("(:[^:]+):.*", "\\1", maf$SNP)

# convert to upper, even tho its not necessary
gwas$A1 <- toupper(gwas$A1)
gwas$A2 <- toupper(gwas$A2)

snps <- SNPlocs.Hsapiens.dbSNP144.GRCh37
temp <- as.data.frame(snpsById(snps, gwas$MarkerName, ifnotfound="drop"))

temp <- temp[, c(1, 2, 4)]
temp <- as.data.table(temp)

setkey(gwas, MarkerName)
setkey(temp, RefSNP_id)

mergeRes <- temp[gwas, nomatch=0]

mergeRes$snp <- paste0(mergeRes$seqnames, ":", mergeRes$pos)

setkey(mergeRes, snp)
setkey(maf, SNP1)

finalRes <- maf[mergeRes]

colnames(finalRes)[4] <- "chr"
colnames(finalRes)[6] <- "rsID"

# save one without MAF and Rsq
#fwrite(finalRes[, c(1, 4:12)], file="data/ONR-newGrant/gwasResMerged.txt", sep="\t")
#fwrite(finalRes[, c(1, 4:12)], file="data/ONR-newGrant/gwasResMerged.txt", sep="\t")

# save it
fwrite(finalRes[complete.cases(finalRes),], file=outFile, sep="\t")
