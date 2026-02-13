#!/usr/bin/env python
#
# Example: using LeanCheck to test a simple user class
#
# (C) 2026  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
#
# This illustrates how one can use LeanCheck
# to define custom (global) enumerators.

from leancheck import *


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"

# The enumeration inferred from the constructor's argument types
# produces spurious values as names, e.g.:
# Person('', 0)
# Person('aa', 0)
# Person('', -1)
# etc
print(Enumerator(Person))

# We can refine by registering an explicit enumerator
# with a better selection of names and age range.
Enumerator.register_cons(
    Person,
    Enumerator.choices(["Alice", "Bob", "Eve"]),
    Enumerator.choices(range(0,99))
)

# Now test values are better:
# Person('Alice', 2)
# Person('Bob', 0)
# etc...
print(Enumerator(Person))
