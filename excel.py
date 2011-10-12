#!/usr/bin/env python
# vim: tw=0

from microarray import DataSet

inputs = [
        'pickles/control.2/000.pkl', 'pickles/control.2/030.pkl', 
        'pickles/control.2/060.pkl', 'pickles/control.2/180.pkl' ] 

experiments = [
        DataSet.restore(input)
        for input in inputs ]

header = '{0.path}'
template = '{0.id}\t{0.normed_ratio}'

DataSet.tabulate(header, template, *experiments)

