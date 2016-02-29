
.. image:: https://travis-ci.org/datakortet/dkfileutils.svg?branch=master
    :target: https://travis-ci.org/datakortet/dkfileutils


.. image:: https://coveralls.io/repos/datakortet/dkfileutils/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/datakortet/dkfileutils?branch=master



dkfileutils -- file and directory utilities
==================================================

Documentation: http://pythonhosted.org/dkfileutils/


Contains the following modules
------------------------------
See the documentation link (above) and module documentation for detailed docs.

changed
    Code to check if directory contents have changed since last check.

listfiles
    Yield (digest, fname) tuples for all interesting files
    in `dirname`.  The file names are relative to `curdir`
    unless otherwise specified.

path
    "Poor man's pathlib".  Object-oriented wrapper around :func:`os.path` and
    friends.  Similar to the Python 3 :mod:`pathlib`, however paths are
    :type:`str` subclasses and thus much easier to use in an environment
    where :func:`os.path` calls are interspersed with object-oriented code.

pfind
    Find directory where a file is located by walking up parent directories.

which
    Functions for finding executable files on the path.


Installing from PyPI
--------------------

This is what you want if you just want to use dkfileutils:

   pip install dkfileutils


As a source package
-------------------
This is what you want if you are developing dkfileutils or want 
to make local changes to the source code.

   pip install -e <path>




See docs/ folder for documentation.
