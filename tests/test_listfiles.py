# -*- coding: utf-8 -*-
import os

from dkfileutils import listfiles, path

BASEDIR = os.path.dirname(__file__)
print "FILE:", __file__
print "BSDIR:", BASEDIR
print "cwd:", os.getcwd()


def _files(fit):
    return [y for x,y in fit]


def test_skipfile():
    assert listfiles.read_skipfile('.', ['foo']) == ['foo']


def test_listfiles():
    empty = path.Path(BASEDIR).makedirs('empty')
    assert _files(listfiles.list_files(empty)) == []


def test_skips():
    skiptests = path.Path(BASEDIR) / 'skiptests'
    print "SKIPTESTS: [%s][%s]" % (skiptests, BASEDIR)
    assert _files(listfiles.list_files(skiptests, skiptests)) == [
        'a',
        'foo/bar'
    ]
