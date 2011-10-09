#!/usr/bin/env python

# This script provides a template for renaming a large number of files.  To use
# this script, edit the pattern variable to match the names of the files you
# want to rename.  Then edit the template and fields variable so that they
# produce the desired names when they're combined on the last line.

import os, sys
import re, glob

prefix = 'control'
pattern = r'TeamUSA-Control-([0-9]+)_?([RW][12])?\.([a-z]*)'

os.chdir('control')

for file in glob.glob('*'):
    file = os.path.basename(file)
    match = re.match(pattern, file)

    timepoint, label, extension = match.groups()

    if label:
        template = "control.{0:0>3}.{1}.{2}"
        fields = timepoint, label, extension

    else:
        template = "control.{0:0>3}.{1}"
        fields = timepoint, extension

    os.rename(file, template.format(*fields))


