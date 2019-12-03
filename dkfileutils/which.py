# -*- coding: utf-8 -*-
"""Print where on the path an executable is located.
"""
from __future__ import print_function
import sys
import os
from stat import ST_MODE, S_IXUSR, S_IXGRP, S_IXOTH


def get_executable(name):
    """Return the first executable on the path that matches `name`.
    """
    for result in which(name):
        return result
    return None


def get_path_directories():
    """Return a list of all the directories on the path.
    """
    pth = os.environ['PATH']
    if sys.platform == 'win32' and os.environ.get("BASH"):
        # winbash has a bug..
        if pth[1] == ';':  # pragma: nocover
            pth = pth.replace(';', ':', 1)
    return [p.strip() for p in pth.split(os.pathsep) if p.strip()]


def is_executable(fname):
    """Check if a file is executable.
    """
    return os.stat(fname)[ST_MODE] & (S_IXUSR | S_IXGRP | S_IXOTH)


def _listdir(pth, extensions):
    """Non-raising listdir."""
    try:
        return [fname for fname in os.listdir(pth)
                if os.path.splitext(fname)[1] in extensions]
    except OSError:  # pragma: nocover
        pass


def _normalize(pth):
    return os.path.normcase(os.path.normpath(pth))


def which(filename, interactive=False, verbose=False):
    """Yield all executable files on path that matches `filename`.
    """
    exe = [e.lower() for e in os.environ.get('PATHEXT', '').split(';')]
    if sys.platform != 'win32':  # pragma: nocover
        exe.append('')

    name, ext = os.path.splitext(filename)
    has_extension = bool(ext)
    if has_extension and ext.lower() not in exe:
        raise ValueError("which can only search for executable files")

    def match(filenames):
        """Returns the sorted subset of ``filenames`` that matches 
           ``filename``.
        """
        res = set()
        for fname in filenames:
            if fname == filename:  # pragma: nocover
                res.add(fname)  # exact match
                continue
            fname_name, fname_ext = os.path.splitext(fname)
            if fname_name == name and fname_ext.lower() in exe:  # pragma: nocover
                res.add(fname)
        return sorted(res)

    returnset = set()
    found = False
    for pth in get_path_directories():
        if verbose:  # pragma: nocover
            print('checking pth..')

        fnames = _listdir(pth, exe)
        if not fnames:
            continue

        for m in match(fnames):
            found_file = _normalize(os.path.join(pth, m))
            if found_file not in returnset:  # pragma: nocover
                if is_executable(found_file):
                    yield found_file
                returnset.add(found_file)
        found = True

    if not found and interactive:  # pragma: nocover
        print("Couldn't find %r anywhere on the path.." % filename)
        sys.exit(1)


if __name__ == "__main__":  # pragma: nocover
    _args = sys.argv
    for _fname in which(_args[1], interactive=True, verbose='-v' in _args):
        print(_fname)
    sys.exit(0)
