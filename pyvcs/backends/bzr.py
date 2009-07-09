from datetime import datetime, timedelta
from time import mktime
import os, sys
import StringIO

from bzrlib import branch, diff, errors

from pyvcs.commit import Commit
from pyvcs.exceptions import CommitDoesNotExist, FileDoesNotExist, FolderDoesNotExist
from pyvcs.repository import BaseRepository

class Repository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(Repository, self).__init__(*args, **kwargs)

        self._branch = branch.Branch.open(self.path.rstrip(os.path.sep))

    def _rev_to_commit(self, rev):
        # this doesn't yet handle the case of multiple parent revisions
        current = self._branch.repository.revision_tree(rev.revision_id)
        prev = self._branch.repository.revision_tree(rev.parent_ids[0])
        
        delta = current.changes_from(prev)
        files = [f[0] for f in delta.added + delta.removed + delta.renamed + delta.kind_changed + delta.modified]
        
        diff_file = StringIO.StringIO()
        diff_tree = diff.DiffTree(prev, current, diff_file)
        
        self._branch.lock_read()
        diff_tree.show_diff('')
        self._branch.unlock()
        
        diff_out = diff_file.getvalue()
        diff_file.close()
        
        return Commit(self._get_commit_id(rev.revision_id), rev.committer, datetime.fromtimestamp(rev.timestamp), rev.message, files, diff_out)

    def _get_rev_id(self, commit_id):
        return self._branch.get_rev_id(int(commit_id))
    
    def _get_commit_id(self, rev_id):
        return self._branch.revision_id_to_revno(rev_id)
    
    def _get_commit_by_rev_id(self, rev_id):
        rev = self._branch.repository.get_revision(rev_id)
        return self._rev_to_commit(rev)
    
    def get_commit_by_id(self, commit_id):
        rev_id = self._get_rev_id(commit_id)
        return self._get_commit_by_rev_id(rev_id)

    def get_recent_commits(self, since=None):
        if since is None:
            since = datetime.now() - timedelta(days=5)
        
        since_ts = mktime(since.timetuple())
        
        commits = []
        hist = self._branch.revision_history()
        hist.reverse()
        for rev_id in hist:
            rev = self._branch.repository.get_revision(rev_id)
            if rev.timestamp < since_ts:
                break
            commits.append(self._rev_to_commit(rev))
        
        return commits

    def list_directory(self, path, revision=None):
        path = path.rstrip(os.path.sep)
        
        tree = self._get_tree(revision)
        
        iter = tree.walkdirs(path)
        try:
            entries = iter.next()
        except StopIteration:
            raise FolderDoesNotExist
        
        plen = len(path)
        if plen != 0:
        	plen += 1
        files = [f[0][plen:] for f in filter(lambda x: x[2] == 'file', entries[1])]
        folders = [f[0][plen:] for f in filter(lambda x: x[2] == 'directory', entries[1])]

        return files, folders

    def _get_tree(self, revision=None):
        if revision:
            return self._branch.repository.revision_tree(self._get_rev_id(revision))
        else:
            return self._branch.repository.revision_tree(self._branch.last_revision())
    
    def file_contents(self, path, revision=None):
        tree = self._get_tree(revision)
        
        try:
            self._branch.lock_read()
            file_id = tree.path2id(path)
            if tree.kind(file_id) != 'file':
            	raise FileDoesNotExist
            out = tree.get_file(file_id).read()
            self._branch.unlock()
        except:
            raise FileDoesNotExist
        
        return out
