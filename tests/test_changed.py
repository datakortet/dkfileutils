# -*- coding: utf-8 -*-

import os
from hashlib import md5
from dkfileutils import changed, path


BASEDIR = os.path.dirname(__file__)


def test_digest():
    assert changed.digest('empty') == md5("").hexdigest()


def test_changed():
    skiptests = path.Path(BASEDIR) / 'skiptests'
    assert changed.changed(skiptests)
