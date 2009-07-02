from dulwich.repo import Repo

from pyvcs.exceptions import CommitDoesNotExist
from pyvcs.commit import Commit

class Repository(object):
    def __init__(self, *args, **kwargs):
        super(Repository, self).__init__(*args, **kwargs)

        self._repo = Repo(self.path)

    def get_commit_by_id(self, commit_id):
        try:
            commit = self._repo.commit(commit_id)
        except Exception, e:
            raise CommitDoesNotExist("%s is not a commit" % commit_id)
        return Commit(commit.committer, commit.time, commit.message,
            commit.as_pretty_string)
