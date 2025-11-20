#!/usr/bin/env python
#
# Example: pretty-printing some default enumerators
#
# (C) 2025 Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

from leancheck import *

def pe(typ):
    name = typ.__name__ if type(typ) == type else str(typ)
    Enumerator.set_repr_length(12)
    print(f">>> print(Enumerator[{name}])")
    print(Enumerator[typ])
    print()
    Enumerator.set_repr_length(6)
    print(f">>> Enumerator[{name}]")
    print(repr(Enumerator[typ]))
    print()

pe(int)

Enumerator.set_repr_length(12)

pe(int)
pe(bool)
pe(list[int])
pe(list[bool])
