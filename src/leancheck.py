#!/usr/bin/env python
#
# LeanCheck for Python.
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)


import itertools
import sys
from inspect import signature


class Enumerator:
    def __init__(self, tiers):
        self.tiers = tiers

    def __iter__(self):
        return to_list(self.tiers())

    @classmethod
    def from_gen(cls, gen):
        return cls(lambda: to_tiers(gen()))

    @classmethod
    def from_list(cls, lst):
        return cls(lambda: to_tiers(x for x in lst))

    @classmethod
    def from_choices(cls, choices):
        return cls(lambda: (cs for cs in [choices]))

    @classmethod
    def lists(cls, enumerator):
        return cls(lambda: llist(enumerator.tiers))

    def __add__(self, other):
        return Enumerator(lambda: zippend(self.tiers(), other.tiers()))

    def __mul__(self, other):
        return Enumerator(lambda: pproduct(self.tiers(), other.tiers()))

    def __repr__(self):
        # TODO: remove magic numbers: make them configurable?
        xss = [str(xs) for xs in itertools.islice(self.tiers(), 7)]
        if (len(xss) > 6):
            xss[6] = "..."
        return "Enumerator(lambda: (xs for xs in [" + ', '.join(xss) + "]))"

    def __str__(self):
        # TODO: remove magic numbers: make them configurable?
        xs = [str(x) for x in itertools.islice(self, 7)]
        if (len(xs) > 6):
            xs[6] = "..."
        return "[" + ', '.join(xs) + "]"

    def map(self, f):
        return Enumerator(lambda: mmap(f, self.tiers()))

    @classmethod
    def product(cls, enumerator, *enumerators):
        # TODO: FIXME: this seems quite unpythonic
        if len(enumerators) == 0:
            return enumerator.map(lambda x: (x,))
        else:
            return (enumerator * cls.product(*enumerators)).map(lambda t: (t[0],) + t[1])

    _enumerators = None

    # A hack!  Functions that use _enumerators, should first call this.
    @classmethod
    def _initialize(cls):
        "Initializes the internal _enumerators dictionary"
        if cls._enumerators is None:
            cls._enumerators = {
                int: cls.from_gen(itertools.count), # TODO: include negatives
                bool: cls.from_choices([False,True]),
            }
            # The following needs to be separate to avoid infinite recursion
            # as __class__getitem__ calls this very function _initialize.
            cls.register(list[int], cls.lists(cls[int]))
            cls.register(list[bool], cls.lists(cls[bool]))
            cls.register(tuple[int,int], cls[int] * cls[int])
            cls.register(tuple[int,int,int], cls.product(cls[int], cls[int], cls[int]))
            cls.register(tuple[int,bool], cls[int] * cls[bool])
            cls.register(tuple[bool,int], cls[bool] * cls[int])
            cls.register(tuple[bool,bool], cls[bool] * cls[bool])

    @classmethod
    def register(cls, c, enumerator):
        """
        Registers an enumerator for the given type.

        >>> Enumerator.register(bool, Enumerator(lambda: (xs for xs in [[False, True]])))
        """
        cls._initialize()
        cls._enumerators[c] = enumerator

    # @classmethod # automatic
    def __class_getitem__(cls, c):
        """
        Finds an enumerator for the given type.

        >>> Enumerator[int]
        Enumerator(lambda: (xs for xs in [[0], [1], [2], [3], [4], [5], ...]))

        >>> Enumerator[bool]
        Enumerator(lambda: (xs for xs in [[False, True]]))

        >>> print(Enumerator[list[int]])
        [[], [0], [0, 0], [1], [0, 0, 0], [1, 0], ...]

        >>> print(Enumerator[tuple[bool, int]])
        [(False, 0), (True, 0), (False, 1), (True, 1), (False, 2), (True, 2), ...]

        >>> print(Enumerator[tuple[int,int,int]])
        [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, 2), (0, 1, 1), ...]

        >>> print(Enumerator[type])
        Traceback (most recent call last):
        ...
        TypeError: could not find Enumerator for <class 'type'>
        """
        cls._initialize()
        try:
            return cls._enumerators[c]
        except KeyError as err:
            raise TypeError(f"could not find Enumerator for {c}") from err

def to_tiers(xs):
    for x in xs:
        yield [x]

def to_list(xss):
    for xs in xss:
        yield from xs

