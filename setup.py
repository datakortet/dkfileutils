#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""dkfileutils - file and directory utilities
"""
import sys

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries
"""

import setuptools
from distutils.core import setup, Command
from setuptools.command.test import test as TestCommand

version = '1.4.7'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='dkfileutils',
    version=version,
    author='Bjorn Pettersen',
    author_email='bp@datakortet.no',
    url='https://github.com/datakortet/dkfileutils/',
    requires=[],
    install_requires=[],
    description=__doc__.strip(),
    classifiers=[line for line in classifiers.split('\n') if line],
    long_description=open('README.rst').read(),
    cmdclass={'test': PyTest},
    packages=['dkfileutils'],
    zip_safe=False,
)
