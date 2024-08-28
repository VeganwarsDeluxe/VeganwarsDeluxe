# Configuration file for the Sphinx documentation builder.

# -- Project information
from VegansDeluxe.core import __version__

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = 'VeganwarsDeluxe'
copyright = '2024, VeganwarsDeluxe'
author = 'Vezono'

release = '1.4'
version = __version__

# -- General configuration

extensions = [
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

autoclass_content = "both"

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
