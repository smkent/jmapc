#!/usr/bin/env python3
from setuptools import setup, find_packages
setup(
    name='jmapc',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jmapc = jmapc.main:main',
        ]
    },
)
