#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Command entry points for gitcoach.
'''

from . import learn as l
from . import coach as c
import argparse
import itertools as it
import subprocess
import pickle
import json
import sys


def learn():
    '''Entry point for gitlearn command.'''
    description = '''Generate coaching data for gitcoach.'''
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()

    # Run git2json and parse the commit data.
    gitpipe = subprocess.Popen(
        ['git2json'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    data = gitpipe.stdout.read().decode()
    commits = json.loads(data)

    # Get the files changed in each commit.
    numstats = (
        [change[2] for change in commit['changes']]
        for commit in commits
    )

    t1, t2 = it.tee(numstats)
    correlations = l.find_correlations(t1)
    counts = l.find_counts(t2)

    result = (correlations, counts)
    try:
        with open(get_coachfile_path(), 'wb') as outfile:
            pickle.dump(result, outfile)
    except NotInGitDir:
        sys.stderr.write('Error: Not in a git directory.\n')
        sys.exit(-1)


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

    try:
        with open(get_coachfile_path(), 'rb') as picklefile:
            cors, counts = pickle.load(picklefile)
    except IOError:
        sys.stderr.write(
            'Error: Coaching data file does not exist.'
            'Try running gitlearn first.\n'
        )
        sys.exit(-1)
    except NotInGitDir:
        sys.stderr.write('Error: Not in a git directory\n')
        sys.exit(-1)

    if args.file is not None:
        coach_files = [args.file]
    elif args.commit is not None:
        try:
            coach_files = get_commit_files(args.commit)
        except NotInGitDir:
            sys.stderr.write(
                'Error: That commit does not exist'
                ' or we are not in a git directory.\n'
            )
            sys.exit(-1)
    else:
        # TODO handle error (invalid commit)
        # TODO handle error (non-existing commit)
        try:
            coach_files = get_modified_files()
        except NotInGitDir:
            sys.stderr.write('Error: Not in a git directory.\n')
            sys.exit(-1)

    all_suggested_files = []
    for coachfile in coach_files:
        if coachfile in counts.keys():
            file_commits = counts[coachfile]
            relevant_cors = c.find_relevant_correlations(
                cors, coachfile)
            normalized_cors = c.normalize_correlations(
                relevant_cors, file_commits)
            above_threshold = c.filter_threshold(normalized_cors, threshold)
            all_suggested_files.extend(
                (cor, suggested, coachfile)
                for (suggested, cor) in above_threshold.items()
            )
        else:
            sys.stdout.write('We have no data for {}\n'.format(coachfile))

    sys.stdout.write('\nHere are some files you might want to look at:\n')
    for cor, fname, suggestedby in sorted(all_suggested_files, reverse=True):
        sys.stdout.write(
            '{}\tsuggested by\t{} ({:2f})\n'.format(fname, suggestedby, cor)
        )


def get_modified_files():
    '''Ask git which files have uncommitted changes.'''
    command = "git ls-files --full-name --modified"
    try:
        with open('/dev/null', 'w') as stderr:
            file_list = subprocess.check_output(command.split(), stderr=stderr)
    except subprocess.CalledProcessError:
        raise NotInGitDir()
    return [f.decode() for f in file_list.splitlines()]


def get_commit_files(commit):
    '''Ask git which files were modified in a given commit.'''
    # TODO git2json shouldn't make me call this command manually
    command = "git log -1 --pretty=raw --numstat {}".format(commit)
    try:
        with open('/dev/null', 'w') as stderr:
            git_log_out = subprocess.check_output(
                command.split(),
                stderr=stderr) + '\n'
    except subprocess.CalledProcessError:
        raise NotInGitDir()
    from git2json import parse_commits
    commit = list(parse_commits(git_log_out))[0]
    return [change[2] for change in commit['changes']]


def get_coachfile_path():
    coaching_data_file = 'coaching-data.pickle'
    command = 'git rev-parse --git-dir'
    try:
        with open('/dev/null', 'w') as stderr:
            output = subprocess.check_output(command.split(), stderr=stderr)
            git_dir = output.decode().strip()
            return git_dir + '/' + coaching_data_file
    except subprocess.CalledProcessError:
        raise NotInGitDir()


class NotInGitDir(Exception):
    pass
