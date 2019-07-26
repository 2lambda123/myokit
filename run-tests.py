#!/usr/bin/env python3
#
# Runs all tests for Myokit.
#
# This file is part of Myokit
#  Copyright 2011-2019 Maastricht University, University of Oxford
#  Licensed under the GNU General Public License v3.0
#  See: http://myokit.org
#
# Parts of this test script are based on the test script for Pints
# See: https://github.com/pints-team/pints
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import gc
import os
import sys
import fnmatch
import argparse
import unittest
import traceback
import subprocess


def unit(args):
    """
    Runs unit tests, exits if anything fails.
    """
    print('Running tests with ' + sys.executable)

    suite = unittest.defaultTestLoader.discover(
        os.path.join('myokit', 'tests'), pattern='test*.py')
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if res.wasSuccessful() else 1)


def flake8():
    """
    Runs flake8 in a subprocess, exits if it doesn't finish.
    """
    print('Running flake8 ... ')
    sys.stdout.flush()
    p = subprocess.Popen(['flake8'], stderr=subprocess.PIPE)
    try:
        ret = p.wait()
    except KeyboardInterrupt:
        try:
            p.terminate()
        except OSError:
            pass
        p.wait()
        print('')
        sys.exit(1)
    if ret == 0:
        print('ok')
    else:
        print('FAILED')
        sys.exit(ret)


def doc_tests(args):
    """
    Checks if the documentation can be built, runs all doc tests, exits if
    anything fails.
    """
    print('Checking if docs can be built.')
    p = subprocess.Popen([
        'sphinx-build',
        '-b',
        'doctest',
        'docs/source',
        'docs/build/html',
        '-W',
    ])
    try:
        ret = p.wait()
    except KeyboardInterrupt:
        try:
            p.terminate()
        except OSError:
            pass
        p.wait()
        print('')
        sys.exit(1)
    if ret != 0:
        print('FAILED')
        sys.exit(ret)


def test_mmt_files(path):
    """
    Run all the `mmt` files in a given directory `path`, returns 0 iff nothing
    goes wrong.
    """
    import myokit

    # Get absolute path
    path = os.path.abspath(path)

    # Show what we're running
    print('Running mmt files for:')
    print('  ' + path)

    # Get current dir
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Error states
    error = 0

    # Change dir, make sure to change back again
    try:
        # Change to dir
        os.chdir(path)

        # Run all
        glob = '*.mmt'
        for fn in fnmatch.filter(os.listdir(path), glob):
            # Load and run
            try:
                print('Loading ' + fn)
                m, p, x = myokit.load(os.path.join(path, fn))
                try:
                    print('Running...')
                    myokit.run(m, p, x)
                except Exception:
                    error = 1
                    print(traceback.format_exc())
                del(m, p, x)
            except Exception:
                print('Unable to load.')
                print(traceback.format_exc())

            # Tidy up
            gc.collect()
            print('-' * 70)

            # Quit on error
            if error:
                return error
    finally:
        # Change back
        os.chdir(current_dir)

    # Return error status 0
    return error


def publication_examples(args):
    """
    Runs all publication examples, exits if one of them fails.
    """
    # Get publications directory
    path = os.path.join('myokit', 'tests', 'publications')

    # PBMB 2016. Myokit: A simple interface to cardiac cellular
    # electrophysiology
    if test_mmt_files(os.path.join(path, 'pbmb-2016')):
        sys.exit(1)


def web_examples(args):
    """
    Runs all web examples, exits if one of them fails.
    """
    # Get web directory
    path = os.path.join(
        'dev',
        'web',
        'html',
        'static',
        'download',
        'examples',
    )
    if not os.path.isdir(path):
        print('Web examples not found. Skipping.')
        return

    # Run, exit on error
    if test_mmt_files(path):
        sys.exit(1)


def full_suite(args):
    """
    Runs the full test suite, exits if anything fails.
    """
    # Set arguments for unit()
    flake8()
    doc_tests(args)
    unit(args)
    web_examples(args)
    publication_examples(args)


def minimal_suite(args):
    """
    Runs a minimal set of tests, exits if anything fails.
    """
    flake8()
    doc_tests(args)
    unit(args)


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description='Run unit tests for Myokit.',
        epilog='To run individual unit tests, use e.g.'
               ' $ tests/test_parser.py',
    )
    subparsers = parser.add_subparsers(help='commands')

    # Disable matplotlib output
    parser.add_argument(
        '--nompl',
        action='store_true',
        help='Disable matplotlib output.',
    )

    # Full test suite
    full_parser = subparsers.add_parser(
        'full', help='Run all tests (including graphical ones)')
    full_parser.set_defaults(func=full_suite)

    # Minimal test suite
    minimal_parser = subparsers.add_parser(
        'minimal', help='Run minimal checks (unit tests, flake8, docs)')
    minimal_parser.set_defaults(func=minimal_suite)

    # Unit tests
    unit_parser = subparsers.add_parser('unit', help='Run unit tests')
    unit_parser.set_defaults(func=unit)

    # Doctests
    doc_parser = subparsers.add_parser(
        'doc', help='Test if documentation can be built, and run doc tests.')
    doc_parser.set_defaults(func=doc_tests)

    # Publication examples
    pub_parser = subparsers.add_parser(
        'pub', help='Run publication examples.')
    pub_parser.set_defaults(func=publication_examples)

    # Web examples
    web_parser = subparsers.add_parser(
        'web', help='Run web examples.')
    web_parser.set_defaults(func=web_examples)

    # Parse!
    args = parser.parse_args()
    if args.nompl:
        print('Disabling matplotlib output')
        import matplotlib
        matplotlib.use('template')
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()