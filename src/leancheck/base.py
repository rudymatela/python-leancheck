#!/usr/bin/env python
#
# LeanCheck for Python.  Core module.
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
"""
This is a port of
[Haskell's LeanCheck][] to [Python][].

[Haskell's LeanCheck]: https://hackage.haskell.org/package/leancheck
[Python]: https://python.org

**WIP: This library is currently experimental.**
It works for simple properties,
but the selection of supported types is still limited.

LeanCheck is an enumerative property-based testing library.
It can be used to complement your unit tests.

The usual drill in unit testing involves making assertions
about specific input-output cases of functions, such as:

    assertEqual(sorted([4,2,1,3]), [1,2,3,4])

There are no arguments to the unit test.

In property-based testing (with LeanCheck)
one writes more general properties that should be true
for a given set of arguments.
Properties in this sense are
parameterized unit tests or
parameterized assertions.

For example:
given *any* list, sorting it twice is the same as sorting it once.
We can encode this as a function returning a boolean value:

    >>> def prop_sorted_twice(xs: list[int]) -> bool:
    ...     return sorted(sorted(xs)) == sorted(xs)

For whatever list we provide this function,
it should return `True`.
Now one can use LeanCheck to verify this automatically:

    >>> check(prop_sorted_twice)
    +++ OK, passed 360 tests: prop_sorted_twice
    True

LeanCheck automatically came up with 360 unique lists
to exercise the property.

When the property or function-under-test is incorrect
LeanCheck may find and report a counterexample:

    >>> def prop_sorted_wrong(xs: list[int]) -> bool:
    ...     return sorted(xs) == xs
    ...

    >>> check(prop_sorted_wrong)
    *** Failed! Falsifiable after 7 tests:
        prop_sorted_wrong([1, 0])
    False

We now know that an ill input is the list `[1, 0]`.
In this arbitrary example, the property is incorrect.
In cases where the property is indeed correct,
the counterexample indicates a bug.

If you have a collection of properties (`prop_*`) in a Python file,
just call `leancheck.main()` and all of them will be automatically tested.
In the case of a library, you can put everything under
an if-expression as you would do with `unittest.main()` or `doctest.testmod()`.

    if __name__ == '__main__':
        leancheck.main()
"""


import inspect
import itertools
import sys
import types
import typing

import leancheck.misc as misc
import leancheck.iitertools as ii
import leancheck.gen as gen
from leancheck.enumerator import Enumerator


def check(prop, max_tests=360, verbose=True, silent=False, types=[]):
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
    for them one can use the `types=` option
    to list argument types.

    >>> check(lambda xs: sorted(sorted(xs)) == sorted(xs), types=[list[int]])
    +++ OK, passed 360 tests: <lambda>
    True
    """
    verbose = verbose and not silent
    clear, red, green, blue, yellow = misc.colour_escapes()
    if not types:
        sig = inspect.signature(prop)
        # print(f"Property's signature: {sig}")
        ret = sig.return_annotation
        if ret != bool and not silent:
            print(f"{yellow}Warning{clear}: property's return value is {ret} and not {bool}")
        types = [par.annotation for par in sig.parameters.values()]
    es = [Enumerator[t] for t in types]
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
        print(f"+++ OK, passed {i} tests{exhausted}: {green}{prop.__name__}{clear}")
    return True


def holds(prop, max_tests=360, types=[]):
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
    return check(prop, max_tests=max_tests, silent=True, types=types)


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
