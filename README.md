LeanCheck for Python
====================

This is a port of [Haskell's LeanCheck] to [Python].

LeanCheck is an enumerative property-based testing library.
It can be used to complement your unit tests.

This is a work in progress, this library barely works at the moment.
Once I go over the most pressing [TODO] items,
I will remove this notice and release it on PyPI.

Quick Example
-------------

```py
$ python -i leancheck.py

>>> from leancheck import *

>>> def prop_sorted_twice(xs: list[int]) -> bool:
...     return sorted(sorted(xs)) == sorted(xs)
...

>>> check(prop_sorted_twice)
Property passes!

>>> def prop_sorted_len(xs: list[int]) -> bool:
...     return len(sorted(xs)) == len(xs)
...

>>> check(prop_sorted_len)
Property passes!

>>> def prop_sorted_wrong(xs: list[int]) -> bool:
...     return sorted(xs) == xs
...

>>> check(prop_sorted_wrong)
Failed, falsifiable on ([1, 0],) after X tests
```


[Haskell's LeanCheck]: https://hackage.haskell.org/package/leancheck
[Python]: https://www.python.org/
[TODO]: TODO.md
