#!/garage/akil_lab/R-3.5.3/bin/Rscript

# needs the individual missing file (*.imiss) and
# the SNP missing file (*.rmiss) and the output directory
args <- commandArgs(trailingOnly = TRUE)

data <- read.table(file = args[1], header = TRUE)
race <- read.table(file = args[2], header = TRUE)
datafile <- merge(data, race, by = c("IID", "FID"))
# head(datafile)

pdf(paste0(args[3], "MDS.pdf"))
plot.new()
for (i in 1:nrow(datafile)) {
    if (datafile[i, 14] == "EUR") {
        plot(datafile[i, 4], datafile[i, 5],
            type = "p",
            xlim = c(-0.1, 0.2), ylim = c(-0.15, 0.1),
            xlab = "MDS Component 1", ylab = "MDS Component 2",
            pch = 1, cex = 0.5, col = "green"
        )
    }
    par(new = T)
    if (datafile[i, 14] == "ASN") {
        plot(datafile[i, 4], datafile[i, 5],
            type = "p",
            xlim = c(-0.1, 0.2), ylim = c(-0.15, 0.1),
            xlab = "MDS Component 1", ylab = "MDS Component 2",
            pch = 1, cex = 0.5, col = "red"
        )
    }
    par(new = T)
    if (datafile[i, 14] == "AMR") {
        plot(datafile[i, 4], datafile[i, 5],
            type = "p",
            xlim = c(-0.1, 0.2), ylim = c(-0.15, 0.1),
            xlab = "MDS Component 1", ylab = "MDS Component 2",
            pch = 1, cex = 0.5, col = 470
        )
    }
    par(new = T)
    if (datafile[i, 14] == "AFR") {
        plot(datafile[i, 4], datafile[i, 5],
            type = "p",
            xlim = c(-0.1, 0.2), ylim = c(-0.15, 0.1),
            xlab = "MDS Component 1", ylab = "MDS Component 2",
            pch = 1, cex = 0.5, col = "blue"
        )
    }
    par(new = T)
    if (datafile[i, 14] == "OWN") {
        plot(datafile[i, 4], datafile[i, 5],
            type = "p",
            xlim = c(-0.1, 0.2), ylim = c(-0.15, 0.1),
            xlab = "MDS Component 1", ylab = "MDS Component 2",
            pch = 3, cex = 0.7, col = "black"
        )
    }
    par(new = T)
}

abline(v = -0.035, lty = 3)
abline(h = 0.035, lty = 3)
legend("topright",
    pch = c(1, 1, 1, 1, 3),
    c("EUR", "ASN", "AMR", "AFR", "OWN"),
    col = c("green", "red", 470, "blue", "black"),
    bty = "o", cex = 1
)