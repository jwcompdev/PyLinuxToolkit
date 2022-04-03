# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# import sphinx_bootstrap_theme

sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------

project = 'PyLinuxToolkit'
copyright = '2022, JWCompDev'
author = 'JWCompDev'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'myst_parser',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv', 'venv']


intersphinx_mapping = {
    "python": ("https://docs.python.org/3.9", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_title = "PyLinuxToolkit & PyStdLib Documentation"
html_last_updated_fmt = ""

html_theme_options = {
    "repository_url": "https://github.com/jwcompdev/PyLinuxToolkit",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "path_to_docs": "docs",
    "extra_navbar": "<p>By JWCompDev<br />© Copyright 2022.</p>",
    "home_page_in_toc": False,
    "toc_title": "Contents",  # Default: Contents
    "show_toc_level": 1,
}

html_sidebars = {
    "**": ["sidebar-logo.html", "search-field.html", "",
           "sbt-sidebar-nav.html", "sbt-sidebar-footer.html"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# -- Options for todo_ extension ----------------------------------------------

# If true, `todo_` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

myst_title_to_header = False
myst_enable_extensions = []
