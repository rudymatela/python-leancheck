#!/usr/bin/env python
#
# LeanCheck for Python.  Init module.
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

from leancheck.base import (
    check,
    holds,
    main,
    testmod,
    precondition,
    Enumerator,
)

# For pdoc
__all__ = [
    "check",
    "holds",
    "main",
    "testmod",
    "precondition",
    "Enumerator",
]
