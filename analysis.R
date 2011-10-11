setwd('/home/dhimmels/workspace/MicroarrayAnalysis/data/')
gpr.skip <- 31
g0 <- read.delim('G/000.gpr', skip=gpr.skip, colClasses='character')
g1 <- read.delim('G/030.gpr', skip=gpr.skip, colClasses='character')
g2 <- read.delim('G/060.gpr', skip=gpr.skip, colClasses='character')
g3 <- read.delim('G/180.gpr', skip=gpr.skip, colClasses='character')


filter.array <- function(l) {
# Pass function a list of the array gpr that need filtering
  keep.gene <- rowSums(sapply(l, function(x) x$Flag == 0 & x$Name != 'None')) == 4
  lapply(l, subset, keep.gene)
}

array.list <- list(g0, g1, g2, g3)
array.list <- filter.array(array.list)



find.lrm <- function(dataset) {
  # Function to find the log ratio of means for each gene from a gpr dataset
  lrm <- log2(as.numeric(dataset$Ratio.of.Medians..635.532.))
  lrm[dataset$Flag != 0] <- NA
  lrm[abs(lrm) > 10] <- NA
  lrm[is.nan(lrm)] <- NA
  return(lrm)
}

find.fc <- function(dataset) {
  # Function to find the log ratio of means for each gene from a gpr dataset
  fc <- as.numeric(dataset$Ratio.of.Medians..635.532.)
  fc[fc < 1] <- -1/fc[fc < 1]
  fc[dataset$Flag != 0] <- NA
  fc[abs(fc) > 1000] <- NA
  fc[is.nan(fc)] <- 
}


bonf.correct <- function(pvals) {
  # Function to adjust pvals via the bonferroni correction
  return(pvals * length(pvals))
}



exp.mat <- cbind(find.fc(g0), find.fc(g1), find.fc(g2), find.fc(g3))
rownames(exp.mat) <- g0$Name
exp.mat <- exp.mat[rownames(exp.mat) != 'None', ]
exp.mat <- exp.mat[rowSums(is.na(exp.mat)) == 0, ]
sum(exp.mat)

# T-test
t.pvals <- apply(exp.mat, 1, function(x) t.test(x)$p.value)
t.pvals.bonf <- bonf.correct(t.pvals)

# Linear Regression
time.points <- c(0, 30, 60, 180)
lm.pvals <- apply(exp.mat, 1, function(x) summary(lm(x~time.points))$coef[2, 4])
lm.pvals.bonf <- bonf.correct(lm.pvals)
