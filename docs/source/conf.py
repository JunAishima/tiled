#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# tiled documentation build configuration file, created by
# sphinx-quickstart on Thu Jun 28 12:35:56 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "matplotlib.sphinxext.plot_directive",
    "numpydoc",
    "sphinx_click",
    "sphinx_copybutton",
    "myst_parser",
]

# Configuration options for plot_directive. See:
# https://github.com/matplotlib/matplotlib/blob/f3ed922d935751e08494e5fb5311d3050a3b637b/lib/matplotlib/sphinxext/plot_directive.py#L81
plot_html_show_source_link = False
plot_html_show_formats = False

# Generate the API documentation when building
autosummary_generate = True
numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "tiled"
copyright = "2021, Bluesky Collaboration"
author = "Bluesky Collaboration"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
import tiled

# The short X.Y version.
version = tiled.__version__
# The full version, including alpha/beta/rc tags.
release = tiled.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext trees.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
import sphinx_rtd_theme

html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    "**": [
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "tiled"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "tiled.tex", "tiled Documentation", "Contributors", "manual")
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "tiled", "tiled Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "tiled",
        "tiled Documentation",
        author,
        "tiled",
        "Tile-based access to SciPy/PyData structures over the web in many formats",
        "Miscellaneous",
    )
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    # Numpy/Scipy sphinx objects.inv is broken:
    # https://github.com/scipy/scipy/issues/15545
    # "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    # "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "matplotlib": ("https://matplotlib.org", None),
}

import yaml


def generate_schema_documentation(header, schema, target):

    # header
    with open(header, "r") as f:
        header_md = f.readlines()
    header_md = header_md[1:]
    header_md = [ln.strip("\n") for ln in header_md]

    # schema
    with open(schema, "r") as f:
        data = yaml.safe_load(f)

    def parse_schema(d, md=[], depth=0, pre=""):
        """
        Generate markdown headers from a passed python dictionary created by
        parsing a schema.yaml file.
        """
        if "then" in d:
            d = d["then"]

        if "properties" in d:
            depth += 1
            # Create markdown headers for each schema level
            for key, val in d["properties"].items():
                md.append("(schema_%s)=" % (pre + key))
                md.append("#" * (depth + 1) + " " + pre + key)
                md.append("")
                if "description" in val:
                    for ln in val["description"].split("\n"):
                        md.append(ln)
                    md.append("")

                parse_schema(val, md, depth, pre + "{}.".format(key))
            depth -= 1

        if "items" in d:
            depth += 1
            # Create markdown headers for each schema level
            if "properties" in d["items"]:
                for key, val in d["items"]["properties"].items():
                    md.append("(schema_%s)=" % (pre + key))
                    md.append("#" * (depth + 1) + " " + pre[:-1] + "[item]." + key)
                    md.append("")
                    if "description" in val:
                        for ln in val["description"].split("\n"):
                            md.append(ln)
                        md.append("")

                parse_schema(val, md, depth, pre + "{}.".format(key))
            depth -= 1

        return md

    schema_md = parse_schema(data)

    # reference = header + schema
    reference_md = header_md + schema_md
    with open(target, "w") as f:
        f.write("\n".join(reference_md))


generate_schema_documentation(
    "reference/service-configuration-header.txt",
    "../../tiled/config_schemas/service_configuration.yml",
    "reference/service-configuration.md",
)
generate_schema_documentation(
    "reference/client-profiles-header.txt",
    "../../tiled/config_schemas/client_profiles.yml",
    "reference/client-profiles.md",
)

from tiled.adapters.mapping import MapAdapter
from tiled.authenticators import DummyAuthenticator
from tiled.server.app import build_app

app = build_app(MapAdapter({}), authentication={"authenticator": DummyAuthenticator()})
api = app.openapi()

with open("reference/api.yml", "w") as file:
    yaml.dump(api, file)
