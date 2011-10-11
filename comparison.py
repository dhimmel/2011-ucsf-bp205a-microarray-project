#!/usr/bin/env python

from __future__ import division

import sys, math

from pprint import pprint
from microarray import DataSet

# Inputs {{{1
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

        'pickles/B/000.pkl', 'pickles/B/030.pkl', 
        'pickles/B/060.pkl', 'pickles/B/180.pkl',

        'pickles/B/000.pkl', 'pickles/B/030.pkl', 
        'pickles/B/060.pkl', 'pickles/B/180.pkl' ]

output = 'pickles/sorted.thresholds=1,2.pkl'

# }}}1

# Find Interesting Genes {{{1
def find_interesting_genes(inputs, threshold):
    experiment = [ DataSet.restore(input) for input in inputs ]
    uninteresting = lambda feature: abs(feature.normed_ratio) < threshold

    for timepoint, input in zip(experiment, inputs):
        sys.stderr.write('  Pruning from %s...\n' % input)
        sys.stderr.flush()

        timepoint.prune(uninteresting)

    sys.stderr.write('  Performing union...\n\n')
    sys.stderr.flush()

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

sys.stderr.write("Searching for interesting genes in all data sets...\n")
sys.stderr.flush()

target = find_interesting_genes(target_inputs, threshold=1)
reference = find_interesting_genes(reference_inputs, threshold=2)

sys.stderr.write("Pruning genes that are not unique to the target...\n")
sys.stderr.flush()

target = remove_common_genes(target, reference)

sys.stderr.write("Printing the results to stdout...\n")
sys.stderr.flush()

target.save(output)
target.display("{0.id}")
