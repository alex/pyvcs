import sys

BACKENDS = {
    'bzr': 'bzr',
    'git': 'git',
    'hg': 'hg',
    'svn': 'svn',
}

def get_backend(backend):
    if backend in BACKENDS:
        path = 'pyvcs.backends.%s' % backend
    else:
        path = backend
    __import__(path)
    return sys.modules[path]
