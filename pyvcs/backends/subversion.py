from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from time import mktime
import os

import pysvn

from pyvcs.commit import Commit
from pyvcs.exceptions import CommitDoesNotExist, FileDoesNotExist, FolderDoesNotExist
from pyvcs.repository import BaseRepository
from pyvcs.utils import generate_unified_diff

class Repository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(Repository, self).__init__(*args, **kwargs)

        self._repo = pysvn.Client(self.path.rstrip(os.path.sep))

    def _log_to_commit(self, log):
        info = self._repo.info(self.path)
        base, url = info['repos'], info['url']
        at = url[len(base):]
        commit_files = [cp_dict['path'][len(at)+1:] for cp_dict in log['changed_paths']]

        def get_diff():
            # Here we go back through history, 5 commits at a time, searching
            # for the first point at which there is a change along our path.
            oldrev_log = None
            i = 1
            # the start of our search is always at the previous commit
            while oldrev_log is None:
                i += 5
                diff_rev_start = pysvn.Revision(pysvn.opt_revision_kind.number,
                    log['revision'].number - (i - 5))
                diff_rev_end = pysvn.Revision(pysvn.opt_revision_kind.number,
                    log['revision'].number - i)
                log_list = self._repo.log(self.path,
                    revision_start=diff_rev_start, revision_end=diff_rev_end,
                    discover_changed_paths=True)
                try:
                    oldrev_log = log_list.pop(0)
                except IndexError:
                    # If we've gone back through the entirety of history and
                    # still not found anything, bail out, this commit doesn't
                    # exist along our path (or perhaps at all)
                    if i >= log['revision'].number:
                        raise CommitDoesNotExist

            diff = self._repo.diff(NamedTemporaryFile().name,
                url_or_path=self.path, revision1=oldrev_log['revision'],
                revision2=log['revision'],
            )
            return diff

        return Commit(log['revision'].number, log['author'],
            datetime.fromtimestamp(log['date']), log['message'],
            commit_files, get_diff)

    def get_commit_by_id(self, commit_id):
        rev = pysvn.Revision(pysvn.opt_revision_kind.number, commit_id)

        try:
            log_list = self._repo.log(self.path, revision_start=rev,
                revision_end=rev, discover_changed_paths=True)
        except pysvn.ClientError:
            raise CommitDoesNotExist

        # If log list is empty most probably the commit does not exists for a
        # given path or branch.
        try:
            log = log_list.pop(0)
        except IndexError:
            raise CommitDoesNotExist

        return self._log_to_commit(log)


    def get_recent_commits(self, since=None):
        if since is None:
            since = datetime.now() - timedelta(days=5)

        revhead = pysvn.Revision(pysvn.opt_revision_kind.head)

        # Convert from datetime to float (seconds since unix epoch)
        utime = mktime(since.timetuple())

        rev = pysvn.Revision(pysvn.opt_revision_kind.date, utime)

        log_list = self._repo.log(self.path, revision_start=revhead,
            revision_end=rev, discover_changed_paths=True)

        commits = [self._log_to_commit(log) for log in log_list]
        return commits

    def list_directory(self, path, revision=None):
        if revision:
            rev = pysvn.Revision(pysvn.opt_revision_kind.number, revision)
        else:
            rev = pysvn.Revision(pysvn.opt_revision_kind.head)

        dir_path = os.path.join(self.path, path)

        try:
            entries = self._repo.list(dir_path, revision=rev, recurse=False)
        except pysvn.ClientError:
            raise FolderDoesNotExist

        files, folders = [], []
        for file_info, file_pops in entries:
            if file_info['kind'] == pysvn.node_kind.dir:
                # TODO: Path is not always present, only repos_path
                # is guaranteed, in case of looking at a remote
                # repository (with no local working copy) we should
                # check against repos_path.
                if not dir_path.startswith(file_info['path']):
                    folders.append(os.path.basename(file_info['repos_path']))
            else:
                files.append(os.path.basename(file_info['repos_path']))

        return files, folders

    def file_contents(self, path, revision=None):
        if revision:
            rev = pysvn.Revision(pysvn.opt_revision_kind.number, revision)
        else:
            rev = pysvn.Revision(pysvn.opt_revision_kind.head)

        file_path = os.path.join(self.path, path)

        try:
            return self._repo.cat(file_path, rev)
        except pysvn.ClientError:
            raise FileDoesNotExist
