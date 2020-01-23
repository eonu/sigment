#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages

VERSION = '0.1.0.alpha1'

setup(
    name = 'sigment',
    version = VERSION,
    author = 'Edwin Onuonga',
    author_email = 'ed@eonu.net',
    description = 'An extensible data augmentation package for creating ' \
        'complex transformation pipelines to apply to audio signals.'
    long_description = 'test',
    package_dir = {'': 'lib'},
    packages = find_packages(where='lib'),
    python_requires='>=3.5,<3.8',
    install_requires = [
        'numpy>=1.17,<2',
        'soundfile>=0.10,<0.11',
        'librosa>=0.7,<0.8'
    ]
)