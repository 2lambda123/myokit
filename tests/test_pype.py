#!/usr/bin/env python
#
# Tests the parser
#
# This file is part of Myokit
#  Copyright 2011-2018 Maastricht University, University of Oxford
#  Licensed under the GNU General Public License v3.0
#  See: http://myokit.org
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals

import unittest

import myokit
import myokit.pype

from shared import TemporaryDirectory


class PypeTest(unittest.TestCase):

    def test_process_errors(self):
        """
        Tests error handling in the ``process`` method.
        """

        # Process method takes a dict
        e = myokit.pype.TemplateEngine()
        self.assertRaisesRegexp(
            ValueError, 'dict', e.process, 'file.txt', [])

        # Test not-a-file
        self.assertRaises(IOError, e.process, 'file.txt', {})

        # Test simple error
        self.e("""<?print(1/0) ?>""", {}, 'ZeroDivisionError')

        # Test closing without opening
        self.e("""Hello ?>""", {}, 'without opening tag')

        # Opening without closing is allowed
        self.e("""<?print('hi')""", {})

        # Nested opening
        self.e("""<?print('hi')<?print('hello')?>""", {}, 'Nested opening tag')

        # Too much inside <?=?>
        self.e("""<?=print('hi')?>""", {}, 'contain a single')

        # Triple quote should be allowed
        self.e('''Hello"""string"""yes''', {})

    def e(self, template, args, expected_error=None):
        """
        Runs a template, if an error is expected it checks if it's the right
        one, otherwise simply raises it.
        """
        with TemporaryDirectory() as d:
            path = d.path('template')
            with open(path, 'w') as f:
                f.write(template)
            e = myokit.pype.TemplateEngine()
            if expected_error is None:
                e.process(path, args)
            else:
                try:
                    e.process(path, args)
                except myokit.pype.PypeError:
                    # Check expected message in error details
                    self.assertIn(expected_error, e.error_details())
                    return
                raise RuntimeError('PypeError not raised.')


if __name__ == '__main__':
    unittest.main()