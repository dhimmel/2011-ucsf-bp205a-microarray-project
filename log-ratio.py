#!/usr/bin/env python

from __future__ import division

import math
from microarray import DataSet

pickles = [
        'pickles/A+D.000.pkl',
        'pickles/A+D.030.pkl',
        'pickles/A+D.060.pkl',
        'pickles/A+D.180.pkl' ]

def log_ratio(feature):
    return feature.log_ratio

def too_extreme(feature):
    return abs(feature.log_ratio) > 15

header = "{0.path} (R/G = {0.intensity_ratio})"
feature = "{0.id:<15} {0.log_ratio}"

timepoints = [
        DataSet.restore(path)
        for path in pickles ]

for timepoint in timepoints:
    timepoint.prune(too_extreme)
    timepoint.sort(log_ratio, reverse=True)
    timepoint.truncate(50)

DataSet.tabulate(header, feature, *timepoints)
