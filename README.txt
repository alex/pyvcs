pyvcs - A minimal VCS abstraction layer for Python
==================================================

pyvcs is a minimal VCS abstraction layer for Python.  It's goals are to provide
as much functionality as is necessary, and no further.  It doesn't try to
abstract every layer or feature of a VCS, just what's necessary to build a code
browsing UI.

Currently supported VCS backends are::

    * Mercurial
    * Git
    * Subversion
    * Bazaar

Requirements::

    * Python (2.4 or greater)

Backend Specific Requirements::

    * Git
        * Dulwich (http://github.com/jelmer/dulwich/)
    * Subversion
        * Pysvn (http://pysvn.tigris.org/)
