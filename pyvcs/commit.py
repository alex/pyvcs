class Commit(object):
    def __init__(self, author, time, message, diff):
        self.author = author
        self.time = time
        self.message = message
        self.diff = diff
