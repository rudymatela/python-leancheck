#!/usr/bin/env python
#
# Example: using LeanCheck to test a simple user class
#
# (C) 2025  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
#
# This illustrates how one can use LeanCheck
# to define custom (global) enumerators.

from leancheck import *


class Person:
    name: str
    age: int

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


Enumerator.register(Person, Enumerator.cons(Person, str, int))

print(Enumerator(Person))
