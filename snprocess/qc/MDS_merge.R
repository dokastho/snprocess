library(data.table)
library(ggplot2)
library(ggthemes)

args <- commandArgs()[-1]
mds <- fread(args[5])
race <- fread(args[6])
fname <- args[7]
 
merged <- merge(mds, race[, c("IID", "race")], by = "IID")
 
ggplot(merged, aes(C1, C2, group = race)) +
  geom_point(aes(shape = race, color = race)) +
  geom_hline(yintercept = 0) +
  geom_vline(xintercept = 0) +
  theme_tufte()

ggsave(paste0(fname,"/MDS_merge.png"), width=3, height=3)