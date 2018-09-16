
dkfileutils -- file and directory utilities
===========================================

.. image:: https://travis-ci.org/datakortet/dkfileutils.svg?branch=master
   :target: https://travis-ci.org/datakortet/dkfileutils

.. image:: https://coveralls.io/repos/datakortet/dkfileutils/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/datakortet/dkfileutils?branch=master

.. image:: https://readthedocs.org/projects/dkfileutils/badge/?version=latest

.. image:: https://codecov.io/gh/datakortet/dkfileutils/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/datakortet/dkfileutils

.. image:: https://scrutinizer-ci.com/g/datakortet/dkfileutils/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/datakortet/dkfileutils/


Documentation: http://dkfileutils.readthedocs.io/


Contains the following modules
------------------------------
See the documentation link (above) and module documentation for detailed docs.

path - a more convenient pathlib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``pathlib`` implementation where ``Path`` is a subclass of string.
This design makes it trivial to pass path objects to library functions
that will use ``os.path.*`` functions without littering your code with
``str(mypath)`` calls.

changed
~~~~~~~
Code to check if directory contents have changed since last check.

listfiles
~~~~~~~~~
Yield (digest, fname) tuples for all interesting files
in `dirname`.  The file names are relative to `curdir`
unless otherwise specified.

pfind
~~~~~
Find directory where a file is located by walking up parent directories.

which
~~~~~
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
