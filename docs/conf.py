# -*- coding: utf-8 -*-

# Configuration file for the Sphinx documentation builder.

# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import sys, os, subprocess

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
try:
    # Sigment is installed
    import sigment
except ImportError:
    # Sigment is run from its source checkout
    sys.path.insert(0, os.path.abspath('../lib'))
    import sigment

subprocess.call('pip install numpydoc sphinx_rtd_theme m2r', shell=True)

# -- Project information -----------------------------------------------------

project = 'sigment'
copyright = '2019-2021, Edwin Onuonga'
author = 'Edwin Onuonga'

# The full version, including alpha/beta/rc tags
release = sigment.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',
    'numpydoc',
    'm2r'
]

autodoc_member_order = 'bysource'
autosummary_generate = True
numpydoc_show_class_members = False

# Set master document
master_doc = 'index'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
# See the documentation for a list of builtin themes.
html_theme = 'sphinx_rtd_theme'