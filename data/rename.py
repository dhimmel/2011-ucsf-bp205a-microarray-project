#!/usr/bin/env python

# This script provides a template for renaming a large number of files.  To use
# this script, edit the pattern variable to match the names of the files you
# want to rename.  Then edit the template and fields variable so that they
# produce the desired names when they're combined on the last line.

import os, sys
import re, glob

directory = sys.argv[1]
os.chdir(directory)

pattern = r'control.(\d+).txt'
template = '{0:0>3}.2.gpr'

for file in glob.glob('*'):
    file = os.path.basename(file)
    match = re.match(pattern, file)

    if match:
        timepoint = match.group(1)
        result = template.format(timepoint)

        print "mv {} {}".format(file, result)
        os.rename(file, result)
