

dkfileutils - file and directory utilities
==========================================

.. image:: https://readthedocs.org/projects/dkfileutils/badge/?version=latest

.. image:: https://codecov.io/gh/datakortet/dkfileutils/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/datakortet/dkfileutils

.. image:: https://scrutinizer-ci.com/g/datakortet/dkfileutils/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/datakortet/dkfileutils/

Documentation: http://dkfileutils.readthedocs.io/


Contains the following modules
------------------------------
See the documentation link (above) and module documentation for detailed docs.

changed
~~~~~~~
Code to check if directory contents have changed since last check.

listfiles
~~~~~~~~~
Yield (digest, fname) tuples for all interesting files
in `dirname`.  The file names are relative to `curdir`
unless otherwise specified.

path
~~~~
"Poor man's pathlib".  Object-oriented wrapper around `os.path` and
friends.  Similar to the Python 3 `pathlib`, however paths are
`str` subclasses and thus much easier to use in an environment
where `os.path` calls are interspersed with object-oriented code.

Brett Cannon strongly dislikes paths being `str` subclasses, see
https://snarky.ca/why-pathlib-path-doesn-t-inherit-from-str/
While I can agree with him in principle, this is clearly a case
of "practicality beats purity".  The official ``pathlib`` version
of ``'/b/' in Path('/a/b/c')`` is rather baroque.

pfind
~~~~~
Find directory where a file is located by walking up parent directories.

which
~~~~~
Functions for finding executable files on the path.

