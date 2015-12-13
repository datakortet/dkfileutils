# -*- coding: utf-8 -*-
import glob
import os
from dkfileutils import path


# def test___iter__():
#     assert os.path.__iter__('empty') == path.Path('empty').__iter__()
#
# def test___contains__():
#     assert os.path.__contains__('empty') == path.Path('empty').__contains__()

def test_glob():
    assert glob.glob('empty') == path.Path('empty').glob('*')


def test_abspath():
    assert os.path.abspath('empty') == path.Path('empty').abspath()


def test_drive():
    assert os.path.splitdrive('empty')[0] == path.Path('empty').drive()


def test_drivepath():
    assert os.path.splitdrive('empty')[1] == path.Path('empty').drivepath()


def test_basename():
    assert os.path.basename('empty') == path.Path('empty').basename()


# def test_commonprefix():
#     assert os.path.commonprefix('empty', 'empty') == path.Path('empty').commonprefix('empty')


def test_dirname():
    assert os.path.dirname('empty') == path.Path('empty').dirname()


def test_exists():
    assert os.path.exists('empty') == path.Path('empty').exists()


def test_expanduser():
    assert os.path.expanduser('empty') == path.Path('empty').expanduser()


def test_expandvars():
    assert os.path.expandvars('empty') == path.Path('empty').expandvars()


# def test_getatime():
#     assert os.path.getatime('empty') == path.Path('empty').getatime()


# def test_getctime():
#     assert os.path.getctime('empty') == path.Path('empty').getctime()


# def test_getmtime():
#     assert os.path.getmtime('empty') == path.Path('empty').getmtime()


def test_getsize():
    assert os.path.getsize(__file__) == path.Path(__file__).getsize()


def test_isabs():
    assert os.path.isabs('empty') == path.Path('empty').isabs()


def test_isdir():
    assert os.path.isdir('empty') == path.Path('empty').isdir()


def test_isfile():
    assert os.path.isfile('empty') == path.Path('empty').isfile()


def test_islink():
    assert os.path.islink('empty') == path.Path('empty').islink()


def test_ismount():
    assert os.path.ismount('empty') == path.Path('empty').ismount()


def test_join():
    assert os.path.join('empty') == path.Path('empty').join()


def test_lexists():
    assert os.path.lexists('empty') == path.Path('empty').lexists()


def test_normcase():
    assert os.path.normcase('empty') == path.Path('empty').normcase()


def test_normpath():
    assert os.path.normpath('empty') == path.Path('empty').normpath()


def test_realpath():
    assert os.path.realpath('empty') == path.Path('empty').realpath()


def test_relpath():
    assert os.path.relpath('empty') == path.Path('empty').relpath()


def test_split():
    assert os.path.split('empty') == path.Path('empty').split()


def test_splitdrive():
    assert os.path.splitdrive('empty') == path.Path('empty').splitdrive()


def test_splitext():
    assert os.path.splitext('empty') == path.Path('empty').splitext()


# def test_ext():
#     assert os.path.ext('empty') == path.Path('empty').ext()


# def test_access():
#     assert os.access('empty') == path.Path('empty').access()


def test_listdir():
    assert os.listdir('.') == path.Path('.').listdir()


def test_lstat():
    assert os.lstat(__file__) == path.Path(__file__).lstat()


def test_stat():
    assert os.stat(__file__) == path.Path(__file__).stat()


# def test_utime():
#     assert os.utime('empty') == path.Path('empty').utime()
