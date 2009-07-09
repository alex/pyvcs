#!/usr/bin/env python
from datetime import datetime
import unittest

from pyvcs.backends import get_backend
from pyvcs.exceptions import FileDoesNotExist, FolderDoesNotExist

class BzrTest(unittest.TestCase):
    def setUp(self):
        bzr = get_backend('bzr')
        self.repo = bzr.Repository('/home/andrew/junk/django/')

    def test_commits(self):
        commit = self.repo.get_commit_by_id('6460')
        self.assert_(commit.author.startswith('gwilson'))
        self.assertEqual(commit.time, datetime(2008, 12, 23, 18, 25, 24, 19000))
        self.assert_(commit.message.startswith('Fixed #8245 -- Added a LOADING flag'))
        self.assertEqual(commit.files, ['tests/regressiontests/bug8245', 'tests/regressiontests/bug8245/__init__.py', 'tests/regressiontests/bug8245/admin.py', 'tests/regressiontests/bug8245/models.py', 'tests/regressiontests/bug8245/tests.py', 'django/contrib/admin/__init__.py'])

    def test_recent_commits(self):
        results = self.repo.get_recent_commits()

    def test_list_directory(self):
        files, folders = self.repo.list_directory('tests/', '7254')
        self.assertEqual(files, ['runtests.py', 'urls.py'])
        self.assertEqual(folders, ['modeltests', 'regressiontests', 'templates'])
        self.assertRaises(FolderDoesNotExist, self.repo.list_directory, 'tests/awesometests/')

    def test_file_contents(self):
        contents = self.repo.file_contents('django/db/models/fields/related.py',
            '7254')
        self.assertEqual(contents.splitlines()[:2], [
            'from django.db import connection, transaction',
            'from django.db.backends import util'
        ])
        self.assertRaises(FileDoesNotExist, self.repo.file_contents, 'django/db/models/jesus.py')


if __name__ == '__main__':
    unittest.main()
