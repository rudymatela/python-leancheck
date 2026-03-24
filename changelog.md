Changelog for Python's LeanCheck
================================


upcoming
--------

* include all tracked files in source distribution


v0.1.6 (March 2026)
-------------------

* add option to dump test values
* fix syntax highlighting in online docs
* more consistent inline/README documentation
* more README badges
* add `examples/float.py`
* add this changelog


v0.1.4 (March 2026)
-------------------

* mark this as beta instead of ~~alpha~~
* add regression tests


v0.1.2 (March 2026)
-------------------

* fix bug/error when property does not have a bool rettype:
  LeanCheck now properly reports "just" a warning.
* `Enumerator`: be more flexible in allowed types for some methods
* better built-in examples
* internal refactoring


v0.1.0 (February 2026)
----------------------

* use `Enumerator(type)` to query available enumerators
  in favour of overloading `__class_getitem()__`:
  `Enumerator` backwards compatibility with the `0.0.*` series is broken
* include version number in generated docs
* improve docs
* improve built-in-examples
* improve error messages
* internal refactoring


v0.0.2 -- v0.0.12 (November 2025 -- February 2026)
--------------------------------------------------

These are alpha releases:
see the git logs for details.


v0.0.0 -- August 2024
---------------------

Initial commit in the public repository
as an import from an internal repo.


Feb 2020
--------

The initial stub of python-leancheck was created in 2020
in an internal repository.
