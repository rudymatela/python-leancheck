LeanCheck for Python
====================

This is a port of [Haskell's LeanCheck] to [Python].

LeanCheck is an enumerative property-based testing library.
It can be used to complement your unit tests.

This is a work in progress, this library barely works at the moment.
Once I go over the most pressing [TODO] items,
I will remove this notice and release it on PyPI.

The usual drill in unit testing involves making assertions
about specific input-output cases of functions, such as:

```py
assertEqual(sorted([4,2,1,3]), [1,2,3,4])
```

There are no arguments to the unit test.

In property-based testing (with LeanCheck)
one writes more general properties that should be true
for a given set of arguments.

For example:
given __any__ list, sorting it twice is the same as sorting it once.
We can encode this as a function returning a boolean value:

```py
def prop_sorted_twice(xs: list[int]) -> bool:
    return sorted(sorted(xs)) == sorted(xs)
```

For whatever list we provide this function,
it should return `True`.
Now one can use LeanCheck to verify this automatically:

```
>>> check(prop_sorted_twice)
+++ OK, passed 360 tests: prop_sorted_twice
```

Quick Example
-------------

```py
$ python -i leancheck.py

>>> from leancheck import *

>>> def prop_sorted_twice(xs: list[int]) -> bool:
...     return sorted(sorted(xs)) == sorted(xs)
...

>>> check(prop_sorted_twice)
+++ OK, passed 360 tests: prop_sorted_twice

>>> def prop_sorted_len(xs: list[int]) -> bool:
...     return len(sorted(xs)) == len(xs)
...

>>> check(prop_sorted_len)
+++ OK, passed 360 tests: prop_sorted_len

>>> def prop_sorted_wrong(xs: list[int]) -> bool:
...     return sorted(xs) == xs
...

>>> check(prop_sorted_wrong)
*** Failed! Falsifiable after 6 tests:
	prop_sorted_wrong([1, 0])
```


[Haskell's LeanCheck]: https://hackage.haskell.org/package/leancheck
[Python]: https://www.python.org/
[TODO]: TODO.md
