#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages

VERSION = '0.1.0'

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name = 'sigment',
    version = VERSION,
    author = 'Edwin Onuonga',
    author_email = 'ed@eonu.net',
    description = 'An extensible data augmentation package for creating complex transformation pipelines for audio signals.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/eonu/sigment',
    project_urls = {
        'Documentation': 'https://sigment.readthedocs.io/en/latest',
        'Bug Tracker': 'https://github.com/eonu/sigment/issues',
        'Source Code': 'https://github.com/eonu/sigment'
    },
    license = 'MIT',
    package_dir = {'': 'lib'},
    packages = find_packages(where='lib'),
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Natural Language :: English'
    ],
    python_requires='>=3.6,<=3.8',
    install_requires = [
        'numpy>=1.17,<2',
        'soundfile>=0.10,<0.11',
        'librosa>=0.7,<0.8'
    ]
)