#!/usr/bin/env python
# vim: tw=0

import sys
from microarray import DataSet

try:
    stress, ours, theirs = sys.argv[1:]
except ValueError:
    print "Usage: display.py <stress> <ours> <theirs>"
    sys.exit()

input = 'pickles/{}/ours={},theirs={}.pkl'.format(stress, ours, theirs)
output = 'output/{}/ours={},theirs={}.txt'.format(stress, ours, theirs)

# Display a number of useful parameters:
#header = '{:<15}{:<15}{:<20}{:<20}{:<20}'.format("Gene_ID", "Gene_Name", "Expression_Level", "Signal_Quality", "Regression")
#template = '{0.id:<15}{0.name:<15}{0.normed_ratio:<20}{0.signal.red.signal_to_noise:<20}{0.regression_quality}'

# Produce only raw output (for use in database queries):
header = ""
template = '{0.name}'

data = DataSet.restore(input)
data.display(template, header, output)

print "Formatting %d genes." % len(data)
