

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
