#!/usr/bin/env python
#
# Some misc funtions that may be of use in the future.
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

# Warning: this destroys argument generators!
def intercalate(generator1, generator2):
    """
    This function intercalates the two given iterables.

    >>> list(intercalate([1,2,3], [-1, -2, -3])
    [1, -1, 2, -2, 3, -3]

    If the arguments are generators, they will be consumed.

    >>> list(intercalate((x for x in [1,2,3]), (y for y in [4,5,6])))
    [1, 4, 2, 5, 3, 6]
    """
    g1 = (x for x in generator1) # makes this work on lists
    g2 = (y for y in generator2) # makes this work on lists
    while True:
        try:
            yield next(g1)
        except StopIteration:
            yield from g2
            break
        try:
            yield next(g2)
        except StopIteration:
            yield from g1
            break
