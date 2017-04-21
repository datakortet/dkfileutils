#!/usr/bin/python
"""CLI usage: ``pfind path filename`` will find the closest ancestor directory
   conataining filename (used for finding syncspec.txt and config files).
"""
import os
import sys


def pfind(path, *fnames):
    """Find the first fname in the closest ancestor directory.
       For the purposes of this function, we are our own closest ancestor.
    """

    wd = os.path.abspath(path)
    assert os.path.isdir(wd)

    def parents():
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
                return os.path.join(d, fname)

    return None


if __name__ == "__main__":  # pragma: nocover
    _path, filename = sys.argv[1], sys.argv[2]
    print pfind(_path, filename)
