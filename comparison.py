#!/usr/bin/env python

from __future__ import division

import sys, math

from pprint import pprint
from microarray import DataSet

# Data Files {{{1
target_inputs = [
        'pickles/G/000.pkl', 'pickles/G/030.pkl', 
        'pickles/G/060.pkl', 'pickles/G/180.pkl' ]

reference_inputs = [
        'pickles/A/000.pkl', 'pickles/A/030.pkl',
        'pickles/A/060.pkl', 'pickles/A/180.pkl',

        'pickles/A+B/000.pkl', 'pickles/A+B/030.pkl',
        'pickles/A+B/060.pkl', 'pickles/A+B/180.pkl',

        'pickles/A+D/000.pkl', 'pickles/A+D/030.pkl',
        'pickles/A+D/060.pkl', 'pickles/A+D/180.pkl',

        'pickles/A+E/000.pkl', 'pickles/A+E/030.pkl',
        'pickles/A+E/060.pkl', 'pickles/A+E/180.pkl',

        'pickles/A+F/000.pkl', 'pickles/A+F/030.pkl',
        'pickles/A+F/060.pkl', 'pickles/A+F/180.pkl',

        'pickles/B/000.pkl', 'pickles/B/030.pkl', 
        'pickles/B/060.pkl', 'pickles/B/180.pkl',

        'pickles/B+H/000.pkl', 'pickles/B+H/030.pkl', 
        'pickles/B+H/060.pkl', 'pickles/B+H/180.pkl',

        'pickles/D/000.pkl', 'pickles/D/030.pkl', 
        'pickles/D/060.pkl', 'pickles/D/180.pkl',

        'pickles/F/000.pkl', 'pickles/F/030.pkl', 
        'pickles/F/060.pkl', 'pickles/F/180.pkl' ]

output = 'pickles/ours={0},theirs={1}.pkl'

# }}}1

# Find Interesting Genes {{{1
def find_interesting_genes(inputs, threshold):

    print "  Restoring pickled data (%d)..." % len(inputs)
    experiment = [ DataSet.restore(input) for input in inputs ]
    uninteresting = lambda feature: abs(feature.normed_ratio) < threshold

    print "  Pruning uninteresting data (%d)..." % len(inputs)
    for timepoint in experiment:
        timepoint.prune(uninteresting)

    print "  Flattening all timepoints (%d)...\n" % len(inputs)
    target, others = experiment[0], experiment[1:]
    target.union(*others)

    return target

# Remove Common Genes {{{1
def remove_common_genes(target, *references):
    relevance = lambda feature: feature.normed_ratio

    target.difference(*references)
    target.sort(relevance)

    return target

# }}}1

target_threshold = 2
reference_threshold = 2

print "Searching for interesting genes in all data sets."
target = find_interesting_genes(target_inputs, target_threshold)
reference = find_interesting_genes(reference_inputs, reference_threshold)

print "Pruning genes that are not unique to the target."
target = remove_common_genes(target, reference)

print "Saving %d hits for further analysis." % len(target)
output = output.format(target_threshold, reference_threshold)
target.save(output)
