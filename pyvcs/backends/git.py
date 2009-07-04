from datetime import datetime, timedelta
from operator import itemgetter, attrgetter
import os

from dulwich.repo import Repo
from dulwich import objects

from pyvcs.commit import Commit
from pyvcs.exceptions import CommitDoesNotExist, FileDoesNotExist, FolderDoesNotExist
from pyvcs.repository import BaseRepository
from pyvcs.utils import generate_unified_diff


def traverse_tree(repo, tree):
    for mode, name, sha in tree.entries():
        if isinstance(repo.get_object(sha), objects.Tree):
            for item in traverse_tree(repo, repo.get_object(sha)):
                yield os.path.join(name, item)
        else:
            yield name

def get_differing_files(repo, past, current):
    past_files = {}
    current_files = {}
    if past is not None:
        past_files = dict([(name, sha) for mode, name, sha in past.entries()])
    if current is not None:
        current_files = dict([(name, sha) for mode, name, sha in current.entries()])

    added = set(current_files) - set(past_files)
    removed = set(past_files) - set(current_files)
    changed = [o for o in past_files if o in current_files and past_files[o] != current_files[o]]

    for name in added:
        sha = current_files[name]
        yield name
        if isinstance(repo.get_object(sha), objects.Tree):
            for item in get_differing_files(repo, None, repo.get_object(sha)):
                yield os.path.join(name, item)

    for name in removed:
        sha = past_files[name]
        yield name
        if isinstance(repo.get_object(sha), objects.Tree):
            for item in get_differing_files(repo, repo.get_object(sha), None):
                yield os.path.join(name, item)

    for name in changed:
        past_sha = past_files[name]
        current_sha = current_files[name]
        if isinstance(repo.get_object(past_sha), objects.Tree):
            for item in get_differing_files(repo, repo.get_object(past_sha), repo.get_object(current_sha)):
                yield os.path.join(name, item)
        else:
            yield name


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

    def _diff_files(self, commit_id1, commit_id2):
        return sorted(get_differing_files(
            self._repo,
            self._get_obj(self._get_obj(commit_id1).tree),
            self._get_obj(self._get_obj(commit_id2).tree),
        ))

    def get_commit_by_id(self, commit_id):
        commit = self._get_commit(commit_id)
        files = self._diff_files(commit.id, commit.parents[0])
        return Commit(commit.id, commit.committer,
            datetime.fromtimestamp(commit.commit_time), commit.message, files,
            generate_unified_diff(self, files, commit.parents[0], commit.id))

    def get_recent_commits(self, since=None):
        if since is None:
            since = datetime.now() - timedelta(days=5)
        pending_commits = self._repo.get_refs().values()#[self._repo.head()]
        history = {}
        while pending_commits:
            head = pending_commits.pop(0)
            try:
                commit = self._repo.commit(head)
            except KeyError:
                raise CommitDoesNotExist
            if commit.id in history or datetime.fromtimestamp(commit.commit_time) <= since:
                continue
            history[commit.id] = commit
            pending_commits.extend(commit.parents)
        commits = filter(lambda o: datetime.fromtimestamp(o.commit_time) >= since, history.values())
        commits = map(lambda o: self.get_commit_by_id(o.id), commits)
        return sorted(commits, key=attrgetter('time'), reverse=True)

    def list_directory(self, path, revision=None):
        commit = self._get_commit(revision or self._repo.head())
        tree = self._repo.tree(commit.tree)
        path = filter(bool, path.split(os.path.sep))
        while path:
            part = path.pop(0)
            found = False
            for mode, name, hexsha in self._repo.tree(tree.id).entries():
                if part == name:
                    found = True
                    tree = self._repo.tree(hexsha)
                    break
            if not found:
                raise FolderDoesNotExist
        files, folders = [], []
        for mode, name, hexsha in tree.entries():
            if isinstance(self._repo.get_object(hexsha), objects.Tree):
                folders.append(name)
            elif isinstance(self._repo.get_object(hexsha), objects.Blob):
                files.append(name)
        return files, folders

    def file_contents(self, path, revision=None):
        commit = self._get_commit(revision or self._repo.head())
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
