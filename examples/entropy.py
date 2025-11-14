#!/bin/bash
#
# Example: using LeanCheck to test an entropy function
#
# (C) 2025 Rudy Matela
# Distributed under the LGPL v2.1 or later (see the file LICENSE)

import leancheck
from math import log

def entropy(probabilities: list[float]) -> float:
    return -sum(p * log(p, 2) for p in probabilities)
    # fix by adding 'if p != 0'

def prop_unit1() -> bool:
    return entropy([1.0]) == 0.0

def prop_unit2() -> bool:
    return entropy([0.5,0.5]) == 1.0

def prop_unit3() -> bool:
    return entropy([0.25,0.25,0.25,0.25]) == 2.0

def prop_unit4() -> bool:
    return entropy([0.99,0.01]) == 0.08079313589591118

def prop_unit5() -> bool:
    return entropy([1/6, 1/6, 1/6, 1/6, 1/6, 1/6]) == 2.584962500721156

def prop_range(p: float) -> bool:
    return 0 < entropy([p, 1-p]) <= 1 if 0 < p < 1 else True

def prop_range0(p: float) -> bool:
    return 0 <= entropy([p, 1-p]) <= 1 if 0 <= p <= 1 else True

if __name__ == '__main__':
    leancheck.main(verbose = True, exit_on_failure = False)
