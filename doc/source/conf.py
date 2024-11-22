# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Finite State Machine Tools'
copyright = '2024, biface'
author = 'biface'
release = '0.0.1'
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('../../src'))

print(sys.path)

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx_rtd_theme',
    'sphinx.ext.mathjax'
]

templates_path = ['source/_templates']
exclude_patterns = []
autoclass_content = 'both'

todo_include_todos = True

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

mathjax_path = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
mathjax3_config = {'chtml': {'displayAlign': 'left', 'displayIndent': '2em'}}