

class BaseRepository(object):
    def __init__(self, path, **kwargs):
        """
        path is the filesystem path where the repo exists, **kwargs are
        anything extra for accessing the repo
        """
        self.path = path
        self.extra = kwargs

    def get_commit_by_id(self, commit_id):
        """
        Returns a commit by it's id (nature of the ID is VCS dependent).
        """
        raise NotImplementedError

    def get_recent_commits(self, since=None):
        """
        Returns all commits since since.  If since is None returns all commits
        from the last 5 days.
        """
        raise NotImplementedError

    def list_directory(self, path, revision=None):
        """
        Returns a tuple of lists of files and folders in a given directory at a
        given revision, or HEAD if revision is None.
        """
        raise NotImplementedError

    def file_contents(self, path, revision=None):
        """
        Returns the contents of a file as a string at a given revision, or
        HEAD if revision is None.
        """
        raise NotImplementedError
