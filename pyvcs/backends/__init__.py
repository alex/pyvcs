import sys

AVAILABLE_BACKENDS = {
    'bzr': 'bzr',
    'git': 'git',
    'hg': 'hg',
    'svn': 'subversion',
}

def get_backend(backend):
    if backend in AVAILABLE_BACKENDS:
        path = 'pyvcs.backends.%s' % AVAILABLE_BACKENDS[backend]
    else:
        path = backend
    __import__(path)
    return sys.modules[path]
