#!/usr/bin/env python
#
# LeanCheck for Python.  Enumerator module.
#
# (C) 2023-2025  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
"""
This is part of the [LeanCheck package](https://pypi.org/project/leancheck/):
an enumerative property-based testing library for Python.

This module defines the `Enumerator` class.


You are better off importing the main `leancheck` module
with `import leancheck`.
"""


import itertools
import types
import typing
import leancheck.iitertools as ii
import leancheck.gen as gen


class Enumerator:
    """
    This class enumerates test values.

    Enumerations are represented internally as
    [a (potentially infinite) generator of finite lists](https://matela.com.br/thesis-rudy.pdf):
    tiers of values of increasing size.
    This is needed in order for the enumeration to be fair.

    As a user, you can query available enumerations with
    enumerations with "indexing":

    >>> Enumerator[int]
    Enumerator(lambda: (xs for xs in [[0], [1], [-1], [2], [-2], [3], ...]))

    >>> Enumerator[bool]
    Enumerator(lambda: (xs for xs in [[False, True]]))

    >>> print(Enumerator[list[int]])
    [[], [0], [0, 0], [1], [0, 0, 0], [0, 1], ...]

    >>> print(Enumerator[tuple[bool, int]])
    [(False, 0), (True, 0), (False, 1), (True, 1), (False, -1), (True, -1), ...]

    >>> print(Enumerator[tuple[int,int,int]])
    [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, 1, 1), ...]

    You can use this class to build new enumerations
    which can be registered using the `Enumerator.register()` method.

    This class supports computing sums and products of enumerations:

    >>> print(Enumerator[int] + Enumerator[bool])
    [0, False, True, 1, -1, 2, ...]

    Use `*` to take the product of two enumerations:

    >>> print(Enumerator[int] * Enumerator[bool])
    [(0, False), (0, True), (1, False), (1, True), (-1, False), (-1, True), ...]
    """

    tiers: typing.Callable[[], typing.Generator]
    """
    Generate tiers of values.

    >>> list(Enumerator[bool].tiers())
    [[False, True]]
    """

    def __init__(self, tiers):
        """
        Raw initialization of an enumerator
        with a (potentially infinite) generator of finite lists.

        >>> Enumerator(lambda: ([x] for x in itertools.count()))
        Enumerator(lambda: (xs for xs in [[0], [1], [2], [3], [4], [5], ...]))

        >>> Enumerator(lambda: (ps for ps in [[False, True]]))
        Enumerator(lambda: (xs for xs in [[False, True]]))
        """

        self.tiers = tiers

    def __iter__(self):
        return ii.flatten(self.tiers())

    @classmethod
    def from_gen(cls, gen):
        """
        Initializes an enumerator directly from a plain generator.

        >>> Enumerator.from_gen(itertools.count)
        Enumerator(lambda: (xs for xs in [[0], [1], [2], [3], [4], [5], ...]))
        """
        return cls(lambda: ii.nest(gen()))

    @classmethod
    def from_list(cls, lst):
        """
        Initializes an enumerator from a list of options.
        Earlier values are considered of smaller size than later values.

        >>> Enumerator.from_list([0,2,4,6])
        Enumerator(lambda: (xs for xs in [[0], [2], [4], [6]]))
        """
        return cls(lambda: ii.nest(x for x in lst))

    @classmethod
    def from_choices(cls, choices):
        """
        Initializes an enumerator from a list of choices.
        All given values are considered to be of the same size.

        >>> Enumerator.from_choices([0,2,4,6])
        Enumerator(lambda: (xs for xs in [[0, 2, 4, 6]]))
        """
        return cls(lambda: (cs for cs in [choices]))

    @classmethod
    def lists(cls, enumerator):
        """
        Constructs an enumerator of lists of values from another enumeration.

        >>> print(Enumerator.lists(Enumerator[int]))
        [[], [0], [0, 0], [1], [0, 0, 0], [0, 1], ...]

        You are perhaps better off using:

        >>> print(Enumerator[list[int]])
        [[], [0], [0, 0], [1], [0, 0, 0], [0, 1], ...]
        """
        return cls(lambda: ii.listss(enumerator.tiers))

    def __add__(self, other):
        """
        Use `+` to compute the sum of two enumerations:

        >>> print(Enumerator[int] + Enumerator[bool])
        [0, False, True, 1, -1, 2, ...]

        >>> Enumerator[int] + Enumerator[bool]
        Enumerator(lambda: (xs for xs in [[0, False, True], [1], [-1], [2], [-2], [3], ...]))
        """
        return Enumerator(lambda: ii.zippend(self.tiers(), other.tiers()))

    def __mul__(self, other):
        """
        Use `*` to take the product of two enumerations:

        >>> print(Enumerator[int] * Enumerator[bool])
        [(0, False), (0, True), (1, False), (1, True), (-1, False), (-1, True), ...]

        >>> Enumerator[int] * Enumerator[bool]
        Enumerator(lambda: (xs for xs in [[(0, False), (0, True)], [(1, False), (1, True)], [(-1, False), (-1, True)], [(2, False), (2, True)], [(-2, False), (-2, True)], [(3, False), (3, True)], ...]))
        """
        return Enumerator(lambda: ii.pproduct(self.tiers(), other.tiers()))

    _repr_len: int = 6

    def __repr__(self):
        l = self._repr_len
        xss = [repr(xs) for xs in itertools.islice(self.tiers(), l + 1)]
        if len(xss) > l:
            xss[l] = "..."
        return "Enumerator(lambda: (xs for xs in [" + ", ".join(xss) + "]))"

    _str_len: int = 6

    def __str__(self):
        l = self._str_len
        xs = [repr(x) for x in itertools.islice(self, l + 1)]
        if len(xs) > l:
            xs[l] = "..."
        return "[" + ", ".join(xs) + "]"

    @classmethod
    def set_repr_length(self, repr_len: int):
        """
        Configures the maximum length of the Enumerator's representation.

        >>> Enumerator.set_repr_length(3)
        >>> Enumerator[int]
        Enumerator(lambda: (xs for xs in [[0], [1], [-1], ...]))
        >>> Enumerator.set_repr_length(6)

        When not set, LeanCheck defaults to 6 tiers.
        """
        self._repr_len = repr_len

    @classmethod
    def set_str_length(self, str_len: int):
        """
        Configures the maximum length of the Enumerator's representation.

        >>> Enumerator.set_str_length(12)
        >>> print(Enumerator[int])
        [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, ...]

        When not set, LeanCheck defaults to 6 items.
        """
        self._str_len = str_len

    def map(self, f):
        """
        Applies a function to all values in the enumeration.

        >>> Enumerator[int].map(lambda x: x*2)
        Enumerator(lambda: (xs for xs in [[0], [2], [-2], [4], [-4], [6], ...]))
        """
        return Enumerator(lambda: ii.mmap(f, self.tiers()))

    def that(self, p):
        """
        Filters values in an enumeration that match a given predicate.

        >>> Enumerator[int].that(lambda x: x % 2 == 0)
        Enumerator(lambda: (xs for xs in [[0], [], [], [2], [-2], [], ...]))

        >>> Enumerator[int].that(lambda x: x > 0)
        Enumerator(lambda: (xs for xs in [[], [1], [], [2], [], [3], ...]))

        This may be innefficient due to empty tiers and unneeded computation,
        use with care.
        """
        return Enumerator(lambda: ii.ffilter(p, self.tiers()))

    @classmethod
    def product(cls, *enumerators):
        """
        Computes the product of several enumerators
        returning an enumeration of tuples.

        >>> print(Enumerator.product(Enumerator[int], Enumerator[bool], Enumerator[list[int]]))
        [(0, False, []), (0, True, []), (0, False, [0]), (0, True, [0]), (1, False, []), (1, True, []), ...]

        If you have just two enumerations, you can simply use `*`:

        >>> print(Enumerator[int] * Enumerator[bool])
        [(0, False), (0, True), (1, False), (1, True), (-1, False), (-1, True), ...]
        """
        if len(enumerators) == 0:
            return Enumerator(lambda: (xs for xs in [[()]]))
        else:
            e, *es = enumerators
            return (e * cls.product(*es)).map(lambda t: (t[0],) + t[1])

    _enumerators: dict = {}

    @classmethod
    def register(cls, c, enumerator):
        """
        Registers an enumerator for the given type.

        >>> Enumerator.register(bool, Enumerator(lambda: (xs for xs in [[False, True]])))
        """
        cls._enumerators[c] = enumerator

    # @classmethod # automatic
    def __class_getitem__(cls, c):
        """
        Finds an enumerator for the given type.

        >>> Enumerator[int]
        Enumerator(lambda: (xs for xs in [[0], [1], [-1], [2], [-2], [3], ...]))

        >>> Enumerator[bool]
        Enumerator(lambda: (xs for xs in [[False, True]]))

        >>> print(Enumerator[list[int]])
        [[], [0], [0, 0], [1], [0, 0, 0], [0, 1], ...]

        >>> print(Enumerator[tuple[bool, int]])
        [(False, 0), (True, 0), (False, 1), (True, 1), (False, -1), (True, -1), ...]

        >>> print(Enumerator[tuple[int,int,int]])
        [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, 1, 1), ...]

        >>> print(Enumerator[set[int]])
        [[], [0], [1], [0, 1], [-1], [-1, 0], ...]

        >>> print(Enumerator[type])
        Traceback (most recent call last):
        ...
        TypeError: could not find Enumerator for <class 'type'>
        """
        try:
            if type(c) is types.GenericAlias:
                origin = typing.get_origin(c)
                args = typing.get_args(c)
                enums = [Enumerator[a] for a in args]
                return cls._enumerators[origin](*enums)
            else:
                return cls._enumerators[c]
        except KeyError as err:
            raise TypeError(f"could not find Enumerator for {c}") from err

    @classmethod
    def default(cls):
        """
        Reverses the effect of `only_positives()`
        restoring negatives in numeric enumerations.

        >>> Enumerator.default()
        """
        cls.register(int,   cls.from_gen(gen.ints))
        cls.register(float, cls.from_gen(gen.floats))

    @classmethod
    def only_positives(cls):
        """
        Forces enumerations to contain only positive numbers:

        >>> Enumerator.only_positives()
        >>> print(Enumerator[int])
        [1, 2, 3, 4, 5, 6, ...]
        >>> print(Enumerator[float])
        [1.0, 0.5, 2.0, 0.3333333333333333, 1.5, 0.6666666666666666, ...]
        >>> print(Enumerator[list[tuple[int,float]]])
        [[], [(1, 1.0)], [(1, 1.0), (1, 1.0)], [(1, 0.5)], [(2, 1.0)], [(1, 1.0), (1, 1.0), (1, 1.0)], ...]

        Reset with

        >>> Enumerator.default()
        """
        cls.register(int,   cls.from_gen(gen.positive_ints))
        cls.register(float, cls.from_gen(gen.positive_floats))

    @classmethod
    def only_non_negatives(cls):
        """
        Forces enumerations to contain only non-negative numbers,
        i.e. zero and positives:

        >>> Enumerator.only_non_negatives()
        >>> print(Enumerator[int])
        [0, 1, 2, 3, 4, 5, ...]
        >>> print(Enumerator[float])
        [0.0, 1.0, 0.5, 2.0, 0.3333333333333333, 1.5, ...]
        >>> print(Enumerator[list[tuple[int,float]]])
        [[], [(0, 0.0)], [(0, 0.0), (0, 0.0)], [(0, 1.0)], [(1, 0.0)], [(0, 0.0), (0, 0.0), (0, 0.0)], ...]

        Reset with

        >>> Enumerator.default()
        """
        cls.register(int,   cls.from_gen(gen.non_negative_ints))
        cls.register(float, cls.from_gen(gen.non_negative_floats))


# Registers default Enumerators
Enumerator.register(int, Enumerator.from_gen(gen.ints))
Enumerator.register(float, Enumerator.from_gen(gen.floats))
Enumerator.register(bool, Enumerator.from_choices([False, True]))
Enumerator.register(list, lambda e: Enumerator.lists(e))
Enumerator.register(tuple, lambda *e: Enumerator.product(*e))
Enumerator.register(str, Enumerator(gen.strss))
# TODO: Fix the following innefficient enumerator for the set type
Enumerator.register(set, lambda e: Enumerator.lists(e).that(lambda xs: all(x < y for x, y in zip(xs, xs[1:]))))


# Runs tests if this is not being imported as a module.
if __name__ == "__main__":
    import doctest
    import sys

    (failures, _) = doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    if failures:
        sys.exit(1)
