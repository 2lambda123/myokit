#!/usr/bin/env python
#
# Runs the main unit tests Myokit, but skips OpenCL dependent tests.
#
# This file is part of Myokit
#  Copyright 2011-2018 Maastricht University, University of Oxford
#  Licensed under the GNU General Public License v3.0
#  See: http://myokit.org
#
import sys
import myotest
exclude = [
    'simulation_opencl.py',
    'simulation_opencl_log_interval.py',
]
result = myotest.run_all(exclude)
sys.exit(0 if result else 1)