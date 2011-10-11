#!/usr/bin/env python

from microarray import DataSet

input = 'pickles/ours=2,theirs=2.pkl'
output = 'output/ours=2,theirs=2.txt'

# Display a number of useful parameters:
#header = "Gene_Name      Expression_Level    Signal_Quality"
#template = '{0.id:<15}{0.normed_ratio:<20}{0.signal.red.signal_to_noise}'

# Produce only raw output (for use in database queries):
header = ""
template = '{0.id}'

data = DataSet.restore(input)
data.display(template, header, output)
