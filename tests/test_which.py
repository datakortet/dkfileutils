# -*- coding: utf-8 -*-
import pytest

from dkfileutils import which


def test_which():
    # find exists on both win an *nix
    assert len(list(which.which('find'))) > 0


def test_get_executable():
    assert which.get_executable('find')


def test_missing_executable():
    assert not which.get_executable('chewbaccascousin')


def test_incorrect_extension():
    with pytest.raises(ValueError):
        which.get_executable('foo.bar')
