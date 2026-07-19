# -- Project information

project = 'VeganwarsDeluxe'
copyright = '2024, VeganwarsDeluxe'
author = 'Vezono'

release = '1.7'
version = release

# -- General configuration

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
]

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
