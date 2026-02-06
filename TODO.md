TODO for leancheck.py
=====================

* turns out using `__class__getitem__` for retrieving global enumerations
  was not a good idea after all.
  [See this](https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__).

  "The purpose of `__class_getitem__()` is to allow runtime parameterization of
  standard-library generic classes in order to more easily apply type hints to
  these classes."

  "Using `__class_getitem__()` on any class for purposes other than type
  hinting is discouraged."

  Its unpythonic, so I'll replace it soon enough...

* add instructions on how to create enumerators for custom types on README

* release

* fix infinite loop in `print(Enumerator[set[bool]])`

* simplify code

* Add some built-in benchmarks.
  Performance is not so good currently.

* add carry-on flag

* package _all_ files like in Haskell's leancheck
