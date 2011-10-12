#!/usr/bin/env python
# vim: tw=0

import sys
from microarray import DataSet

condition = sys.argv[1]
timepoint = sys.argv[2]
name = sys.argv[3]

timepoints = '0', '30', '60', '180'
conditions = (
        'A', 'A+B', 'A+D', 'A+E', 'A+F',
        'B', 'B+H', 'D', 'F', 'G',
        'control.1', 'control.2' )

# Do some simple error-checking on the command line arguments.

if condition not in conditions:
    raise ValueError("Unrecognized condition '%s'." % condition)

if timepoint not in timepoints:
    raise ValueError("Unrecognized timepoint '%s'." % timepoint)

template = 'pickles/{}/{:0>3}.pkl'
input = template.format(condition, timepoint)

def by_name(feature):
    return name == feature.name

data = DataSet.restore(input)
data.retain(by_name)

header = '{:<15}{:<15}{:<20}'.format("Gene_Name", "Gene_ID", "Expression_Level")
row = '{0.name:<15}{0.id:<15}{0.normed_ratio:<20}'

data.display(row, header)
