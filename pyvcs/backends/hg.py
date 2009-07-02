from mercurial import ui
from mercurial.localrepo import localrepository as hg_repo
from pyvcs import repository
from pyvcs.commit import Commit
from pyvcs.exceptions import CommitDoesNotExist
from datetime import datetime
from difflib import ndiff


def get_diff(chgset):
    diff = []
    for i in chgset.files():
        fctx = chgset.filectx(i)
        # FIXME: Fix this to handle multiple parents
        parent = fctx.parents()[0]
        # FIXME: This should return diff + context, not entire files
        diff.append(ndiff(fctx.data().splitlines(1), parent.data().splitlines(1)))
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
        changeset = self.repo.changectx(commit_id).changeset()
        commit = Commit(changeset.user(),
                        datetime.fromtimestamp(changeset.date()[0]), 
                        changeset.description(),
                        "\n".join(get_diff(changeset)))
        return commit

    def get_recent_commits(self, since=None):
        """
        Returns all commits since since.  If since is None returns all commits
        from the last 5 days.
        """
        raise NotImplementedError

    def list_directory(self, revision=None):
        """
        Returns a list of files in a directory (list of strings) at a given
        revision, or HEAD if revision is None.
        """
        raise NotImplementedError

    def file_contents(self, revision=None):
        """
        Returns the contents of a file as a string at a given revision, or
        HEAD if revision is None.
        """
        raise NotImplementedError
