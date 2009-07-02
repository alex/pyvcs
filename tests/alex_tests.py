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
            'django/trunk/AUTHORS',
            'django/trunk/django/contrib/gis/db/models/aggregates.py',
            'django/trunk/django/contrib/gis/db/models/query.py',
            'django/trunk/django/contrib/gis/db/models/sql/aggregates.py',
            'django/trunk/django/contrib/gis/db/models/sql/query.py',
            'django/trunk/django/db/backends/__init__.py',
            'django/trunk/django/db/backends/mysql/base.py',
            'django/trunk/django/db/backends/oracle/query.py',
            'django/trunk/django/db/backends/sqlite3/base.py',
            'django/trunk/django/db/models/aggregates.py',
            'django/trunk/django/db/models/__init__.py',
            'django/trunk/django/db/models/manager.py',
            'django/trunk/django/db/models/query.py',
            'django/trunk/django/db/models/query_utils.py',
            'django/trunk/django/db/models/sql/aggregates.py',
            'django/trunk/django/db/models/sql/datastructures.py',
            'django/trunk/django/db/models/sql/query.py',
            'django/trunk/django/db/models/sql/subqueries.py',
            'django/trunk/django/test/testcases.py',
            'django/trunk/docs/index.txt',
            'django/trunk/docs/ref/models/index.txt',
            'django/trunk/docs/ref/models/querysets.txt',
            'django/trunk/docs/topics/db/aggregation.txt',
            'django/trunk/docs/topics/db/index.txt',
            'django/trunk/tests/modeltests/aggregation',
            'django/trunk/tests/modeltests/aggregation/fixtures',
            'django/trunk/tests/modeltests/aggregation/fixtures/initial_data.json',
            'django/trunk/tests/modeltests/aggregation/__init__.py',
            'django/trunk/tests/modeltests/aggregation/models.py',
            'django/trunk/tests/regressiontests/aggregation_regress',
            'django/trunk/tests/regressiontests/aggregation_regress/fixtures',
            'django/trunk/tests/regressiontests/aggregation_regress/fixtures/initial_data.json',
            'django/trunk/tests/regressiontests/aggregation_regress/__init__.py',
            'django/trunk/tests/regressiontests/aggregation_regress/models.py'
        ]
        self.assertEqual(set(self.repo._diff(
            '842e1d0dabfe057c1eeb4b6b83de0b2eb7dcb9e6',
            'a6195888efe947f7b23c61248f43f4cab3c5200c',
        )), set(files))

if __name__ == '__main__':
    unittest.main()
