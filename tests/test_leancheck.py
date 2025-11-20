#!/usr/bin/env python
#
# Tests for LeanCheck itself.
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)


import unittest
import itertools
from leancheck import Enumerator, check, holds


def take(n, generator):
    """
    This function returns a list with the first _n_ elements of a generator.

    >>> take(3, [1,2,3,4,5,6])
    [1, 2, 3]

    >>> take(6, itertools.count())
    [0, 1, 2, 3, 4, 5]
    """
    return list(itertools.islice(generator, n))


class TestLeanCheck(unittest.TestCase):

    def assertEnum(self, typ, lst):
        self.assertEqual(take(len(lst), Enumerator[typ]), lst)

    def assertFiniteEnum(self, typ, lst):
        self.assertEqual(list(Enumerator[typ]), lst)

    def test_constructor(self):
        e = Enumerator(lambda: ([x] for x in [3,1,3,3,7]))
        self.assertEqual(list(e), [3,1,3,3,7])
        self.assertEqual(list(e.tiers()), [[3],[1],[3],[3],[7]])
    
    def test_from_list(self):
        e = Enumerator.from_list([3,1,3,3,7])
        self.assertEqual(list(e), [3,1,3,3,7])

    def test_int(self):
        self.assertEnum(int, [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6])
        self.assertEnum(list[int], [[], [0], [0, 0], [1], [0, 0, 0], [1, 0]])

    def test_float(self):
        self.assertEnum(float, [0, 1, -1, 0.5, -0.5, 2, -2, 1/3, -1/3, 3/2, -3/2, 2/3])

    def test_bool(self):
        self.assertFiniteEnum(bool, [False,True])
        self.assertEnum(list[bool], [[], [False], [True], [False,False], [True,False], [False,True]])

    def test_tuple(self):
        self.assertEnum(tuple[int,int], [(0,0), (0,1), (1,0), (0,-1), (1,1), (-1,0)])
        self.assertEnum(tuple[int,int,int], [(0,0,0), (0,0,1), (0,1,0), (1,0,0), (0,0,-1), (0,1,1)])
        self.assertEnum(tuple[bool,bool], [(False, False), (False, True), (True, False), (True, True)])

    def test_properties(self):
        self.assertEqual(holds(lambda x: x + x >= x, types=[int]), False)
        self.assertEqual(holds(lambda x: x * x >= x, types=[int]), True)
        self.assertEqual(holds(lambda x: not x or 1 / x * x == 1, types=[float]), False)
        self.assertEqual(holds(lambda x: x / 3 * 3 == x, types=[float]), False)

    def test_empty_product(self):
        e = Enumerator.product()
        self.assertEqual(list(e), [()])
        self.assertEqual(list(e.tiers()), [[()]])


if __name__ == '__main__':
    unittest.main()
