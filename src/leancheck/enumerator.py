#!/usr/bin/env python
#
# LeanCheck for Python.  Enumerator module.
#
# (C) 2023-2026  Rudy Matela
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

    Nesting can be arbitrary:

    >>> print(Enumerator[list[list[int]]])
    [[], [[]], [[], []], [[0]], [[], [], []], [[], [0]], ...]

    You can use this class to build new enumerations
    which can be registered using the `Enumerator.register()` method.

    This class supports computing sums and products of enumerations:

    >>> print(Enumerator[int] + Enumerator[bool])
    [0, False, True, 1, -1, 2, ...]

    Use `*` to take the product of two enumerations:

    >>> print(Enumerator[int] * Enumerator[bool])
    [(0, False), (0, True), (1, False), (1, True), (-1, False), (-1, True), ...]
    """

    tiers: typing.Callable[[], typing.Generator[list]]
    """
    Generate tiers of values.

    >>> list(Enumerator[bool].tiers())
    [[False, True]]
    """

    def __new__(cls, *args):
        """
        Raw initialization of an enumerator
        with a (potentially infinite) generator of finite lists.

        >>> Enumerator(lambda: ([x] for x in itertools.count()))
        Enumerator(lambda: (xs for xs in [[0], [1], [2], [3], [4], [5], ...]))

        >>> Enumerator(lambda: (ps for ps in [[False, True]]))
        Enumerator(lambda: (xs for xs in [[False, True]]))

        No arguments yield an empty enumerator:
        >>> Enumerator()
        Enumerator(lambda: (xs for xs in []))

        With a type, this queries `register()`ed enumerators:
        >>> Enumerator(int)
        Enumerator(lambda: (xs for xs in [[0], [1], [-1], [2], [-2], [3], ...]))
        """
        match args:
            case []:
                return cls.empty()
            case [ty] if type(ty) in [type, types.GenericAlias, typing.Union, types.UnionType]:
                return cls.find(ty)
            case [tiers]:
                e = super(Enumerator, cls).__new__(cls)
                e.tiers = tiers
                return e
            case _:
                raise ValueError("could not construct Enumerator")  # TODO: display args

    def __iter__(self):
        return ii.flatten(self.tiers())

    @classmethod
    def choices(cls, *iis):
        """
        Builds an enumerator from choices of iterables or items.

        >>> Enumerator.choices(itertools.count)
        Enumerator(lambda: (xs for xs in [[0], [1], [2], [3], [4], [5], ...]))

        >>> Enumerator.choices([1,2,3], False, True)
        Enumerator(lambda: (xs for xs in [[1, False, True], [2], [3]]))

        Note strings are iterables, you need to nest if you plan to include
        them:

        >>> Enumerator.choices([1,2,3], ["abc"])
        Enumerator(lambda: (xs for xs in [[1, 'abc'], [2], [3]]))

        >>> Enumerator.choices([1,2,3], "abc")
        Enumerator(lambda: (xs for xs in [[1, 'a'], [2, 'b'], [3, 'c']]))

        Initializes an enumerator from a list of options.
        Earlier values are considered of smaller size than later values.

        >>> Enumerator.choices([0,2,4,6])
        Enumerator(lambda: (xs for xs in [[0], [2], [4], [6]]))

        TODO: improve these docs
        """

        def tierify(obj):
            try:
                return ii.nest(obj())
            except TypeError:  # not callable
                try:
                    return ii.nest(iter(obj))
                except TypeError:
                    return ii.unit(obj)

        return cls(lambda: ii.zippend(*[tierify(i) for i in iis]))

    @classmethod
    def cons(cls, ty, *etys):
        """
        For types that can be constructed from other types,
        one can just list the class and type arguments:

        >>> print(Enumerator.cons(complex, float, float))
        [0j, 1j, (1+0j), -1j, (1+1j), (-1+0j), ...]

        ... or enumerations:

        >>> print(Enumerator.cons(complex, Enumerator(float), Enumerator(float)))
        [0j, 1j, (1+0j), -1j, (1+1j), (-1+0j), ...]
        """
        return Enumerator.product(
            *[Enumerator(et) if not isinstance(et, Enumerator) else et for et in etys]
        ).map(lambda vs: ty(*vs))

    def lists(self):
        """
        Constructs an enumerator of lists of values from another enumeration.

        >>> print(Enumerator.lists(Enumerator[int]))
        [[], [0], [0, 0], [1], [0, 0, 0], [0, 1], ...]

        >>> print(Enumerator[int].lists())
        [[], [0], [0, 0], [1], [0, 0, 0], [0, 1], ...]

        You are perhaps better off using:

        >>> print(Enumerator[list[int]])
        [[], [0], [0, 0], [1], [0, 0, 0], [0, 1], ...]
        """
        return Enumerator(lambda: ii.listss(self.tiers))

    def sets(self):
        """
        Constructs an enumerator of sets of values from another enumeration.

        >>> print(Enumerator[int].sets())
        [set(), {0}, {1}, {0, 1}, {-1}, {0, -1}, ...]

        >>> Enumerator[bool].sets()
        Enumerator(lambda: (xs for xs in [[set()], [{False}, {True}], [{False, True}], [], [], [], ...]))

        You are perhaps better off using:

        >>> print(Enumerator[set[int]])
        [set(), {0}, {1}, {0, 1}, {-1}, {0, -1}, ...]

        >>> Enumerator[set[bool]]
        Enumerator(lambda: (xs for xs in [[set()], [{False}, {True}], [{False, True}], [], [], [], ...]))

        Nested sets are allowed:

        >>> print(Enumerator[set[frozenset[int]]])
        [set(), {frozenset()}, {frozenset({0})}, {frozenset(), frozenset({0})}, {frozenset({1})}, {frozenset(), frozenset({1})}, ...]
        """
        # TODO: Fix the following innefficient enumerator for sets
        return self.lists().that(lambda xs: all(x < y for x, y in zip(xs, xs[1:]))).map(set)

    def dicts(self, other):
        """
        Constructs an enumeration of dictionaries.

        >>> print(Enumerator[int].dicts(Enumerator[int]))
        [{}, {0: 0}, {0: 1}, {1: 0}, {0: -1}, {1: 1}, ...]

        >>> print(Enumerator[bool].dicts(Enumerator[int]))
        [{}, {False: 0}, {True: 0}, {False: 1}, {True: 1}, {False: 0, True: 0}, ...]

        You are perhaps better of using:

        >>> print(Enumerator[dict[int,int]])
        [{}, {0: 0}, {0: 1}, {1: 0}, {0: -1}, {1: 1}, ...]

        >>> print(Enumerator[dict[bool,int]])
        [{}, {False: 0}, {True: 0}, {False: 1}, {True: 1}, {False: 0, True: 0}, ...]

        >>> print(Enumerator[dict[bool,bool]])
        [{}, {False: False}, {False: True}, {True: False}, {True: True}, {False: False, True: False}, ...]
        """
        return self.sets().concatmap(
            lambda s: Enumerator.product(*[other] * len(s)).map(lambda vs: dict(zip(s, vs)))
        )

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

        When not set, LeanCheck defaults to 6 tiers.

        >>> Enumerator.set_repr_length(6)
        >>> Enumerator[int]
        Enumerator(lambda: (xs for xs in [[0], [1], [-1], [2], [-2], [3], ...]))
        """
        # NOTE: In the doctests above,
        #       the default reversal is needed
        #       to not affect other doctests.
        self._repr_len = repr_len

    @classmethod
    def set_str_length(self, str_len: int):
        """
        Configures the maximum length of the Enumerator's representation.

        >>> Enumerator.set_str_length(12)
        >>> print(Enumerator[int])
        [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, ...]

        When not set, LeanCheck defaults to 6 items.

        >>> Enumerator.set_str_length(6)
        >>> print(Enumerator[int])
        [0, 1, -1, 2, -2, 3, ...]
        """
        # NOTE: In the doctests above,
        #       the default reversal is needed
        #       to not affect other doctests.
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
    def empty(cls):
        return cls(lambda: (xs for xs in []))

    def sum(*enumerators):
        """
        Computes the sum of several enumerators
        respecting size-order.

        >>> print(Enumerator[int].sum(Enumerator[bool],Enumerator[str]))
        [0, False, True, '', 1, 'a', ...]

        >>> print(Enumerator[int].sum(Enumerator[int]))
        [0, 0, 1, 1, -1, -1, ...]

        If you have just two enumerations, you are better off using `+`:
        >>> print(Enumerator[int] + Enumerator[bool])
        [0, False, True, 1, -1, 2, ...]
        """
        return sum(enumerators, start=Enumerator.empty())

    def product(*enumerators):
        """
        Computes the product of several enumerators
        returning an enumeration of tuples.

        >>> print(Enumerator.product(Enumerator[int], Enumerator[bool], Enumerator[list[int]]))
        [(0, False, []), (0, True, []), (0, False, [0]), (0, True, [0]), (1, False, []), (1, True, []), ...]

        >>> print(Enumerator[bool].product(Enumerator[float], Enumerator[str]))
        [(False, 0.0, ''), (True, 0.0, ''), (False, 0.0, 'a'), (False, 1.0, ''), (True, 0.0, 'a'), (True, 1.0, ''), ...]

        If you have just two enumerations, you can simply use `*`:

        >>> print(Enumerator[int] * Enumerator[bool])
        [(0, False), (0, True), (1, False), (1, True), (-1, False), (-1, True), ...]
        """
        if len(enumerators) == 0:
            return Enumerator(lambda: (xs for xs in [[()]]))
        else:
            e, *es = enumerators
            return (e * Enumerator.product(*es)).map(lambda t: (t[0],) + t[1])

    def concatmap(self, f):
        """
        Map and concatenate enumerators.

        >>> Enumerator[int].concatmap(lambda x: Enumerator(lambda: (xs for xs in [[x],[x]])))
        Enumerator(lambda: (xs for xs in [[0], [0, 1], [1, -1], [-1, 2], [2, -2], [-2, 3], ...]))

        This has its use in the implementation of some
        enumerators-without-repetitions, such as dicts.
        """
        return Enumerator(lambda: ii.cconcatmap(lambda x: f(x).tiers(), self.tiers()))

    _enumerators: dict = {}

    @classmethod
    def register(cls, c, enumerator):
        """
        Registers an enumerator for the given type.

        >>> Enumerator.register(bool, Enumerator(lambda: (xs for xs in [[False, True]])))
        """
        cls._enumerators[c] = enumerator

    @classmethod
    def find(cls, c):
        try:
            if type(c) is types.GenericAlias:
                origin = typing.get_origin(c)
                args = typing.get_args(c)
                enums = [Enumerator[a] for a in args]
                return cls._enumerators[origin](*enums)
            if type(c) in [typing.Union, types.UnionType]:
                # ^ oof.., cf. stackoverflow.com/q/45957615
                args = typing.get_args(c)
                enums = [Enumerator[a] for a in args]
                return cls.sum(*enums)
            else:
                return cls._enumerators[c]
        except KeyError as err:
            raise TypeError(f"could not find Enumerator for {c}") from err

    # @classmethod # automatic
    def __class_getitem__(cls, c):
        """
        Finds an enumerator for the given type.

        >>> Enumerator[int]
        Enumerator(lambda: (xs for xs in [[0], [1], [-1], [2], [-2], [3], ...]))

        >>> Enumerator[bool]
        Enumerator(lambda: (xs for xs in [[False, True]]))

        >>> Enumerator[int | bool]
        Enumerator(lambda: (xs for xs in [[0, False, True], [1], [-1], [2], [-2], [3], ...]))

        >>> print(Enumerator[list[int]])
        [[], [0], [0, 0], [1], [0, 0, 0], [0, 1], ...]

        >>> print(Enumerator[tuple[bool, int]])
        [(False, 0), (True, 0), (False, 1), (True, 1), (False, -1), (True, -1), ...]

        >>> print(Enumerator[tuple[int,int,int]])
        [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, 1, 1), ...]

        >>> print(Enumerator[type])
        Traceback (most recent call last):
        ...
        TypeError: could not find Enumerator for <class 'type'>
        """
        return cls.find(c)

    @classmethod
    def default(cls):
        """
        Reverses the effect of `only_positives()`
        restoring negatives in numeric enumerations.

        >>> Enumerator.default()
        """
        cls.register(int, cls.choices(gen.ints))
        cls.register(float, cls.choices(gen.floats))

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
        cls.register(int, cls.choices(gen.positive_ints))
        cls.register(float, cls.choices(gen.positive_floats))

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
        cls.register(int, cls.choices(gen.non_negative_ints))
        cls.register(float, cls.choices(gen.non_negative_floats))


