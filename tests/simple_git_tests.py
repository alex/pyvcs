#!/usr/bin/env python
from datetime import datetime
import unittest
import os
import subprocess

from pyvcs.backends import get_backend
from pyvcs.exceptions import FileDoesNotExist, FolderDoesNotExist, CommitDoesNotExist

class GitSimpleTest(unittest.TestCase):

    def setUp(self):
        git = get_backend('git')
        ret = subprocess.call('./setup_git_test.sh')
        self.repo = git.Repository('/tmp/pyvcs-test/git-test/')

    def tearDown(self):
        ret = subprocess.call('./teardown_git_test.sh')

    def test_recent_commits(self):
        recent_commits = self.repo.get_recent_commits()
        self.assertEqual(len(recent_commits),2)

    def test_commits(self):
        recent_commits = self.repo.get_recent_commits()
        commit = self.repo.get_commit_by_id(recent_commits[1].commit_id)
        self.assert_(commit.message.startswith('initial add of files'))
        self.assertEqual(commit.time.date(), datetime.today().date())
        self.assertEqual(commit.files, ['README', 'hello_world.py'])
        self.assert_('this is a test README file for a mock project' in commit.diff)
        self.assertRaises(CommitDoesNotExist,self.repo.get_commit_by_id,'crap')

    def test_list_directory(self):
        files, folders = self.repo.list_directory('')
        self.assertEqual(files, ['README', 'hello_world.py'])
        self.assertEqual(folders, [])
        self.assertRaises(FolderDoesNotExist, self.repo.list_directory, 'tests/awesometests/')

    def test_file_contents(self):
        contents = self.repo.file_contents('hello_world.py')
        self.assertEqual(contents,'print hello, world!\n')
        self.assertRaises(FileDoesNotExist, self.repo.file_contents, 'waybettertest.py')

    def test_diffs(self):
        recent_commits = self.repo.get_recent_commits()
        self.assertEqual(self.repo._diff_files(recent_commits[0].commit_id,recent_commits[1].commit_id),['README'])


if __name__ == '__main__':
    unittest.main()
