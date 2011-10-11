#!/usr/bin/env python

from __future__ import division

import sys, math
from microarray import DataSet

stressors = [
        'A', 'A+B', 'A+D', 'A+E', 'A+F',
        'B', 'B+H', 'D', 'F', 'G',
        'control.1', 'control.2' ]

# These data sets are screwed up for some reason: B+F, E

inputs = [
        'data/%s/000.gpr', 'data/%s/030.gpr',
        'data/%s/060.gpr', 'data/%s/180.gpr' ]

outputs = [
        'pickles/%s/000.pkl', 'pickles/%s/030.pkl',
        'pickles/%s/060.pkl', 'pickles/%s/180.pkl' ]

def make_pass(stressor):

    #print "Parsing data for '%s'...\n" % stressor

    experiments = [ DataSet.load(input % stressor) for input in inputs ]
    reference = experiments[0]

    for data in experiments:

        # Find the ratio between the amount of red and green fluorescence that was
        # detected.  This ratio is assumed to be one for most data analysis
        # purposes, so the raw data needs to be corrected.

        green, red = 0, 0
        for feature in data:
            red += feature.signal.red.intensity
            green += feature.signal.green.intensity

        data.intensity_ratio = red / green
        data.log_ratio = math.log(red / green, 2)

        def correction(feature):
            feature.log_ratio -= data.log_ratio
            return feature

        data.apply(correction)

    for data in experiments:

        for feature, zero in zip(data, reference):
            feature.normed_ratio = feature.log_ratio - zero.log_ratio

    for data in experiments:

        def irrational(feature):
            return math.isnan(feature.normed_ratio)

        def noisy(feature):
            return (feature.signal.red.signal_to_noise < 1) or     \
                   (feature.signal.green.signal_to_noise < 1)

        def unnamed(feature):
            return feature.name in ('None', 'EMPTY')

        # This filter was proposed by team JKRW.
        def inconsistent(feature):
            return feature.regression_quality < 0.5

        data.prune(irrational)
        data.prune(noisy)
        data.prune(unnamed)
        data.prune(inconsistent)

    for data, output in zip(experiments, outputs):
        print "Saving %d features for '%s'." % (len(data), stressor)
        data.save(output % stressor)

    print

if __name__ == '__main__':
    for stressor in stressors:
        make_pass(stressor)
