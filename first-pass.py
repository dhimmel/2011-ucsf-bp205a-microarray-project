#!/usr/bin/env python

from __future__ import division

import math
from microarray import DataSet

inputs = [
        '/Users/ucsf/ucsf/etal/Team-Kale-088.gpr',
        '/Users/ucsf/ucsf/etal/Team-Kale-089.gpr',
        '/Users/ucsf/ucsf/etal/Team-Kale-090.gpr',
        '/Users/ucsf/ucsf/etal/Team-Kale-010.gpr' ]

outputs = [
        '/Users/ucsf/ucsf/pickles/A+D.000.pkl',
        '/Users/ucsf/ucsf/pickles/A+D.030.pkl',
        '/Users/ucsf/ucsf/pickles/A+D.060.pkl',
        '/Users/ucsf/ucsf/pickles/A+D.180.pkl' ]

header = "{0.path} (R/G = {0.intensity_ratio})"
row = "{0.id:<15} {0.log_ratio}"

data0 = DataSet.load(inputs[0])

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
    
    def norm_zero(feature):
        feature.log_ratio_norm_zero = feature.log_ratio - data0.search(criterion = lambda a: a.position==feature.position)[0].log_ratio 
        return feature

    data.apply(correction)

    data.prune(irrational)
    data.prune(too_extreme)

    data.save(output)
