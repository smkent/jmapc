#!/usr/bin/env python3
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox

        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setup(
    name="jmapc",
    packages=find_packages(),
    install_requires=[
        "dataclasses-json",
        "python-dateutil",
        "requests",
        "setuptools-scm",
    ],
    entry_points=dict(console_scripts=[]),
    tests_require=["tox"],
    cmdclass=dict(test=Tox),
)
