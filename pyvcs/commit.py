class Commit(object):
    def __init__(self, author, time, message, files, diff):
        """
        author should be a string, time a datetime object, message a string,
        files a list of filenames (strings), and diff a string
        """
        self.author = author
        self.time = time
        self.message = message
        self.diff = diff
