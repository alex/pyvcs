#!/usr/bin/env python
from datetime import datetime
import unittest

from pyvcs.backends import get_backend
from pyvcs.exceptions import FileDoesNotExist, FolderDoesNotExist

class GitTest(unittest.TestCase):
    def setUp(self):
        git = get_backend('git')
        self.repo = git.Repository('/home/alex/django_src/')

#    def test_commits(self):
#        commit = self.repo.get_commit_by_id('c3699190186561d5c216b2a77ecbfc487d42a734')
#        self.assert_(commit.author.startswith('ubernostrum'))
#        self.assertEqual(commit.time, datetime(2009, 6, 30, 13, 40, 29))
#        self.assert_(commit.message.startswith('Fixed #11357: contrib.admindocs'))

    def test_list_directory(self):
        files, folders = self.repo.list_directory('tests/', 'c3699190186561d5c216b2a77ecbfc487d42a734')
        self.assertEqual(files, ['runtests.py', 'urls.py'])
        self.assertEqual(folders, ['modeltests', 'regressiontests', 'templates'])

    def test_file_contents(self):
        contents = self.repo.file_contents('django/db/models/fields/related.py',
            'c3699190186561d5c216b2a77ecbfc487d42a734')
        self.assertEqual(contents.splitlines()[:2], [
            'from django.db import connection, transaction',
            'from django.db.backends import util'
        ])

    def test_diffs(self):
        self.assertEqual(self.repo._diff(
            '35fa967a05d54d5159eb1c620544e050114ab0ed',
            'c3699190186561d5c216b2a77ecbfc487d42a734'
        ), ['django/contrib/admindocs/views.py'])
        files = [
            'AUTHORS',
            'django/contrib/gis/db/models/aggregates.py',
            'django/contrib/gis/db/models/query.py',
            'django/contrib/gis/db/models/sql/aggregates.py',
            'django/contrib/gis/db/models/sql/query.py',
            'django/db/backends/__init__.py',
            'django/db/backends/mysql/base.py',
            'django/db/backends/oracle/query.py',
            'django/db/backends/sqlite3/base.py',
            'django/db/models/aggregates.py',
            'django/db/models/__init__.py',
            'django/db/models/manager.py',
            'django/db/models/query.py',
            'django/db/models/query_utils.py',
            'django/db/models/sql/aggregates.py',
            'django/db/models/sql/datastructures.py',
            'django/db/models/sql/query.py',
            'django/db/models/sql/subqueries.py',
            'django/test/testcases.py',
            'docs/index.txt',
            'docs/ref/models/index.txt',
            'docs/ref/models/querysets.txt',
            'docs/topics/db/aggregation.txt',
            'docs/topics/db/index.txt',
            'tests/modeltests/aggregation',
            'tests/modeltests/aggregation/fixtures',
            'tests/modeltests/aggregation/fixtures/initial_data.json',
            'tests/modeltests/aggregation/__init__.py',
            'tests/modeltests/aggregation/models.py',
            'tests/regressiontests/aggregation_regress',
            'tests/regressiontests/aggregation_regress/fixtures',
            'tests/regressiontests/aggregation_regress/fixtures/initial_data.json',
            'tests/regressiontests/aggregation_regress/__init__.py',
            'tests/regressiontests/aggregation_regress/models.py'
        ]
        self.assertEqual(set(self.repo._diff(
            '842e1d0dabfe057c1eeb4b6b83de0b2eb7dcb9e6',
            'a6195888efe947f7b23c61248f43f4cab3c5200c',
        )), set(files))


if __name__ == '__main__':
    unittest.main()
