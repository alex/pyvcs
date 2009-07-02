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


if __name__ == '__main__':
    unittest.main()
