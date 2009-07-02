from datetime import datetime
from difflib import Differ

from mercurial import ui
from mercurial.localrepo import localrepository as hg_repo

from pyvcs.commit import Commit
from pyvcs.repository import BaseRepository
from pyvcs.exceptions import CommitDoesNotExist, FileDoesNotExist

def get_diff(chgset):
    diff = []
    for i in chgset.files():
        fctx = chgset.filectx(i)
        # FIXME: Fix this to handle multiple parents
        parent = fctx.parents()[0]
        # FIXME: This should return diff + context, not entire files
        differ = Differ()
        single_diff = list(differ.compare(fctx.data().splitlines(1), parent.data().splitlines(1)))
        diff.append(''.join(single_diff)) 
    return diff

class Repository(BaseRepository):
    def __init__(self, path, **kwargs):
        """
        path is the filesystem path where the repo exists, **kwargs are
        anything extra fnor accessing the repo
        """
        self.repo = hg_repo(ui.ui(), path=path)
        self.path = path
        self.extra = kwargs

    def get_commit_by_id(self, commit_id):
        """
        Returns a commit by it's id (nature of the ID is VCS dependent).
        """
        changeset = self.repo.changectx(commit_id)
        commit = Commit(changeset.user(),
                        datetime.fromtimestamp(changeset.date()[0]),
                        changeset.description(),
                        changeset.files(),
                        "\n".join(get_diff(changeset)))
        return commit

    def get_recent_commits(self, since=None):
        """
        Returns all commits since since.  If since is None returns all commits
        from the last 5 days.
        """
        raise NotImplementedError

    def list_directory(self, path, revision=None):
        """
        Returns a list of files in a directory (list of strings) at a given
        revision, or HEAD if revision is None.
        """
        chgctx = self.repo.changectx(revision)
        file_list = []
        folder_list = []
        for file, node in chgctx.manifest().items():
            if not file.startswith(path):
                continue
            folder_name = '/'.join(file.lstrip(path).split('/')[:-1])
            if folder_name != '':
                if folder_name not in folder_list:
                    folder_list.append(folder_name)
            if '/' not in file.lstrip(path):
                file_list.append(file)
        return file_list, folder_list

    def file_contents(self, path, revision=None):
        """
        Returns the contents of a file as a string at a given revision, or
        HEAD if revision is None.
        """
        chgctx = self.repo.changectx(revision)
        try:
            fctx = chgctx.filectx(path)
        except KeyError:
            raise FileDoesNotExist
        return fctx.data()
