#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Command entry points for gitcoach.
'''

import argparse
import learn as l
import itertools as it
import pickle


def learn():
    '''Entry point for gitlearn command.'''
    # TODO call git2json yourself instead of accepting as stdin
    import sys
    import json
    commits = json.load(sys.stdin)
    numstats = (
        [change[2] for change in commit['changes']]
        for commit in commits
    )
    t1, t2 = it.tee(numstats)
    correlations = l.find_correlations(t1)
    counts = l.find_counts(t2)
    result = (correlations, counts)
    with open('learning-data.pickle', 'wb') as outfile:
        pickle.dump(result, outfile)


def coach():
    '''Entry point for gitcoach command.'''
    # TODO add arguments from mhoye version
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--threshold', '-t', type=float, default=0.9)
    args = parser.parse_args()
    coachfile = args.file
    with open('learning-data.pickle', 'rb') as picklefile:
        correlations, counts = pickle.load(picklefile)
    file_commits = counts[args.file]
    relevant_correlations = {
        ([k for k in [k1, k2] if k != coachfile][0]): 1.*v/file_commits
        for (k1, k2), v in correlations.items()
        if coachfile == k1 or coachfile == k2
    }
    correlations_above_threshold = {
        k: v
        for k, v in relevant_correlations.items()
        if v >= args.threshold
    }
    print correlations_above_threshold
