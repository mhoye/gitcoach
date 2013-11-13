#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Code for persisting and loading training data.
'''

import sqlite3

TABLE_COINCIDENCE = '''CREATE TABLE IF NOT EXISTS coincidence
(f1 text, f2 text, commit_id text)'''

# TABLE_COINCIDENCE_AGG = '''
# CREATE TABLE IF NOT EXISTS coincidence_agg
# (f1 text, f2 text, count int)'''


class TrainingDB(object):
    def __init__(self, path):
        self._path = path

    def connect(self):
        self._conn = sqlite3.connect(self._path)
        self._cursor = self._conn.cursor()

    def init_schema(self):
        '''Create the coincidence table if it doesn't exist.'''
        self._cursor.execute(TABLE_COINCIDENCE)

    def add_coincidence(self, f1, f2, commit):
        q = 'INSERT INTO coincidence VALUES (?, ?, ?)'
        self._cursor.execute(q, (f1, f2, commit))

    def cleanup(self):
        self._conn.commit()
        self._conn.close()
