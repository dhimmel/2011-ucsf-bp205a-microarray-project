#!/usr/bin/env python

from microarray import DataSet

input = '../data/control/control.000.gpr'
output = '../data/control.control.000.pkl'

def parameter(feature):
    return feature.log_ratio

data = DataSet.load(input)
data.sort(parameter)

for feature in data.features:
    print "{0:<15}{1}".format(feature.name, feature.log_ratio)

data.save(output)


