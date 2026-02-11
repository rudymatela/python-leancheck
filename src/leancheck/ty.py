#!/usr/bin/env python
#
# LeanCheck for Python.  Utils for inspecting (function) types.
#
# (C) 2023-2026  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
"""
This is part of the [LeanCheck package](https://pypi.org/project/leancheck/):
an enumerative property-based testing library for Python.

This module defines utilities for inspecting (function) types.


You are better off importing the main `leancheck` module
with `import leancheck`.
"""

import inspect

def return_type(fun):
    """
    Returns the return type of the given function.

    >>> def negate(p: bool) -> bool:
    ...     return not bool
    >>> return_type(negate)
    <class 'bool'>
    """
    return inspect.signature(fun).return_annotation

def arg_types(fun):
    """
    Returns the argument types of the given function.

    >>> def add(x: int, y: int) -> int:
    ...     return x + y
    >>> arg_types(add)
    [<class 'int'>, <class 'int'>]
    """
    # TODO: This currently returns kwargs' types as well
    #       causing problems in some contexts.
    #       Make so that this only returns args.
    #       Have a separate function kwarg_types for these cases.
    return [par.annotation for par in inspect.signature(fun).parameters.values()]


# Runs tests if this is not being imported as a module.
if __name__ == "__main__":
    import doctest
    import sys

    (failures, _) = doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    if failures:
        sys.exit(1)
