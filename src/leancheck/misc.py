#!/usr/bin/env python
#
# LeanCheck for Python.  Misc module.
#
# (C) 2023-2026  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
"""
This is part of the [LeanCheck package](https://pypi.org/project/leancheck/):
an enumerative property-based testing library for Python.

This module defines miscellaneous utilities used throughout LeanCheck.


You are better off importing the main `leancheck` module
with `import leancheck`.
"""


import sys


# This is a simple colour_escapes function
# so that we don't impose additional dependencies on LeanCheck.
def colour_escapes():
    """
    Returns colour escape sequences for clear, red, green, blue and yellow

    >>> clear, red, green, blue, yellow = colour_escapes()
    >>> print(f"{red}This is red{clear} and {blue}this is blue{clear}.")
    This is red and this is blue.
    """
    plats = ["linux"]  # TODO: add other supported platforms
    supported = sys.stdout.isatty() and sys.platform in plats
    if supported:
        return "\x1b[m", "\x1b[1;31m", "\x1b[32m", "\x1b[34m", "\x1b[33m"
    else:
        return "", "", "", "", ""


# Runs tests if this is not being imported as a module.
if __name__ == "__main__":
    import doctest
    import sys

    (failures, _) = doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    if failures:
        sys.exit(1)
