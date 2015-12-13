# -*- coding: utf-8 -*-
import os

from dkfileutils import pfind

BASEDIR = os.path.dirname(__file__)


def test_pfind():
    assert pfind.pfind('.', 'setup.py') == os.path.abspath(BASEDIR + '/../setup.py')
