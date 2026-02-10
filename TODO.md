TODO for leancheck.py
=====================

* avoid `__class_getitem__` abuse (see below)

* fix infinite loop in `print(Enumerator[set[bool]])`

* simplify code

* Add some built-in benchmarks.
  Performance is not so good currently.

* add carry-on flag

* package _all_ files like in Haskell's leancheck


## Avoid `__class_getitem__` abuse

Turns out using `__class__getitem__` for retrieving global enumerations
was not a good idea after all.
[See this](https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__).

"The purpose of `__class_getitem__()` is to allow runtime parameterization of
standard-library generic classes in order to more easily apply type hints to
these classes."

"Using `__class_getitem__()` on any class for purposes other than type
hinting is discouraged."

Its unpythonic, so I'll replace it soon enough...

### Idea.

If the one-and-only argument to the constructor is a type or `GenericAlias`,
we query an existing enumerator.

```py
>>> Enumerator(int)
Enumerator(lambda: (xs for xs in [[0], [1], [-1], [2], [-2], [3], ...]))

>>> Enumerator(bool)
Enumerator(lambda: (xs for xs in [[False, True]]))
```

If the first argument is a type, and the second is something else (see below),
we register an enumerator (and return it).

If the something else argument is a raw enumeration (function),
we create a raw enumeration.

Create a raw enumeration (function type as sole argument):

```py
>>> Enumerator(lambda: (xs for xs in [[False, True]]))
Enumerator(lambda: (xs for xs in [[False, True]]))
```

Define-and-register raw enumerations (function type as 2nd argument):

```py
>>> Enumerator(bool, lambda: (xs for xs in [[False, True]]))
Enumerator(lambda: (xs for xs in [[False, True]]))
```

Define-and-register list/choice enumerations?

```py
>>> Enumerator(int, itertools.count)
>>> Enumerator(int, gen.ints)
>>> Enumerator(bool, False, True)
>>> Enumerator(type(None), None)
```

We always zippend the rest of the arguments.

Problem: how to differentiate between `itertools.count()` and `(lambda:
tiers)`.  They are both callable.  Solution: check if it is tiers by looking at
the first element in the enumeration.  Better solution: requires flat
generators to be "called" already.


### A refinement

Maybe not use the constructor for registration?  Maybe yes.

```py
Enumerator(Class, type, type, type)
```

The above instantiates and registers and enumerator for Class, with type, type, type as argument enumerators.


```py
Enumerator(Class)
```

The above instantiates and registers or query an enumerator for Class, inferring argument enumerators


```py
Enumerator(Class, Enumerator(...), Enumerator(...)
```

The above does the same with explicit enumerators.


```py
Enumerator(Class, type, Enumerator(...))
```

Mixing-up is allowed.


Raw enumerations are permitted as well somehow.


I will probably need to define `__new__` instead of `__init__`, here's the default behaviour inherited from Object:

```py
class X:
	def __new__(cls):
		# X and cls are distinct upon inheritance.
		return super(X, cls).__new__(cls)
```
