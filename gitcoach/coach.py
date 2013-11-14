#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Functions related to finding codependencies.'''


def normalize_correlations(correlations, coachfile_count):
    return {
        k: normalize_correlation(v, coachfile_count)
        for (k, v) in correlations.items()
    }


def normalize_correlation(coincidence_count, coachfile_count):
    '''Calculate a correlation between 0 and 1 for scoring.

    Essentially, we are calculating:

        P(Y|X) = times_XY_committed_together/times_X_committed

    Example:

    >>> normalize_correlation(3, 6)
    0.5
    '''
    return 1.*coincidence_count/coachfile_count


def find_relevant_correlations(correlations, coachfile):
    '''Find which correlations in the `correlations` dictionary
    are relevant to `coachfile` file_commits.

    >>> find_relevant_correlations({('f1', 'f2'): 1, ('f2', 'f3'): 2}, 'f2', 3)
    {'f1': 0.33, 'f3': 0.66}
    '''
    return {
        ([k for k in [k1, k2] if k != coachfile][0]): v
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
