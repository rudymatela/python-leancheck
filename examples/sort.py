#!/usr/bin/env python
#
# Example: using LeanCheck to test a sorting function
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

import leancheck

# A (not-quite) quicksort implementation.
# This is not intended to be most efficient
# but exists to illustrate a bug
def qsort(lst):
    if lst == []:
        return []
    x, *etc = lst  # split into head and tail
    lesser  = [y for y in etc if y < x]
    greater = [y for y in etc if y > x]
    return qsort(lesser) + [x] + qsort(greater)

def prop_unit1() -> bool:
    return qsort([4,3,2,1]) == [1,2,3,4]

def prop_unit2() -> bool:
    return qsort([3,1,2]) == [1,2,3]

def prop_sort_twice(xs: list[int]) -> bool:
    "Sorting a list once is the same as sorting twice."
    return qsort(qsort(xs)) == qsort(xs)

def prop_sort_ordered(xs: list[int]) -> bool:
    "Sorting a list returns the elements in order."
    def ordered(xs):
        for x, y in zip(xs, xs[1:]):
            if x > y:
                return False
        return True
    return ordered(qsort(xs))

def prop_sort_elem(x: int, xs: list[int]) -> bool:
    "Sorting preserves membership in the list."
    return (x in qsort(xs)) == (x in xs)

def prop_sort_len(xs: list[int]) -> bool:
    "Sorting should not change the length of the list."
    return len(qsort(xs)) == len(xs)

def prop_min(xs: list[int]) -> bool:
    "The minimum is the head of the sorted list."
    # Removing the precondition is a nice way to test exception handling and reporting.
    leancheck.precondition(len(xs) > 0)
    return qsort(xs)[0] == min(xs)

if __name__ == '__main__':
    leancheck.main(verbose = True, exit_on_failure = False)
