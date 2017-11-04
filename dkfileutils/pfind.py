#!/usr/bin/python
"""CLI usage: ``pfind path filename`` will find the closest ancestor directory
   conataining filename (used for finding syncspec.txt and config files).
"""
from __future__ import print_function
import os
import sys


def pfindall(path, *fnames):
    """Find all fnames in the closest ancestor directory.
       For the purposes of this function, we are our own closest ancestor.
       I.e. given the structure::

            .
            `-- a
                |-- b
                |   |-- c
                |   |   `-- x.txt
                |   `-- x.txt
                `-- y.txt

       the call::

           dict(pfindall('a/b/c', 'x.txt', 'y.txt'))

       will return::

           {
               'x.txt': 'a/b/c/x.txt',
               'y.txt': 'a/y.txt'
           }

       ``a/b/x.txt`` is not returned, since ``a/b/c/x.txt`` is the "closest"
       ``x.txt`` when starting from ``a/b/c`` (note: pfindall only looks
       "upwards", ie. towards the root).
    """
    wd = os.path.abspath(path)
    assert os.path.isdir(wd)

    def parents():
        """yield successive parent directories
        """
        parent = wd
        yield parent
        while 1:
            parent, dirname = os.path.split(parent)
            if not dirname:
                return
            yield parent

    for d in parents():
        curdirlist = os.listdir(d)
        for fname in fnames:
            if fname in curdirlist:
                yield fname, os.path.join(d, fname)


def pfind(path, *fnames):
    """Find the first fname in the closest ancestor directory.
       For the purposes of this function, we are our own closest ancestor, i.e.
       given the structure::

            /srv
            |-- myapp
            |   |-- __init__.py
            |   `-- myapp.py
            `-- setup.py

       then both ``pfind('/srv', 'setup.py')`` and
       ``pfind('/srv/myapp', 'setup.py')`` will return ``/srv/setup.py``
    """
    for _fname, fpath in pfindall(path, *fnames):
        return fpath
    return None


if __name__ == "__main__":  # pragma: nocover
    _path, filename = sys.argv[1], sys.argv[2]
    print(pfind(_path, filename))
