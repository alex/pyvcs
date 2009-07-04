#!/usr/bin/env python
from datetime import datetime
import unittest

from pyvcs.backends import get_backend
from pyvcs.exceptions import FileDoesNotExist, FolderDoesNotExist


class HGTest(unittest.TestCase):
    def setUp(self):
        hg = get_backend('hg')
        self.repo = hg.Repository('/home/jlilly/Code/python/pyvcs/src/mercurial')
        
    def test_commits(self):
        commit = self.repo.get_commit_by_id(45)
        self.assert_(commit.author.startswith('mpm'))
        self.assertEqual(commit.time, datetime(2005, 5, 10, 4, 34, 57))
        self.assert_(commit.message.startswith('Fix recursion depth'))
        
    def test_recent_commits(self):
        results = self.repo.get_recent_commits()
        
    def test_list_directory(self):
        files, folders = self.repo.list_directory('contrib/', 450)
        self.assertEqual(len(files), 3)
        self.assertEqual(folders, ['git-viz'])
        
    def test_file_contents(self):
        contents = self.repo.file_contents('tests/test-up-local-change', 450)
        self.assertEqual(contents.splitlines()[:1], ['#!/bin/bash'])

if __name__ == '__main__':
    unittest.main()
