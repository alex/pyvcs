#!/usr/bin/env python
from datetime import datetime
import unittest

from pyvcs.backends import get_backend

class GitTest(unittest.TestCase):
    def test_commits(self):
        git = get_backend('git')
        repo = git.Repository('/home/alex/django_src/')
        commit = repo.get_commit_by_id('c3699190186561d5c216b2a77ecbfc487d42a734')
        self.assert_(commit.author.startswith('ubernostrum'))
        self.assertEqual(commit.time, datetime(2009, 6, 30, 13, 40, 29))
        self.assert_(commit.message.startswith('Fixed #11357: contrib.admindocs'))


if __name__ == '__main__':
    unittest.main()
