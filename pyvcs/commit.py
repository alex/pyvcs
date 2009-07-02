class Commit(object):
    def __init__(self, commit_id, author, time, message, files, diff):
        """
        comimt_id should be a string, author a string, time a datetime object,
        message a string, files a list of filenames (strings), and diff a
        string
        """
        self.commit_id = commit_id
        self.author = author
        self.time = time
        self.message = message
        self.files = files
        self.diff = diff

    def __str__(self):
        return "<Commit %s by %s on %s>" % (self.commit_id, self.author, self.time)

    __repr__ = __str__
