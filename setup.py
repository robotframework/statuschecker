#!/usr/bin/env python

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
""".strip().splitlines()

import sys

from distutils.core import setup
from os.path import abspath, dirname

sys.path.insert(0, dirname(abspath(__file__)))
from robotstatuschecker import __version__

setup(
    name             = 'robotstatuschecker',
    version          = __version__,
    author           = 'Robot Framework Developers',
    author_email     = 'robotframework@gmail.com',
    url              = 'http://robotframework.org',
    download_url     = 'https://pypi.python.org/pypi/robotstatuschecker',
    license          = 'Apache License 2.0',
    description      = 'A tool for checking that Robot Framework test cases '
                       'have expected statuses and log messages.',
    long_description = open('README.rst').read(),
    keywords         = 'robotframework testing testautomation atdd',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    py_modules       = ['robotstatuschecker']
)
