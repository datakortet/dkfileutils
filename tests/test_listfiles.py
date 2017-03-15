# -*- coding: utf-8 -*-
import os

from dkfileutils.listfiles import list_files, read_skipfile
from yamldirs import create_files

BASEDIR = os.path.dirname(__file__)
print "FILE:", __file__
print "BSDIR:", BASEDIR
print "cwd:", os.getcwd()


# def _files(fit):
#     return [y for x, y in fit]


def test_skipfile():
    assert read_skipfile('.', ['foo']) == ['foo']


def test_skippy():
    files = """
        - a
        - b
        - f:
            - .dotfile
        - __pycache__:
            - c
        - htmlcov:
            - d
        - e.pyc
        - foo.egg-info:
            - e
    """
    with create_files(files) as root:
        assert {fname for _hex, fname in list_files(root)} == {'a', 'b'}

        assert {fname for _hex, fname in list_files(root)} == {'a', 'b'}

        assert [fname for _hex, fname in list_files(os.path.join(root, '.dotdir'))] == []


def test_dot_path():
    files = """
        - a:
            - .skipfile: |
                b/.c/d/e
            - b:
                - .c:
                    - d:
                        - e: |
                            hello
                        - f: |
                            world
            - g
    """
    print "test_dot_path"
    with create_files(files) as directory:
        os.chdir(directory)
        assert [fname for _hex, fname in list_files('a')] == ['g']
