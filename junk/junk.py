#!/usr/bin/env python
#
# Some misc funtions that may be of use in the future.
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

# Warning: this destroys argument generators!
def intercalate(generator1, generator2):
    """
    This function intercalates the two given generators.

    >>> list(intercalate((x for x in [1,2,3]), (y for y in [-1, -2, -3])))
    [1, -1, 2, -2, 3, -3]
    """
    while True:
        try:
            yield next(generator1)
        except StopIteration:
            yield from generator2
            break
        try:
            yield next(generator2)
        except StopIteration:
            yield from generator1
            break
