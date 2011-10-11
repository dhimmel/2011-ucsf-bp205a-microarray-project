#!/usr/bin/env python

from __future__ import division

import sys, math

from pprint import pprint
from microarray import DataSet

inputs = {
          "A" : [ 'pickles/A/000.pkl',
                  'pickles/A/030.pkl',
                  'pickles/A/060.pkl',
                  'pickles/A/180.pkl' ],

          "A+B" : [ 'pickles/A+B/000.pkl',
                  'pickles/A+B/030.pkl',
                  'pickles/A+B/060.pkl',
                  'pickles/A+B/180.pkl' ],

          "A+D" : [ 'pickles/A+D/000.pkl',
                  'pickles/A+D/030.pkl',
                  'pickles/A+D/060.pkl',
                  'pickles/A+D/180.pkl' ],

          "A+E" : [ 'pickles/A+E/000.pkl',
                  'pickles/A+E/030.pkl',
                  'pickles/A+E/060.pkl',
                  'pickles/A+E/180.pkl' ],

          "A+F" : [ 'pickles/A+F/000.pkl',
                  'pickles/A+F/030.pkl',
                  'pickles/A+F/060.pkl',
                  'pickles/A+F/180.pkl' ],

          "B" : [ 'pickles/B/000.pkl',
                  'pickles/B/030.pkl', 
                  'pickles/B/060.pkl',
                  'pickles/B/180.pkl' ],

          "B+H" : [ 'pickles/B+H/000.pkl',
                  'pickles/B+H/030.pkl', 
                  'pickles/B+H/060.pkl',
                  'pickles/B+H/180.pkl' ],

          "D" : [ 'pickles/B/000.pkl',
                  'pickles/B/030.pkl', 
                  'pickles/B/060.pkl',
                  'pickles/B/180.pkl' ],

          "F" : [ 'pickles/B/000.pkl',
                  'pickles/B/030.pkl', 
                  'pickles/B/060.pkl',
                  'pickles/B/180.pkl' ],

          "G" : [ 'pickles/G/000.pkl',
                  'pickles/G/030.pkl', 
                  'pickles/G/060.pkl',
                  'pickles/G/180.pkl' ] }

def restore_paths(paths):
    return [ DataSet.restore(path) for path in paths ]

def normed_ratio(feature):
    return feature.normed_ratio

experiments = {
        key : restore_paths(inputs[key])
        for key in inputs }

timepoints = experiments['G']
references = [
        experiment for experiment in experiments.values()
        if experiment is not timepoints ]

references = zip(*references)

sys.stderr.write("Pruning uninteresting data...\n")

# In each data set, find and remove genes with less than two-fold changes in
# expression.  
for experiment in experiments.values():

    if experiment is timepoints:
        uninteresting = lambda feature: abs(feature.normed_ratio) < 2
    else:
        uninteresting = lambda feature: abs(feature.normed_ratio) < 1

    for timepoint in experiment:
        timepoint.prune(uninteresting)

sys.stderr.write("Searching for differences...\n")

# Assume that any genes left the reference data sets are common stress
# responses.  Remove those from our data.
for timepoint, reference in zip(timepoints, references):
    timepoint.difference(*reference)
    timepoint.sort(normed_ratio)

header = "{0.path} (R/G = {0.intensity_ratio})"
feature = "{0.name:<15} {0.normed_ratio}"

DataSet.tabulate(header, feature, *timepoints)
