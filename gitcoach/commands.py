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
import json


def learn():
    '''Entry point for gitlearn command.'''
    description = '''Generate coaching data for gitcoach.'''
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()

    # Run git2json and parse the commit data.
    gitpipe = subprocess.Popen(['git2json'], stdout=subprocess.PIPE)
    commits = json.load(gitpipe.stdout)

    # Get the files changed in each commit.
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
    description = '''Find co-dependent files based on git history.

    Two files are co-dependent if they have been modified in the same
    commits often enough.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--file', '-f',
        help='Find suggestions for a specific file'
    )
    parser.add_argument(
        '--commit', '-c',
        help='Find suggestions for files modified in a specific commit.'
    )
    parser.add_argument(
        '--threshold', '-t', type=float, default=0.8,
        help='Threshold for co-incidence ratio (default=0.8).'
    )
    args = parser.parse_args()
    coachfile = args.file

    threshold = args.threshold

    # TODO handle error (no coaching data available)
    with open('learning-data.pickle', 'rb') as picklefile:
        cors, counts = pickle.load(picklefile)

    if args.file is not None:
        coach_files = [args.file]
    if args.commit is not None:
        # TODO handle error (not in git folder)
        coach_files = get_commit_files(args.commit)
    else:
        # TODO handle error (not in git folder)
        # TODO handle error (invalid commit)
        # TODO handle error (non-existing commit)
        coach_files = get_modified_files()

    all_suggested_files = []
    for coachfile in coach_files:
        if coachfile in counts.keys():
            file_commits = counts[coachfile]
            relevant_cors = c.find_relevant_correlations(
                cors, coachfile, file_commits)
            above_threshold = c.filter_threshold(relevant_cors, threshold)
            all_suggested_files.extend(
                (cor, suggested, coachfile)
                for (suggested, cor) in above_threshold.items()
            )
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


def get_commit_files(commit):
    '''Ask git which files were modified in a given commit.'''
    command = "git log -1 --pretty=raw --numstat {}".format(commit)
    git_log_out = subprocess.check_output(command.split()) + '\n'
    from git2json import parse_commits
    commit = list(parse_commits(git_log_out))[0]
    return [change[2] for change in commit['changes']]
