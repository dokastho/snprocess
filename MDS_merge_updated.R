library(data.table)
library(ggplot2)
library(ggthemes)
 
mds <- fread("MDS_merge.mds")
race <- fread("raceFile2.txt")
 
merged <- merge(mds, race[, c("FID", "race")], by.x = "IID", by.y = "FID")
 
ggplot(merged, aes(C1, C2, group = race)) +
  geom_point(aes(shape = race, color = race)) +
  geom_hline(yintercept = 0) +
  geom_vline(xintercept = 0) +
  theme_tufte()
