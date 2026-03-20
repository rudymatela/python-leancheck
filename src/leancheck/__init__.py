#!/usr/bin/env python
#
# LeanCheck for Python.  Init module.
#
# (C) 2023-2026  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
"""
LeanCheck is an enumerative property-based testing library.
It can be used to complement your unit tests.

## Introduction

The usual drill in unit testing involves making assertions
about specific input-output cases of functions, such as:

    assertEqual(sorted([4,2,1,3]), [1,2,3,4])

There are no arguments to the unit test.

In property-based testing (with LeanCheck)
one writes more general properties that should be true
for any assignment of arguments.
Properties in this sense are
parameterized unit tests or
parameterized assertions.

For example:
given **any** list, sorting it twice is the same as sorting it once.
We can encode this as a function returning a boolean value:

>>> def prop_sorted_twice(xs: list[int]) -> bool:
...     return sorted(sorted(xs)) == sorted(xs)

For whatever list we provide this function,
it should return `True`.
Now one can use LeanCheck to verify this automatically:

>>> from leancheck import *
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

[LeanCheck is available on PyPI][python-leancheck] and installable via:

    $ pip install leancheck

This is a port of [Haskell's LeanCheck][] to [Python][].

[python-leancheck]: https://pypi.org/project/leancheck/
[Haskell's LeanCheck]: https://hackage.haskell.org/package/leancheck
[Python]: https://python.org

Example: testing a sorting function
-----------------------------------

Consider the following (not-quite) `qsort` function:

```py
def qsort(lst):
    if lst == []:
        return []
    x, *etc = lst  # split into head and tail
    lesser  = [y for y in etc if y < x]
    greater = [y for y in etc if y > x]
    return qsort(lesser) + [x] + qsort(greater)
```

It returns the sorted version of the given argument list:

```py
> qsort([4,2,1,3])
[1,2,3,4]
```

We can define the following three properties about it:

1. Sorting a list returns the elements in order;
2. Sorting preserves membership in the list;
3. Sorting does not change the list length.

We can define and test these properties with LeanCheck as follows:

```py
import leancheck

def prop_sort_ordered(xs: list[int]) -> bool:
    ys = qsort(xs)
    return all(x <= y for x, y in zip(ys, ys[1:]))

def prop_sort_elem(x: int, xs: list[int]) -> bool:
    return (x in qsort(xs)) == (x in xs)

def prop_sort_len(xs: list[int]) -> bool:
    return len(qsort(xs)) == len(xs)

if __name__ == '__main__':
    leancheck.main(verbose=True)
```

We import LeanCheck, define the properties and call `leancheck.main()`
which will test all properties defined in the file:
anything named `prop_*`.
The properties may be placed together with the function(s) under test
or in a separate test file depending on your needs.

Note the type annotations, these are necessary for LeanCheck to know
how to test each property.

Running the above file/program/script yields the following report:

    +++ OK, passed 360 tests: prop_sort_ordered

    +++ OK, passed 360 tests: prop_sort_elem

    *** Failed! Falsifiable after 3 tests:
        prop_sort_len([0, 0])

We actually have a failure in the third property
and we can investigate:

    > leancheck.check(prop_sort_len)
    *** Failed! Falsifiable after 3 tests:
        prop_sort_len([0, 0])

    > prop_sort_len([0, 0])
    False

    > len(qsort([0, 0]))
    1

    > qsort([0, 0])
    [0]

Our function discards repeated elements!
Fixing the bug in `qsort` is left as an exercise to the reader.

An extended version of this example can be found
under the `examples/` folder in the source repository.


Example: custom class
---------------------

LeanCheck also works for tesing properties
over instances of custom or user-defined classes.
The following short example illustrates how to do this:

```py
import leancheck
from leancheck import Enumerator

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def distance(self, other):
        return (self.x - other.x)**2 + (self.y - other.y)**2

def prop_distance_positive(p: Point, q: Point) -> bool:
    return Point.distance(p,q) >= 0

def prop_self_distance(p: Point) -> bool:
    return Point.distance(p,p) == 0

if __name__ == '__main__':
    leancheck.main(verbose=True)
```

Then just run:

```sh
$ python point.py
+++ OK, passed 360 tests: prop_distance_positive
+++ OK, passed 360 tests: prop_self_distance
+++ 2 properties passed
```

The enumeration for `Point`s is inferred
from the type annotations in the constructor.
A point is a cross-product of two floats:

```py
> print(Enumerator(Point))
[Point(0.0, 0.0), Point(0.0, 1.0), Point(1.0, 0.0), Point(0.0, -1.0), Point(1.0, 1.0), Point(-1.0, 0.0), ...]
```

If the type-annotation was not present,
an enumerator could be registered for use with:

```py
Enumerator.register_cons(Point, float, float)
```

... anywhere between the `Point` class declaration
and the `leancheck.main` call.
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


# Runs tests if this is not being imported as a module.
if __name__ == "__main__":
    import doctest
    import sys

    (failures, _) = doctest.testmod(optionflags=doctest.FAIL_FAST)
    if failures:
        sys.exit(1)
