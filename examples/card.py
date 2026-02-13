#!/usr/bin/env python
#
# Example: using LeanCheck to test Luciano Ramalho's Card class
# (cf. "Fluent Python")
#
# (C) 2026  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
#
# This illustrates how one can use LeanCheck
# to define custom (global) enumerators.

import collections
from leancheck import *

# Declare Fluent Python's Card class
Card = collections.namedtuple("Card", ["rank", "suit"])

# Registers a global Card enumerator
Enumerator.register_cons(
    Card,
    Enumerator.choices([c for c in "A23456789JQK"]),
    Enumerator.choices(["spades"], ["diamonds"], ["clubs"], ["hearts"]),
)

# Access the Enumerator and pretty-prints it:
print(Enumerator(Card))

# Print all possible cards:
for card in Enumerator(Card):
    print(card)


# The enumerator allows us to define-and-test properties over cards
def prop_valid_suit(card: Card) -> bool:
    return card.suit in "spades diamonds clubs hearts".split()


def prop_valid_rank(card: Card) -> bool:
    return card.rank in "A23456789JQK"


main(verbose=True)
