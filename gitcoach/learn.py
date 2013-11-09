#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Functions related to learning.'''

import itertools as it
from collections import defaultdict


def find_correlations(numstats):
    '''find_correlations(numstats) -> {file_pair: coincidence_count}

    For each pair of files, find how many times they are modified in
    the same commit.

    >>> find_correlations([['a', 'b', 'c'], ['b', 'c']])
    {('a', 'b'): 1, ('a', 'c'): 1, ('b', 'c'): 2}
    '''
    correlations = defaultdict(lambda: 0)
    for numstat in numstats:
        snumstats = sorted(numstat)
        combos = it.combinations(snumstats, r=2)
        for combo in combos:
            combotuple = (combo[0], combo[1])
            correlations[combotuple] += 1
    return dict(correlations)


def find_counts(numstats):
    '''find_counts(numstats) -> {file: file_count}

    Find out how many commits have touched a given file.

    >>> find_counts([['a', 'b', 'c'], ['b', 'c']])
    {'a': 1, 'b': 2, 'c': 2}
    '''
    return dict(
        (k, len(list(g))) for (k, g) in
        it.groupby(
            sorted(it.chain.from_iterable(numstats))
        )
    )
