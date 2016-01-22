# -*- coding: utf-8 -*-
import argparse
import os
from hashlib import md5
from .path import Path

SKIPFILE_NAME = '.skipfile'


def read_skipfile(dirname='.', defaults=None):
    if defaults is None:
        defaults = ['Makefile', 'make.bat', 'atlassian-ide-plugin.xml']
    try:
        return defaults + open(
            os.path.join(dirname, SKIPFILE_NAME)
        ).read().splitlines()
    except IOError:
        return defaults


def list_files(dirname='.', curdir=".", relative=True):
    skipdirs = ['__pycache__', '.git', '.svn', 'htmlcov', 'dist', 'build',
                '.idea', 'tasks', 'static', 'media', 'data', 'migrations',
                '.doctrees', '_static', 'node_modules', 'external',
                'jobs', 'tryout', 'tmp', '_coverage',
                ]
    skipexts = ['.pyc', '~', '.svg', '.txt', '.TTF', '.tmp', '.errmail',
                '.email', '.bat', '.dll', '.exe', '.Dll', '.jpg', '.gif',
                '.png', '.ico', '.db', '.md5']
    dirname = str(dirname)
    skipfiles = read_skipfile(dirname)

    def clean_dirs(directories):
        for d in directories:
            if d.endswith('.egg-info'):
                directories.remove(d)
        for d in skipdirs:
            if d in directories:
                directories.remove(d)

    def keep_file(filename, filepath):
        if filename.startswith('.'):
            return False
        if filepath in skipfiles:
            return False
        for ext in skipexts:
            if filename.endswith(ext):
                return False
        return True

    for root, dirs, files in os.walk(os.path.abspath(dirname)):
        clean_dirs(dirs)
        for fname in files:
            relpth = os.path.relpath(os.path.join(root, fname), dirname).replace('\\', '/')

            parts = Path(relpth).parts()
            if not keep_file(fname, relpth) or any(p.startswith('.') for p in parts):
                continue

            pth = os.path.join(dirname, relpth)
            yield md5(open(pth).read()).hexdigest(), relpth


def main():  # pragma: nocover
    p = argparse.ArgumentParser(add_help="Recursively list interesting files.")
    p.add_argument(
        'directory', nargs="?", default="",
        help="The directory to process (current dir if omitted)."
    )
    p.add_argument(
        '--verbose', '-v', action='store_true',
        help="Increase verbosity."
    )

    args = p.parse_args()
    args.curdir = os.getcwd()
    if not args.directory:
        args.direcotry = args.curdir
    if args.verbose:
        print args

    for chsm, fname in list_files(args.directory):
        print chsm, fname


if __name__ == "__main__":  # pragma: nocover
    main()
