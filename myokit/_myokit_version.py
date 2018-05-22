#
# Myokit's version info
#
# This file is part of Myokit
#  Copyright 2011-2018 Maastricht University, University of Oxford
#  Licensed under the GNU General Public License v3.0
#  See: http://myokit.org
#
import sys

# True if this is a release, False for a development version
RELEASE = False

# Version as a tuple (major, minor, revision)
#  - Changes to major are rare
#  - Changes to minor indicate new features, possible slight backwards
#    incompatibility
#  - Changes to revision indicate bugfixes, tiny new features
VERSION_INT = 1, 27, 0

# String version of the version number
VERSION = '.'.join([str(x) for x in VERSION_INT])
if not RELEASE:
    VERSION_INT += ('dev', )
    VERSION += '.dev'

# Don't expose x on Python2
if not sys.hexversion > 0x03000000:
    del(x)