import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from django.conf import settings  # noqa isort:skip

settings.configure()

import drf_api_checker  # noqa isort:skip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "_ext")))
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {
    "django": ("http://django.readthedocs.org/en/latest/", None),
    "sphinx": ("http://sphinx.readthedocs.org/en/latest/", None),
}
extlinks = {
    "issue": ("https://github.com/saxix/drf-api-checker/issues/%s", "issue #"),
    "django_issue": ("https://code.djangoproject.com/ticket/%s", "issue #"),
}

github_project_url = "https://github.com/saxix/drf-api-checker"

todo_include_todos = True

templates_path = ["_templates"]

source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# HTML translator class for the builder
html_translator_class = "version.DjangoHTMLTranslator"

# General information about the project.
project = "DRF API Checker"
copyright = "2018-2019, Stefano Apostolico"  # noqa

# The short X.Y version.
version = ".".join(drf_api_checker.VERSION.split(".")[0:2])
release = drf_api_checker.VERSION
next_version = "0.8"

# List of patterns, relative to source directory, that match files and directories to
# ignore when looking for source files.
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# The theme to use for HTML and HTML Help pages.  See the documentation for a list of builtin themes.
html_theme = "default"

# Output file base name for HTML help builder.
htmlhelp_basename = "drf_api_checkerdoc"

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    (
        "index",
        "drf_api_checker.tex",
        "DRF API Checker Documentation",
        "Stefano Apostolico",
        "manual",
    ),
]

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        "index",
        "drf_api_checker",
        "DRF API Checker Documentation",
        ["Stefano Apostolico"],
        1,
    )
]
