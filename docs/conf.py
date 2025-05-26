import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

from jmapc.__version__ import __version__


project = "jmapc"
author = "Stephen Kent"
copyright = f"{datetime.now().year}, {author}"

version = __version__
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {
    ".rst": None,
    ".md": "myst_parser",
}

master_doc = "index"

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "white",
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

html_static_path = ["_static"]

html_sidebars = {}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
}

todo_include_todos = True

autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

napoleon_google_docstring = True

napoleon_numpy_docstring = True

napoleon_include_private_with_doc = False

napoleon_include_special_with_doc = True
