#!/usr/bin/env python
#
# LeanCheck for Python.  Core module.
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
"""
This is part of the [LeanCheck package](https://pypi.org/project/leancheck/):
an enumerative property-based testing library for Python.

This module defines leancheck's entry points such
as `leancheck.main()` and `leancheck.check()`.

You are better off importing the main `leancheck` module
with `import leancheck`.
"""


import inspect
import itertools
import sys
import types
import typing

import leancheck.misc as misc
import leancheck.iitertools as ii
import leancheck.gen as gen
import leancheck.ty as ty
from leancheck.enumerator import Enumerator


def check(prop, *types, max_tests=360, verbose=True, silent=False):
    """
    Checks a property for several enumerated argument values.
    Properties must have type hints
    in order for LeanCheck to be able to know
    which kinds of argument values to generate.

    >>> def prop_commute(x:int, y:int) -> bool:
    ...     return x + y == y + x
    >>> check(prop_commute)
    +++ OK, passed 360 tests: prop_commute
    True

    >>> def prop_increase(x:int, y:int) -> bool:
    ...     return x + y > x
    >>> check(prop_increase)
    *** Failed! Falsifiable after 1 tests:
        prop_increase(0, 0)
    False

    >>> def prop_sorted_twice(xs: list[int]) -> bool:
    ...     return sorted(sorted(xs)) == sorted(xs)
    ...
    >>> check(prop_sorted_twice)
    +++ OK, passed 360 tests: prop_sorted_twice
    True

    >>> def prop_sorted_len(xs: list[int]) -> bool:
    ...     return len(sorted(xs)) == len(xs)
    ...
    >>> check(prop_sorted_len)
    +++ OK, passed 360 tests: prop_sorted_len
    True

    >>> def prop_sorted_wrong(xs: list[int]) -> bool:
    ...     return sorted(xs) == xs
    ...
    >>> check(prop_sorted_wrong)
    *** Failed! Falsifiable after 7 tests:
        prop_sorted_wrong([1, 0])
    False

    >>> check(prop_sorted_twice, silent=True)
    True

    Lambdas do not allow type annotations,
    for them just pass types as further arguments.

    >>> check(lambda xs: sorted(sorted(xs)) == sorted(xs), list[int])
    +++ OK, passed 360 tests: <lambda>
    True
    """
    verbose = verbose and not silent
    clear, red, green, blue, yellow = misc.colour_escapes()
    if not types:
        if ty.return_type(prop) != bool and not silent:
            print(f"{yellow}Warning{clear}: property's return value is {ret} and not {bool}")
        types = ty.arg_types(prop)
    es = [Enumerator(t) for t in types]
    u = 0  # number of precondition fails
    for i, args in enumerate(itertools.islice(Enumerator.product(*es), max_tests)):
        # TODO: remove slight code duplication below...
        #       have a single "if not silent"
        try:
            if not prop(*args):
                if not silent:
                    repr_args = ", ".join(map(repr, args))
                    print(f"*** Failed! Falsifiable after {i+1} tests:")
                    print(f"    {red}{prop.__name__}{clear}({repr_args})")
                return False
        except PreconditionUnmatched as e:
            u += 1
            continue
        except BaseException as e:
            if not silent:
                repr_args = ", ".join(map(repr, args))
                print(f"*** Failed! Exception after {i+1} tests:")
                print(f"    {red}{prop.__name__}{clear}({repr_args})")
                print(f"    raised '{e}'")
            return False
    if verbose:
        i = i + 1
        exhausted = " (exhausted)" if i < max_tests else ""
        print(f"+++ OK, passed {i-u} tests{exhausted}: {green}{prop.__name__}{clear}")
    return True


def holds(prop, *types, max_tests=360):
    """
    Alias to `check(prop, silent=True)`.
    Returns a boolean indicating whether the given argument property holds
    for a (given) number of maximum tests.

    >>> def prop_commute(x:int, y:int) -> bool:
    ...     return x + y == y + x
    >>> holds(prop_commute)
    True

    >>> def prop_increase(x:int, y:int) -> bool:
    ...     return x + y > x
    >>> holds(prop_increase)
    False
    """
    return check(prop, *types, max_tests=max_tests, silent=True)


def main(max_tests=360, silent=False, verbose=False, exit_on_failure=True):
    """
    Tests all properties present in the current file,
    report results and
    exit with an error in case one of the properties fails.

    This is analogous to `unittest.main()`
    and is generally used at the end of a Python file as:

        if __name__ == '__main__':
            leancheck.main()
    """
    n_failures, n_properties = testmod(max_tests=max_tests, silent=silent, verbose=verbose)
    clear, red, green, blue, yellow = misc.colour_escapes()
    if not silent:
        if not n_properties:
            print(f"{yellow}Warning{clear}: no properties found")
        if n_failures:
            print(f"\n{red}*** {n_failures} of {n_properties} properties failed{clear}")
        elif verbose:
            print(f"{green}+++ {n_properties} properties passed{clear}")
    if n_failures and exit_on_failure:
        sys.exit(1)


def testmod(max_tests=360, silent=False, verbose=False):
    """
    Tests all properties present in the current file
    and report the results.

    This is analogous to `doctest.testmod()`
    and is generally used at the end of a Python file as:

        if __name__ == '__main__':
            n_failures, n_properties = leancheck.testmod()
            if n_failures:
                sys.exit(1)

    Depending on your use-case
    you may be better off calling `leancheck.main()` instead.
    """
    n_failures = 0
    n_properties = 0

    def lineno(m):
        try:
            return m[1].__code__.co_firstlineno
        except AttributeError:
            return -1

    for name, member in sorted(inspect.getmembers(sys.modules["__main__"]), key=lineno):
        if name.startswith("prop_") and callable(member):
            n_properties += 1
            passed = check(member, max_tests=max_tests, silent=silent, verbose=verbose)
            if not passed:
                n_failures += 1
    return (n_failures, n_properties)  # just like doctest.testmod()


def precondition(condition: bool):
    """
    Allows one to define a precondition for a property.

    >>> def prop_min(xs: list[int]) -> bool:
    ...     return sorted(xs)[0] == min(xs)
    >>> check(prop_min)
    *** Failed! Exception after 1 tests:
        prop_min([])
        raised 'list index out of range'
    False

    A correct version of the above property,
    requires that the given input list is non-empty.
    This can be specified in LeanCheck with the `precondition` directive.

    >>> def prop_min(xs: list[int]) -> bool:
    ...     precondition(len(xs) > 0)
    ...     return sorted(xs)[0] == min(xs)
    >>> check(prop_min)
    +++ OK, passed 359 tests: prop_min
    True

    Above, `precondition(xs)` would be equivalent.
    We use the verbose option for clarity.
    """
    if not condition:
        raise PreconditionUnmatched


class PreconditionUnmatched(ValueError):
    pass


# Runs tests if this is not being imported as a module.
if __name__ == "__main__":
    import doctest
    import sys

    (failures, _) = doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    if failures:
        sys.exit(1)
