#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Command entry points for gitcoach.
'''

import learn as l
import coach as c
import argparse
import itertools as it
import subprocess
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
    # TODO use files modified in a commit
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f')
    parser.add_argument('--threshold', '-t', type=float, default=0.8)
    args = parser.parse_args()
    coachfile = args.file

    threshold = args.threshold

    with open('learning-data.pickle', 'rb') as picklefile:
        cors, counts = pickle.load(picklefile)

    if args.file is not None:
        coach_files = [args.file]
    else:
        coach_files = get_modified_files()

    all_suggested_files = []
    for coachfile in coach_files:
        if coachfile in counts.keys():
            file_commits = counts[coachfile]
            relevant_cors = c.find_relevant_correlations(
                cors, coachfile, file_commits)
            above_threshold = c.filter_threshold(relevant_cors, threshold)
            all_suggested_files.extend((cor, suggested, coachfile) for (suggested, cor) in above_threshold.items())
        else:
            print ('We have no data for {}'.format(coachfile))

    print ('\nHere are some files you might want to look at:\n')
    for cor, fname, suggestedby in sorted(all_suggested_files, reverse=True):
        print ('{}\tsuggested by\t{} ({:2f})'.format(fname, suggestedby, cor))


def get_modified_files():
    '''Ask git which files have uncommitted changes.'''
    command = "git ls-files --full-name --modified"
    file_list = subprocess.check_output(command.split())
    return file_list.splitlines()
