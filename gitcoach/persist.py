#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Code for persisting and loading training data.
'''

import sqlite3

TABLE_COINCIDENCE = '''CREATE TABLE IF NOT EXISTS coincidence
(f1 text, f2 text, commit_id text)'''

TABLE_COINCIDENCE_AGG = '''
CREATE TABLE IF NOT EXISTS coincidence_agg
(f1 text, f2 text, count int)'''


class TrainingDB(object):
    def __init__(self, path):
        self._path = path

    def connect(self):
        self._conn = sqlite3.connect(self._path)
        self._cursor = self._conn.cursor()

    def init_schema(self):
        '''Create the coincidence table if it doesn't exist.'''
        q = 'DROP TABLE IF EXISTS coincidence'
        self._cursor.execute(q)
        q = 'DROP TABLE IF EXISTS coincidence_agg'
        self._cursor.execute(q)
        self._cursor.execute(TABLE_COINCIDENCE)
        self._cursor.execute(TABLE_COINCIDENCE_AGG)

    def add_coincidence(self, f1, f2, commit):
        q = 'INSERT INTO coincidence VALUES (?, ?, ?)'
        self._cursor.execute(q, (f1, f2, commit))

    def create_agg_table(self):
        q = 'INSERT INTO coincidence_agg SELECT f1, f2, count(*) FROM coincidence GROUP BY f1, f2'
        self._cursor.execute(q)

    def schema_exists(self):
        try:
            q = 'SELECT 1 FROM coincidence'
            self._cursor.execute(q)
            q = 'SELECT 1 FROM coincidence_agg'
            self._cursor.execute(q)
            return True
        except sqlite3.OperationalError:
            return False

    def file_count(self, fname):
        q = 'SELECT count(distinct commit_id) FROM coincidence WHERE f1=? OR f2=?'
        result = self._cursor.execute(q, (fname, fname))
        row = result.fetchone()
        return row[0]

    def find_relevant_correlations(self, fname):
        q = 'SELECT f1, f2, count FROM coincidence_agg WHERE f1=? or f2=?'
        result = self._cursor.execute(q, (fname, fname))
        return {
            [k for k in [f1, f2] if k != fname][0]: count
            for f1, f2, count in result
        }
        return result.fetchall()

    def cleanup(self):
        self._conn.commit()
        self._conn.close()
