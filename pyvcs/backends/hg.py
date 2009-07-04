from datetime import datetime, timedelta
from difflib import unified_diff

from mercurial import ui
from mercurial.localrepo import localrepository as hg_repo
from mercurial.util import matchdate

from pyvcs.commit import Commit
from pyvcs.exceptions import CommitDoesNotExist, FileDoesNotExist
from pyvcs.repository import BaseRepository
from pyvcs.utils import generate_unified_diff

class Repository(BaseRepository):
    def __init__(self, path, **kwargs):
        """
        path is the filesystem path where the repo exists, **kwargs are
        anything extra fnor accessing the repo
        """
        self.repo = hg_repo(ui.ui(), path=path)
        self.path = path
        self.extra = kwargs

    def _ctx_to_commit(self, ctx):
        diff = generate_unified_diff(self, ctx.files(), ctx.parents()[0].rev(), ctx.rev())
        
        return Commit(ctx.rev(),
                      ctx.user(),
                      datetime.fromtimestamp(ctx.date()[0]),
                      ctx.description(),
                      ctx.files(),
                      diff)

    def _latest_from_parents(self, parent_list):
        pass

    def get_commit_by_id(self, commit_id):
        """
        Returns a commit by it's id (nature of the ID is VCS dependent).
        """
        changeset = self.repo.changectx(commit_id)
        return self._ctx_to_commit(changeset)

    def get_recent_commits(self, since=None):
        """
        Returns all commits since since.  If since is None returns all commits
        from the last 5 days.
        """
        if since is None:
            since = datetime.now() - timedelta(5)

        cur_ctx = self.repo.changectx(self.repo.changelog.rev(self.repo.changelog.tip()))

        changesets = []
        to_look_at = [cur_ctx]

        while to_look_at:
            head = to_look_at.pop(0)
            to_look_at.extend(head.parents())
            if datetime.fromtimestamp(head.date()[0]) >= since:
                changesets.append(head)
            else:
                break

        return [self._ctx_to_commit(ctx) for ctx in changesets] or None

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
