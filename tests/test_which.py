# -*- coding: utf-8 -*-

from dkfileutils import which


def test_which():
    # find exists on both win an *nix
    assert len(list(which.which('find'))) > 0


def test_get_executable():
    assert which.get_executable('find')
