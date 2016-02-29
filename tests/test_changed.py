# -*- coding: utf-8 -*-

import os
from hashlib import md5
from yamldirs import create_files
from dkfileutils import changed
from dkfileutils.changed import Directory


def test_empty_digest():
    files = """
        emptydir: []
    """
    with create_files(files) as directory:
        assert changed.digest('emptydir') == md5("").hexdigest()


def test_changed():
    files = """
        emptydir: []
    """
    with create_files(files) as directory:
        assert changed.changed('emptydir')


def test_missing():
    assert changed.changed("this-directory-doesnt-exist")


def test_multifiles():
    files = """
        a:
            - b: |
                hello
            - c: |
                world
    """
    with create_files(files) as directory:
        assert changed.changed('a')
        assert not Directory('a').changed()
