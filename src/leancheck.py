#!/usr/bin/env python
#
# LeanCheck for Python.
#
# (C) 2023-2024  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)


import itertools
import sys
import typing
from inspect import signature, getmembers
from types import GenericAlias


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
    def product(cls, *enumerators):
        if len(enumerators) == 0:
            return Enumerator(lambda: (xs for xs in [[()]]))
        else:
            e, *es = enumerators
            return (e * cls.product(*es)).map(lambda t: (t[0],) + t[1])

    _enumerators = None

    # A hack!  Functions that use _enumerators, should first call this.
    @classmethod
    def _initialize(cls):
        "Initializes the internal _enumerators dictionary"
        if cls._enumerators is None:
            cls._enumerators = {
                int: cls.from_gen(itertools.count), # TODO: include negatives
                bool: cls.from_choices([False,True]),
                list: lambda e: cls.lists(e),
                tuple: lambda *e: cls.product(*e),
            }

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
            if type(c) is GenericAlias:
                origin = typing.get_origin(c)
                args = typing.get_args(c)
                enums = [Enumerator[a] for a in args]
                return cls._enumerators[origin](*enums)
            else:
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

def pproduct(xss, yss, with_f=None):
    if with_f is None:
        with_f = lambda x, y: (x,y)
    xss_ = []
    yss_ = []
    l = 0
    while True:
        xss_.append(list(next(xss, [])))
        yss_.append(list(next(yss, [])))
        l += 1
        zs = []
        for i in range(0,l):
            zs += [with_f(x,y) for x in xss_[i] for y in yss_[l-i-1]]
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
    yield from pproduct(mkTiers(), llist(mkTiers), with_f=lambda x, xs: xs + [x])

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

def intercalate(generator1, generator2):
    """
    This function intercalates the two given iterables.

    >>> list(intercalate([1,2,3], [-1, -2, -3]))
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

def check(prop, max_tests=360, verbose=True, silent=False):
    """
    Checks a property for several enumerated argument values.

    >>> def prop_commute(x:int, y:int) -> bool:
    ...     return x + y == y + x
    >>> check(prop_commute)
    +++ OK, passed 360 tests: prop_commute
    True

    >>> def prop_increase(x:int, y:int) -> bool:
    ...     return x + y > x
    >>> check(prop_increase)
    *** Failed! Falsifiable after 1 tests:
        prop_increase(0, 0)
    False

    >>> def prop_sorted_twice(xs: list[int]) -> bool:
    ...     return sorted(sorted(xs)) == sorted(xs)
    ...
    >>> check(prop_sorted_twice)
    +++ OK, passed 360 tests: prop_sorted_twice
    True

    >>> def prop_sorted_len(xs: list[int]) -> bool:
    ...     return len(sorted(xs)) == len(xs)
    ...
    >>> check(prop_sorted_len)
    +++ OK, passed 360 tests: prop_sorted_len
    True

    >>> def prop_sorted_wrong(xs: list[int]) -> bool:
    ...     return sorted(xs) == xs
    ...
    >>> check(prop_sorted_wrong)
    *** Failed! Falsifiable after 6 tests:
        prop_sorted_wrong([1, 0])
    False

    >>> check(prop_sorted_twice, silent=True)
    True
    """
    verbose = verbose and not silent
    clear, red, green, blue, yellow = colour_escapes()
    sig = signature(prop)
    ret = sig.return_annotation
    # print(f"Property's signature: {sig}")
    if ret != bool and not silent:
        print(f"{yellow}Warning{clear}: property's return value is {ret} and not {bool}")
    es = []
    for par in sig.parameters.values():
        # print(par.annotation)
        e = Enumerator[par.annotation]
        es.append(e)
    for i, args in enumerate(itertools.islice(Enumerator.product(*es), max_tests)):
        if not prop(*args):
            if not silent:
                repr_args = ', '.join(map(repr, args))
                print(f"*** Failed! Falsifiable after {i+1} tests:")
                print(f"    {red}{prop.__name__}{clear}({repr_args})")
            return False
    if verbose:
        i = i+1
        exhausted = " (exhausted)" if i < max_tests else ""
        print(f"+++ OK, passed {i} tests{exhausted}: {green}{prop.__name__}{clear}")
    return True

def holds(prop, max_tests=360):
    """
    Alias to `check(prop, silent=True)`.

    >>> def prop_commute(x:int, y:int) -> bool:
    ...     return x + y == y + x
    >>> holds(prop_commute)
    True

    >>> def prop_increase(x:int, y:int) -> bool:
    ...     return x + y > x
    >>> holds(prop_increase)
    False
    """
    return check(prop, max_tests=max_tests, silent=True)

def testmod(max_tests=360, silent=False, verbose=False):
    n_failures = 0
    n_properties = 0
    def lineno(m):
        try:
            return m[1].__code__.co_firstlineno
        except AttributeError:
            return -1
    for name, member in sorted(getmembers(sys.modules["__main__"]), key=lineno):
        if name.startswith("prop_") and callable(member):
            n_properties += 1
            passed = check(member, max_tests=max_tests, silent=silent, verbose=verbose)
            if not passed:
                n_failures += 1
    return (n_failures, n_properties) # just like doctest.testmod()

def main(max_tests=360, silent=False, verbose=False, exit_on_failure=True):
    n_failures, n_properties = testmod(max_tests=max_tests, silent=silent, verbose=verbose)
    clear, red, green, blue, yellow = colour_escapes()
    if not silent:
        if not n_properties:
            print(f"{yellow}Warning{clear}: no properties found")
        if n_failures:
            print(f"\n{red}*** {n_failures} of {n_properties} properties failed{clear}")
        elif verbose:
            print(f"{green}+++ {n_properties} properties passed{clear}")
    if n_failures and exit_on_failure:
        sys.exit(1)

if __name__ == "__main__":
    import doctest
    import sys
    (failures, _) = doctest.testmod()
    if failures:
        sys.exit(1)
