# -*- coding: utf-8 -*-

from hashlib import md5
from dkfileutils import changed


def test_digest():
    assert changed.digest('empty') == md5("").hexdigest()


def test_changed():
    assert changed.changed('empty')
