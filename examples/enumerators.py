#!/usr/bin/env python
#
# Example: pretty-printing some default enumerators
#
# (C) 2025 Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

from leancheck import *

def pe(typ):
    print(f">>> Enumerator[{typ}]")
    print(Enumerator[typ])
    print()

pe(int)

Enumerator.set_repr_length(12)

pe(int)
pe(bool)
pe(list[int])
pe(list[bool])
