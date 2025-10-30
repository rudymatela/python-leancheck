LeanCheck for Python
====================

This is a port of [Haskell's LeanCheck] to [Python].

LeanCheck is an enumerative property-based testing library.
It can be used to complement your unit tests.

This is a work in progress:
__this library is currently experimental.__.

The usual drill in unit testing involves making assertions
about specific input-output cases of functions, such as:

```py
assertEqual(sorted([4,2,1,3]), [1,2,3,4])
```

There are no arguments to the unit test.

In property-based testing (with LeanCheck)
one writes more general properties that should be true
for any assignment of arguments.

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

```py
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


Further reading
---------------

[LeanCheck for Haskell] is subject to a chapter in a [PhD Thesis (2017)].

As of 2024, [Python] already has a relatively popular property-based testing
library called [Hypothesis].  While writing this port of LeanCheck, I
intentionally didn't take a closer look at Hypothesis.  I want to see if I
would take an entirely different approach here by not getting biased of how
things were implemented there.  The (current) idea is mostly to stay as close
as I could to the Haskell version.  I will note the differences (and
similarities) here, once I am done with the LeanCheck prototype and after I
take a closer look at Hypothesis.  LeanCheck test generation is enumerative,
Hypothesis test generation is (likely) random.


[Haskell's LeanCheck]:   https://hackage.haskell.org/package/leancheck
[LeanCheck for Haskell]: https://hackage.haskell.org/package/leancheck
[Python]: https://www.python.org/
[Hypothesis]: https://pypi.org/project/hypothesis/
[TODO]: TODO.md
[PhD Thesis (2017)]: https://matela.com.br/thesis-rudy.pdf
