#!/usr/bin/env python
#
# Example: using LeanCheck to test Luciano Ramalho's Card class
# (cf. "Fluent Python")
#
# (C) 2025  Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)
#
# This illustrates how one can use LeanCheck
# to define custom (global) enumerators.

import collections
from leancheck import *

# Declare Fluent Python's Card class
Card = collections.namedtuple("Card", ["rank", "suit"])

# Define enumerators for rank and suits
rank_enumerator = Enumerator.from_list([c for c in "A23456789JQK"])
suits_enumerator = Enumerator.from_choices("spades diamonds clubs hearts".split())
card_enumerator = (rank_enumerator * suits_enumerator).map(lambda rs: Card(*rs))

# Registers a global Card enumerator
Enumerator.register(Card, card_enumerator)

# Access the Enumerator and pretty-prints it:
print(Enumerator[Card])  # type: ignore # TODO:

# Print all possible cards:
# type: ignore
for card in Enumerator[Card]:  # type: ignore # TODO:
    print(card)


# The enumerator allows us to define-and-test properties over cards
def prop_valid_suit(card: Card) -> bool:
    return card.suit in "spades diamonds clubs hearts".split()


def prop_valid_rank(card: Card) -> bool:
    return card.rank in "A23456789JQK"


main(verbose=True)
