# -*- coding: utf-8 -*-
import os

# from dkfileutils import path
from dkfileutils.listfiles import list_files, read_skipfile
from yamldirs import create_files


BASEDIR = os.path.dirname(__file__)


def test_skipfile():
    assert read_skipfile('.', ['foo']) == ['foo']


def test_listfiles():
    assert list(list_files('empty')) == []


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
        assert [fname for _hex, fname in list_files(root, root)] == [
            'a', 'b'
        ]

        assert [fname for _hex, fname in list_files(root, root, False)] == [
            os.path.join(root, 'a').replace('\\', '/'),
            os.path.join(root, 'b').replace('\\', '/')
        ]

        assert [fname for _hex, fname in list_files(os.path.join(root, '.dotdir'), root)] == []
