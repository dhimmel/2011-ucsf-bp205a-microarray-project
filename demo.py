#!/usr/bin/env python

from microarray import DataSet

input = '../data/control/control.000.gpr'
output = '../data/control/control.000.pkl'

def parameter(feature):
    return feature.log_ratio

data = DataSet.load(input)
#data = DataSet.restore(output)

data.sort(parameter)
data.save(output)

data.display("{0.name:<15}{1.log_ratio}")

