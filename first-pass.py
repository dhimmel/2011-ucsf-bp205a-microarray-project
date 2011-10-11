#!/usr/bin/env python

from __future__ import division

import math
from microarray import DataSet

inputs = [
        'data/G/000.gpr', 'data/G/030.gpr',
        'data/G/060.gpr', 'data/G/180.gpr' ]

outputs = [
        'pickles/G/000.pkl', 'pickles/G/030.pkl',
        'pickles/G/060.pkl', 'pickles/G/180.pkl' ]

header = "{0.path} (R/G = {0.intensity_ratio})"
row = "{0.id:<15} {0.log_ratio}"

reference = DataSet.load(inputs[0])

for input, output in zip(inputs, outputs):
    data = DataSet.load(input)

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

    def irrational(feature):
        return math.isnan(feature.log_ratio)

    def too_extreme(feature):
        return abs(feature.log_ratio) > 15
    
    data.apply(correction)

    for feature, zero in zip(data, reference):
        feature.log_ratio -= zero.log_ratio

    data.prune(irrational)
    data.prune(too_extreme)

    data.save(output)
