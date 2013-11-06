#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools as it
from collections import defaultdict


def find_correlations(numstats):
    correlations = defaultdict(lambda: 0)
    for numstat in numstats:
        snumstats = sorted(numstat)
        combos = it.combinations(snumstats, r=2)
        for combo in combos:
            combotuple = (combo[0], combo[1])
            correlations[combotuple] += 1
    return dict(correlations)


def find_counts(numstats):
    return dict(
        (k, len(list(g))) for (k, g) in
        it.groupby(
            sorted(it.chain.from_iterable(numstats))
        )
    )
