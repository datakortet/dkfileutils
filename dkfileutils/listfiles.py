# -*- coding: utf-8 -*-
"""
"""
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
        ).read().split('\n')
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
    skipfiles = read_skipfile()

    def clean_dirs(dirs):
        for d in dirs:
            if d.endswith('.egg-info'):
                dirs.remove(d)
        for d in skipdirs:
            if d in dirs:
                dirs.remove(d)

    def keep_file(fname):
        if fname.startswith('.'):
            return False
        if fname in skipfiles:
            return False
        for ext in skipexts:
            if fname.endswith(ext):
                return False
        return True

    for root, dirs, files in os.walk(os.path.abspath(str(dirname))):
        clean_dirs(dirs)
        for fname in [f for f in files if keep_file(f)]:
            pth = os.path.join(root, fname).replace('\\', '/')
            if pth.startswith('./'):
                pth = pth[2:]
            if any(p.startswith('.') for p in Path(pth).parts()):
                continue
            if relative:
                p = os.path.relpath(pth, curdir)
            else:
                p = pth
            yield md5(open(pth).read()).hexdigest(), p.replace('\\', '/')


def main():
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


if __name__ == "__main__":
    main()
