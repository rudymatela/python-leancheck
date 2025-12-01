#!/usr/bin/env python
#
# Example: pretty-printing some default enumerators
#
# (C) 2025 Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

from leancheck import *


def pe(typ):
    name = typ.__name__ if type(typ) == type else str(typ)
    print(f">>> print(Enumerator[{name}])")
    print(Enumerator[typ])
    print()
    print(f">>> Enumerator[{name}]")
    print(repr(Enumerator[typ]))
    print()


# TODO: make a function from string to string
#       that transforms list definitions into multiline
#       def multiline(str: string) -> string:

pe(int)

Enumerator.set_str_length(12)

pe(int)
pe(bool)
pe(list[int])
pe(list[bool])
pe(float)
pe(list[float])

pe(tuple[int, int])
pe(tuple[int, int, int])

pe(tuple[bool, bool])
pe(tuple[bool, bool, bool])

pe(tuple[bool, int])

pe(tuple[bool, int, float])

pe(str)
