from datetime import datetime
import os

from dulwich.repo import Repo
from dulwich import objects

from pyvcs.commit import Commit
from pyvcs.exceptions import CommitDoesNotExist
from pyvcs.repository import BaseRepository

class Repository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(Repository, self).__init__(*args, **kwargs)

        self._repo = Repo(self.path)

    def _get_commit(self, commit_id):
        try:
            return self._repo.commit(commit_id)
        except Exception, e:
            raise CommitDoesNotExist("%s is not a commit" % commit_id)


    def get_commit_by_id(self, commit_id):
        commit = self._get_commit(commit_id)
        return Commit(commit.committer,
            datetime.fromtimestamp(commit.commit_time), commit.message,
            commit.as_pretty_string())

    def get_recent_commits(self, since=None):
        raise NotImplementedError

    def list_directory(self, path, revision=None):
        commit = self._get_commit(revision)
        tree = self._repo.tree(commit.tree)
        path = path.lstrip(self.path).split(os.path.sep)
        while path:
            part = path.pop(0)
            for mode, name, hexsha in self._repo.tree(tree.id).entries():
                if part == name:
                    tree = self._repo.tree(hexsha)
                    break
        files, folders = [], []
        for mode, name, hexsha in self._repo.tree(tree.id).entries():
            if isinstance(self._repo.get_object(hexsha), objects.Tree):
                folders.append(name)
            elif isinstance(self._repo.get_object(hexsha), objects.Blob):
                files.append(name)
        return files, folders

    def file_contents(self, path, revision=None):
        raise NotImplementedError
