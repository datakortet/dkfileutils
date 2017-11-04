# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from yamldirs import create_files
from dkfileutils import pfind
from dkfileutils.path import Path
from dkfileutils.pfind import pfindall

BASEDIR = os.path.dirname(__file__)


def test_pfind():
    assert pfind.pfind(BASEDIR, 'setup.py') == os.path.abspath(BASEDIR + '/../setup.py')


def test_notfound():
    assert pfind.pfind(BASEDIR, 'this-file-does-not-exist') is None


def test_pfindall():
    files = """
        a:
            - a1.txt
            - a1:
                - a2:
                    - a3.txt
                - a2.txt    
    """
    with create_files(files) as root:
        root = Path(root)

        assert dict(pfindall('a/a1/a2', 'a3.txt')) == {
            'a3.txt': root / 'a/a1/a2/a3.txt',
        }

        assert dict(pfindall('a/a1/a2', 'a2.txt', 'a3.txt')) == {
            'a3.txt': root / 'a/a1/a2/a3.txt',
            'a2.txt': root / 'a/a1/a2.txt',
        }

        assert dict(pfindall('a/a1/a2', 'a1.txt', 'a2.txt', 'a3.txt')) == {
            'a3.txt': root / 'a/a1/a2/a3.txt',
            'a2.txt': root / 'a/a1/a2.txt',
            'a1.txt': root / 'a/a1.txt',
        }
