from datetime import datetime
from operator import itemgetter
import os

from dulwich.repo import Repo
from dulwich import objects

from pyvcs.commit import Commit
from pyvcs.exceptions import CommitDoesNotExist, FileDoesNotExist, FolderDoesNotExist
from pyvcs.repository import BaseRepository

def get_differing_files(repo, past, current):
    iterator = zip(
        sorted(past.entries(), key=itemgetter(1)),
        sorted(current.entries(), key=itemgetter(1))
    )
    for (past_mode, past_name, past_sha), (current_mode, current_name, current_sha) in iterator:
        if past_name == current_name and past_sha != current_sha:
            if isinstance(repo.get_object(past_sha), objects.Tree):
                for name in get_differing_files(repo, repo.get_object(past_sha), repo.get_object(current_sha)):
                    yield os.path.join(current_name, name)
            else:
                yield current_name

class Repository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(Repository, self).__init__(*args, **kwargs)

        self._repo = Repo(self.path)

    def _get_commit(self, commit_id):
        try:
            return self._repo.commit(commit_id)
        except Exception, e:
            raise CommitDoesNotExist("%s is not a commit" % commit_id)

    def _get_obj(self, sha):
        return self._repo.get_object(sha)

    def _diff(self, commit_id1, commit_id2):
        return list(get_differing_files(
            self._repo,
            self._get_obj(self._get_obj(commit_id1).tree),
            self._get_obj(self._get_obj(commit_id2).tree),
        ))

    def get_commit_by_id(self, commit_id):
        commit = self._get_commit(commit_id)
        return Commit(commit.committer,
            datetime.fromtimestamp(commit.commit_time), commit.message)

    def get_recent_commits(self, since=None):
        raise NotImplementedError

    def list_directory(self, path, revision=None):
        commit = self._get_commit(revision)
        tree = self._repo.tree(commit.tree)
        path = path.split(os.path.sep)
        while path:
            part = path.pop(0)
            for mode, name, hexsha in self._repo.tree(tree.id).entries():
                if part == name:
                    tree = self._repo.tree(hexsha)
                    break
        files, folders = [], []
        for mode, name, hexsha in tree.entries():
            if isinstance(self._repo.get_object(hexsha), objects.Tree):
                folders.append(name)
            elif isinstance(self._repo.get_object(hexsha), objects.Blob):
                files.append(name)
        return files, folders

    def file_contents(self, path, revision=None):
        commit = self._get_commit(revision)
        tree = self._repo.tree(commit.tree)
        path = path.split(os.path.sep)
        path, filename = path[:-1], path[-1]
        while path:
            part = path.pop(0)
            for mode, name, hexsha in self._repo.tree(tree.id).entries():
                if part == name:
                    tree = self._repo.tree(hexsha)
                    break
        for mode, name, hexsha in tree.entries():
            if name == filename:
                return self._repo.get_object(hexsha).as_pretty_string()
        raise FileDoesNotExist
