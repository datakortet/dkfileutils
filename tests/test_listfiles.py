# -*- coding: utf-8 -*-
import os

from dkfileutils import listfiles

BASEDIR = os.path.dirname(__file__)


def test_skipfile():
    assert listfiles.read_skipfile('.', ['foo']) == ['foo']


def test_listfiles():
    assert list(listfiles.list_files('empty')) == []
