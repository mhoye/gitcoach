#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_gitcoach
----------------------------------

Tests for `gitcoach` module.
"""

from nose.tools import eq_
from gitcoach import learn


def test_find_correlations():
    input = [
        ['f1', 'f2', 'f3', 'f4'],
        ['f2', 'f3', 'f4'],
        ['f2', 'f4'],
        ['f2', 'f6'],
        ['f4', 'f6'],
    ]
    result = learn.find_correlations(input)
    expected_result = {
        ('f1', 'f2'): 1,
        ('f1', 'f3'): 1,
        ('f1', 'f4'): 1,
        ('f2', 'f3'): 2,
        ('f3', 'f4'): 2,
        ('f2', 'f4'): 3,
        ('f2', 'f6'): 1,
        ('f4', 'f6'): 1,
    }
    eq_(result, expected_result)


def test_find_counts():
    input = [
        ['f1', 'f2', 'f3', 'f4'],
        ['f2', 'f3', 'f4'],
        ['f2', 'f4'],
        ['f2', 'f6'],
        ['f4', 'f6'],
    ]
    expected_result = {
        'f1': 1,
        'f2': 4,
        'f3': 2,
        'f4': 4,
        'f6': 2,
    }
    result = learn.find_counts(input)
    eq_(result, expected_result)
