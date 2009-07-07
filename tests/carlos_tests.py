#!/usr/bin/env python
from datetime import datetime
import unittest

from pyvcs.backends import get_backend
from pyvcs.exceptions import FileDoesNotExist, FolderDoesNotExist


class SVNTest(unittest.TestCase):
    def setUp(self):
        svn = get_backend('svn')
        self.repo = svn.Repository('/home/clsdaniel/Development/django')
        
    def test_commits(self):
        commit = self.repo.get_commit_by_id(11127)
        self.assert_(commit.author.startswith('ubernostrum'))
        self.assertEqual(commit.time, datetime(2009, 6, 30, 11, 40, 29, 647241))
        self.assert_(commit.message.startswith('Fixed #11357: contrib.admindocs'))
        self.assertEqual(commit.files, ['/django/trunk/django/contrib/admindocs/views.py'])
        
    def test_recent_commits(self):
        results = self.repo.get_recent_commits()

    def test_list_directory(self):
        files, folders = self.repo.list_directory('tests/', 11127)
        self.assertEqual(files, ['runtests.py', 'urls.py'])
        self.assertEqual(folders, ['modeltests', 'regressiontests', 'templates'])
        self.assertRaises(FolderDoesNotExist, self.repo.list_directory, 'tests/awesometests/')

    def test_file_contents(self):
        contents = self.repo.file_contents('django/db/models/fields/related.py', 11127)
        self.assertEqual(contents.splitlines()[:2], [
            'from django.db import connection, transaction',
            'from django.db.backends import util'
        ])
        self.assertRaises(FileDoesNotExist, self.repo.file_contents, 'django/db/models/jesus.py')

if __name__ == '__main__':
    unittest.main()
