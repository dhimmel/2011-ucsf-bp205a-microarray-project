#!/usr/bin/env python

from __future__ import division
from microarray import DataSet

inputs = [
        'data/A+D.000.gpr',
        'data/A+D.030.gpr',
        'data/A+D.060.gpr',
        'data/A+D.180.gpr' ]

for input in inputs:
    data = DataSet.load(input)
    print len(data)