# Registers default Enumerators
Enumerator.register(int, Enumerator.choices(gen.ints))
Enumerator.register(float, Enumerator.choices(gen.floats))
Enumerator.register(bool, Enumerator.choices(False, True))
Enumerator.register(list, Enumerator.lists)  # i.e.: lambda e: e.lists()
Enumerator.register(tuple, Enumerator.product)  # i.e.: lambda *e: Enumerator.product(*e)
Enumerator.register(str, Enumerator(gen.strss))
Enumerator.register(set, Enumerator.sets)
Enumerator.register(dict, Enumerator.dicts)
Enumerator.register(frozenset, lambda e: e.sets().map(frozenset))

Enumerator.register(types.NoneType, Enumerator.choices(None))
Enumerator.register(Ellipsis, Enumerator.choices(...))
Enumerator.register(NotImplemented, Enumerator.choices(NotImplemented))
# Enumerator.register(type, Enumerator.from_list([int, bool, float, list, tuple, str, set, dict, frozenset, complex, range]))

Enumerator.register(complex, Enumerator.cons(complex, float, float))
# TODO: try with different step values in the range enumeration
Enumerator.register(range, Enumerator.cons(range, int, int))

Enumerator.register(bytes, Enumerator[str].map(lambda s: bytes(s, "ascii")))  # type: ignore
Enumerator.register(bytearray, Enumerator[str].map(lambda s: bytearray(s, "ascii")))  # type: ignore
Enumerator.register(memoryview, Enumerator.cons(memoryview, bytes))


# Runs tests if this is not being imported as a module.
if __name__ == "__main__":
    import doctest
    import sys

    (failures, _) = doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
    if failures:
        sys.exit(1)
