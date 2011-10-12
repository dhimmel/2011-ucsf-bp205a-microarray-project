# Daniel Himmelstein
str.num <- 10
str.name <- 'G'
alpha <- 0.10

setwd('/Users/dhimmels/Documents/ucsf/systems/excel/')
stressors.files <- c('A+B.tsv', 'A+D.tsv', 'A+E.tsv', 'A+F.tsv', 'A.tsv', 'B+H.tsv', 'B.tsv', 'D.tsv', 'F.tsv', 'G.tsv', 'control.1.tsv', 'control.2.tsv')
stressors <- c('ab', 'ad', 'ae', 'af', 'a', 'bh', 'b', 'd', 'f', 'g', 'c1', 'c2')
gpr.list <- lapply(stressors.files, function(x) read.delim(x, colClasses='character', na.strings='', col.names=c('name0', 'id0', 'G0', 'name1', 'id1', 'G30','name2', 'id2', 'G60','name3', 'id3', 'G180'), skip=1))
names(gpr.list) <- stressors

no.nas.ids <- lapply(gpr.list, function(x) as.character(na.omit(Reduce(intersect, list(x[, 2], x[, 5], x[, 8], x[, 11])))))
express <- lapply(1:12, function(x) cbind(
  as.numeric(gpr.list[[x]][match(no.nas.ids[[x]], gpr.list[[x]][, 2]), 3]),
  as.numeric(gpr.list[[x]][match(no.nas.ids[[x]], gpr.list[[x]][, 5]), 6]),
  as.numeric(gpr.list[[x]][match(no.nas.ids[[x]], gpr.list[[x]][, 8]), 9]),
  as.numeric(gpr.list[[x]][match(no.nas.ids[[x]], gpr.list[[x]][, 11]), 12])))

abses <- lapply(express, function(x) rowSums(abs(x)))

ids <- no.nas.ids[[str.num]]
non.str.ind <- (1:12)[-str.num]
abs.list <- list()
for (i in 1:length(ids)) {
  pos.in.ids <- sapply(no.nas.ids, function(x) which(x == ids[i]))
  abs.for.id <- sapply(non.str.ind, function(j) ifelse(length(pos.in.ids[[j]]) == 0, NA, abses[[j]][pos.in.ids[[j]]]))
  abs.for.id <- as.numeric(na.omit(abs.for.id))
  abs.list[[i]] <- abs.for.id
}

keep.gene <- sapply(abs.list, length) > 5
ids <- ids[keep.gene]
mu.abses <- abses[[str.num]][keep.gene]
abs.list <- abs.list[keep.gene]
p.unaj <- sapply(1:length(ids), function(i) t.test(abs.list[[i]], alternative='greater', mu=mu.abses[i])$p.val)
p.bonf <- p.unaj * length(p.unaj)
sig.ids <- ids[p.bonf < alpha]
write.table(sig.ids, paste('abs-spec-v-', str.name, '-bonf', alpha, '-list.txt', sep=''), quote=F, sep='\t', col.names=F, row.names=F)
eset <- cbind('ID'=ids, 'Name'=gpr.list[[str.num]][match(ids, gpr.list[[str.num]][, 2]), 1],
  express[[str.num]][keep.gene, ], 'pval'=p.unaj, 'bonf'=p.bonf)
colnames(eset)[3:6] <- c('t0', 't30', 't60', 't180')
write.table(eset, paste('abs-spec-v-', str.name, '-all.txt', sep=''), quote=F, sep='\t', col.names=F, row.names=F)





#######OLD
abs.list <- abs.list[keep.gene]
p.unaj <- sapply(1:length(ids), function(i) t.test(abs.list[[i]], alternative='greater', mu=exp.no.nas.win.exp.ids[[str.num]][i])$p.val)
p.bonf <- p.unaj * length(p.unaj)
sig.ids <- ids[p.bonf < alpha]
write.table(sig.ids, paste('abs-spec-v-', str.name, '-bonf', alpha, '-list.txt', sep=''), quote=F, sep='\t', col.names=F, row.names=F)
eset <- cbind('ID'=ids, 'Name'=gpr.list[[str.num]][match(ids, gpr.list[[str.num]][, 2]), 1],
  exp.no.nas.win.exp.ids[[str.num]], 'pval'=p.unaj, 'bonf'=p.bonf)


sig.eset <- eset[match(sig.ids, rownames(eset)), ]
write.table(sig.eset, 'signif-stan-dev-genes.20.txt', quote=F, sep='\t')



