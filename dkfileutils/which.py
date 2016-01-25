# -*- coding: utf-8 -*-
"""Print where on the path an executable is located.
"""
from __future__ import print_function
import sys
import os
from stat import ST_MODE, S_IXUSR, S_IXGRP, S_IXOTH


def get_executable(name):
    for result in which(name)):
        return result
    return None


def get_path_directories():
    pth = os.environ['PATH']
    if sys.platform == 'win32' and os.environ.get("BASH"):
        # winbash has a bug..
        if pth[1] == ';':  # pragma: nocover
            pth = pth.replace(';', ':', 1)
    return pth.split(os.pathsep)


def is_executable(fname):
    return os.stat(fname)[ST_MODE] & (S_IXUSR | S_IXGRP | S_IXOTH)


def which(filename, interactive=False, verbose=False):
    exe = os.environ.get('PATHEXT', ['.cmd', '.bat', '.exe', '.com'])

    name, ext = os.path.splitext(filename)
    if ext and (ext in exe):  # pragma: nocover
        exe = []

    def match(filenames):
        res = set()
        for fname in filenames:
            if fname == filename:  # pragma: nocover
                res.add(fname)
                continue

            fn_name, fn_ext = os.path.splitext(fname)
            if name == fn_name:
                for suffix in exe:
                    if name + fn_ext == fname:
                        res.add(fname)

        return sorted(res)

    returnset = set()
    found = False
    for pth in get_path_directories():
        if not pth.strip():  # pragma: nocover
            continue

        if verbose:  # pragma: nocover
            print('checking pth..')

        try:
            fnames = os.listdir(pth)
        except:  # pragma: nocover
            continue

        matched = match(fnames)

        if matched:
            for m in matched:
                found_file = os.path.normcase(os.path.normpath(os.path.join(pth, m)))
                if found_file not in returnset:
                    if is_executable(found_file):
                        yield found_file
                    returnset.add(found_file)
            found = True

    if not found and interactive:  # pragma: nocover
        print("Couldn't find %r anywhere on the path.." % filename)
        sys.exit(1)


if __name__ == "__main__":  # pragma: nocover
    for _fname in which(sys.argv[1], interactive=True, verbose='-v' in sys.argv):
        print(_fname)
    sys.exit(0)
