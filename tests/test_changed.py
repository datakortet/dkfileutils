# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from hashlib import md5
from yamldirs import create_files
from dkfileutils import changed, path
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


def test_changed_glob():
    files = """
        a:
            b:
                c:
                    d.txt: hello world
            e:
                f.rst: thanks for all the fish
    """
    with create_files(files) as _root:
        adir = changed.Directory('a')
        print('digest:', changed.digest(adir))

        # should be changed first time
        assert adir.changed(glob='**/*')
        assert adir.changed(glob='**/*.txt')
        assert adir.changed(glob='**/*.rst')

        print('digest:', changed.digest(adir))

        # not changed second time
        assert not adir.changed(glob='**/*')
        assert not adir.changed(glob='**/*.txt')
        assert not adir.changed(glob='**/*.rst')

        dtxt = adir / 'b' / 'c' / 'd.txt'
        with dtxt.open('a') as fp:
            print('appended', file=fp)

        print("DTXT:", dtxt.read())
        os.chdir(_root)

        print('digest:', changed.digest(adir))
        print('cwd:', os.getcwd())
        adir = changed.Directory('a')
        assert adir.changed(glob='**/*')
        assert adir.changed(glob='**/*.txt')
        assert not adir.changed(glob='**/*.rst')

        frst = adir / 'e' / 'f.rst'
        with frst.open('a') as fp:
            print('appended', file=fp)

        assert adir.changed(glob='**/*')
        assert not adir.changed(glob='**/*.txt')
        assert adir.changed(glob='**/*.rst')


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
