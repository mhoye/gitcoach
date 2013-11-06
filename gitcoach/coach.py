#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Functions related to finding codependencies.'''


def find_relevant_correlations(correlations, coachfile, file_commits):
    '''Find which correlations in the `correlations` dictionary
    are relevant to `coachfile` and normalize their counts relative to
    file_commits.

    >>> find_relevant_correlations({('f1', 'f2'): 1, ('f2', 'f3'): 2}, 'f2', 3)
    {'f1': 0.33, 'f3': 0.66}
    '''
    return {
        ([k for k in [k1, k2] if k != coachfile][0]): 1.*v/file_commits
        for (k1, k2), v in correlations.items()
        if coachfile in [k1, k2]
    }


def filter_threshold(correlations, threshold):
    '''Return a new dictionary with `correlations` above or equal to
    threshold.'''
    return {
        k: v
        for k, v in correlations.items()
        if v >= threshold
    }