def zippend(*iiterables):
    return itertools.starmap(itertools.chain,itertools.zip_longest(*iiterables, fillvalue=[]))

# TODO: merge pproduct and pproduct_with
def pproduct(xss, yss):
    xss_ = []
    yss_ = []
    l = 0
    while True:
        xss_.append(list(next(xss, [])))
        yss_.append(list(next(yss, [])))
        l += 1
        zs = []
        for i in range(0,l):
            zs += itertools.product(xss_[i],yss_[l-i-1])
        if zs == []:
            # This is "sound-but-incomplete".
            # TODO: in the final version, use None as a default value
            # in the appends above
            # and break only in the case where we
            # end up with empty zs because of None values
            # there's an opportunity for memory optimization here
            # such as in the example of product between integers and booleans
            break
        yield zs

def pproduct_with(f, xss, yss):
    xss_ = []
    yss_ = []
    l = 0
    while True:
        xss_.append(list(next(xss, [])))
        yss_.append(list(next(yss, [])))
        l += 1
        zs = []
        for i in range(0,l):
            zs += [f(x,y) for x in xss_[i] for y in yss_[l-i-1]]
        if zs == []:
            # This is "sound-but-incomplete".
            # TODO: in the final version, use None as a default value
            # in the appends above
            # and break only in the case where we
            # end up with empty zs because of None values
            # there's an opportunity for memory optimization here
            # such as in the example of product between integers and booleans
            break
        yield zs

def delay(xss):
    yield []
    yield from xss

def mmap(f,xss):
    for xs in xss:
        yield [f(x) for x in xs]

def llist(mkTiers):
    yield [[]]
    yield from pproduct_with(lambda x, xs: xs + [x], mkTiers(), llist(mkTiers))

def colour_escapes():
    """
    Returns colour escape sequences for clear, red, green, blue and yellow

    >>> c, r, g, b, y = colour_escapes()
    """
    plats = ['linux'] # TODO: add other supported platforms
    supported = sys.stdout.isatty() and sys.platform in plats
    if supported:
        return '\x1b[m', '\x1b[1;31m', '\x1b[32m', '\x1b[34m', '\x1b[33m'
    else:
        return '', '', '', '', ''

def check(prop, max_tests=360):
    """
    Checks a property for several enumerated argument values.

    >>> def prop_commute(x:int, y:int) -> bool:
    ...     return x + y == y + x
    >>> check(prop_commute)
    +++ OK, passed 360 tests: prop_commute

    >>> def prop_increase(x:int, y:int) -> bool:
    ...     return x + y > x
    >>> check(prop_increase)
    *** Failed! Falsifiable after 1 tests:
        prop_increase(0, 0)

    >>> def prop_sorted_twice(xs: list[int]) -> bool:
    ...     return sorted(sorted(xs)) == sorted(xs)
    ...
    >>> check(prop_sorted_twice)
    +++ OK, passed 360 tests: prop_sorted_twice

    >>> def prop_sorted_len(xs: list[int]) -> bool:
    ...     return len(sorted(xs)) == len(xs)
    ...
    >>> check(prop_sorted_len)
    +++ OK, passed 360 tests: prop_sorted_len

    >>> def prop_sorted_wrong(xs: list[int]) -> bool:
    ...     return sorted(xs) == xs
    ...
    >>> check(prop_sorted_wrong)
    *** Failed! Falsifiable after 6 tests:
        prop_sorted_wrong([1, 0])
    """
    sig = signature(prop)
    ret = sig.return_annotation
    # print(f"Property's signature: {sig}")
    if ret != bool:
        print(f"Warning: property's return value is {ret} and not {bool}")
    es = []
    for par in sig.parameters.values():
        # print(par.annotation)
        e = Enumerator[par.annotation]
        es.append(e)
    clear, red, green, _, _ = colour_escapes()
    for i, args in enumerate(itertools.islice(Enumerator.product(*es), max_tests)):
        if not prop(*args):
            repr_args = ', '.join(map(repr, args))
            print(f"*** Failed! Falsifiable after {i+1} tests:")
            print(f"    {red}{prop.__name__}{clear}({repr_args})")
            return
    i = i+1
    exhausted = " (exhausted)" if i < max_tests else ""
    print(f"+++ OK, passed {i} tests{exhausted}: {green}{prop.__name__}{clear}")


if __name__ == "__main__":
    import doctest
    import sys
    (failures, _) = doctest.testmod()
    if failures:
        sys.exit(1)
