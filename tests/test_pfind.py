# -*- coding: utf-8 -*-
import os

from dkfileutils import pfind

BASEDIR = os.path.dirname(__file__)


def test_pfind():
    assert pfind.pfind(BASEDIR, 'setup.py') == os.path.abspath(BASEDIR + '/../setup.py')


def test_failure():
    assert pfind.pfind('/', 'zysasdfasdfasdf') is None
