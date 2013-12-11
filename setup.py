#!/usr/bin/env python

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
""".strip().splitlines()
VERSION ='0.1'

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name             = 'robotstatuschecker',
    version          = VERSION,
    author           = 'Robot Framework Developers',
    author_email     = 'robotframework@gmail.com',
    url              = 'http://robotframework.org',
    download_url     = 'https://pypi.python.org/pypi/robotstatuschecker',
    license          = 'Apache License 2.0',
    description      = 'A tool for checking that Robot Framework test cases '
                       'have expected statuses and log messages.',
    long_description = readme(),
    keywords         = 'robotframework testing testautomation atdd',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    py_modules       = ['robotstatuschecker']
)
