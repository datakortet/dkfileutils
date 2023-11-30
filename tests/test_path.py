# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import stat

import time

import pytest
import sys

from dkfileutils import path
from yamldirs import create_files

from dkfileutils.path import cd, doc

opjoin = os.path.join


def _relcontent(root):
    return {p.relpath(root) for p in root}


def test_doc_decorator():
    def hasdoc():
        "hasdoc-docstring"
        pass

    def nodoc():
        pass

    @doc(hasdoc)
    def t1():
        "t1doc"
        pass

    @doc(nodoc)
    def t2():
        "t2doc"

    assert hasdoc() == nodoc() == t1() == t2()
    assert t1.__doc__ == "t1-docstring"
    assert t2.__doc__ is None


def test_open():
    files = """
        b: hello
    """
    with create_files(files) as root:
        assert (path.Path(root) / 'b').open().read() == 'hello'


def test_read():
    files = """
        b: hello
    """
    with create_files(files) as root:
        assert (path.Path(root) / 'b').read() == 'hello'


def test_write():
    files = """
        b: hello
    """
    with create_files(files) as root:
        r = path.Path(root)
        bfile = r / 'b'
        bfile.write('goodbye')
        assert bfile.read() == 'goodbye'
        cfile = r / 'c'
        cfile.write('world')
        assert cfile.read() == 'world'


def test_append():
    files = """
        b: hello
    """
    with create_files(files) as root:
        r = path.Path(root)
        bfile = r / 'b'
        bfile.append(' world')
        assert bfile.read() == 'hello world'


def test_iter():
    files = """
        - .dotfile
        - .dotdir:
            - d
            - e
        - a
        - b
        - c:
            - d
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert _relcontent(root) == {'a', 'b', opjoin('c', 'd')}


def test_contains():
    files = """
        - a
        - b
        - somename
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert 'a' in root
        assert 'b' in root
        assert 'c' not in root
        assert 'some' in (root / 'somename')


def test_rmtree():
    files = """
        a:
            b:
                c:
                    d.txt: hello world
        e:
            f.txt: thanks for all the fish
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        print("FILES:", root.contents())
        # print "LISTALL:", root.listall()
        (root / 'a').rmtree('b')
        assert root.contents() == [path.Path('e') / 'f.txt']
        (root / 'e').rmtree()
        assert root.contents() == []


def test_curdir():
    assert path.Path.curdir() == os.path.normcase(os.getcwd())


def test_touch_existing():
    # needs enough files that it takes a perceivable amount of time to create
    # them
    files = """
        a: hello
        b: beautiful
        c: world
        d:
            a: hello
            b: beautiful
            c: world
            d:
                a: hello
                b: beautiful
                c: world
                d:
                    a: hello
                    b: beautiful
                    c: world
                    d:
                        a: hello
                        b: beautiful
                        c: world
    """
    before = time.time()
    with create_files(files) as _root:
        after = time.time()
        assert before <= after
        print('before/after', before, after, after - before)
        root = path.Path(_root)
        print("FILES:", root.contents())
        assert 'a' in root
        a = root / 'a'
        a_before_touch = a.getmtime()
        # assert before <= a_before_touch <= after
        a.touch()
        after_touch = time.time()
        a_after_touch = a.getmtime()
        print("LOCALS:", locals())
        assert a_before_touch <= a_after_touch
        # assert a_after_touch > after
        # assert a_after_touch <= after_touch


def test_touch_not_exist():
    files = """
        a: hello
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        a = root / 'a'
        with pytest.raises(OSError):
            a.touch(exist_ok=False)


def test_touch_new():
    files = """
        a: hello
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert 'a' in root
        assert 'b' not in root
        b = root / 'b'
        assert not b.exists()
        b.touch()
        assert b.exists()
        assert 'b' in root


def test_parents():
    files = """
        a:
            b:
                c:
                    d.txt: hello world
    """
    with create_files(files) as _root:
        root = path.Path(_root).abspath()
        d = root / 'a' / 'b' / 'c' / 'd.txt'
        assert d.open().read() == "hello world"
        print("PARTS:", d.parts())
        print("PARENTS:", d.parents)
        assert d.parents == [
            root / 'a' / 'b' / 'c',
            root / 'a' / 'b',
            root / 'a',
            root
        ] + root.parents
        assert d.parent == root / 'a' / 'b' / 'c'


def test_dirops():
    files = """
        - a:
            - b
            - c
        - d: []
        - e:
            - f:
                - g: []
    """
    with create_files(files) as directory:
        p = path.Path(directory)
        (p / 'a').chdir()
        assert set(os.listdir(p / 'a')) == {'b', 'c'}

        (p / 'd').rmdir()
        assert set(os.listdir(p)) == {'a', 'e'}

        (p / 'e' / 'f' / 'g').removedirs()
        assert set(os.listdir(p)) == {'a'}


def test_move():
    files = """
       - a:
       - b:
         - c: []
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert sorted(os.listdir(root)) == ['a', 'b']
        assert os.listdir(os.path.join(_root, 'b', 'c')) == []
        a = root / 'a'
        a.move('b/c')
        assert os.listdir(root) == ['b']
        assert os.listdir(os.path.join(_root, 'b', 'c')) == ['a']


def test_rename():
    files = """
        a
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert os.listdir(root) == ['a']
        (root / 'a').rename('b')
        assert os.listdir(root) == ['b']


def test_renames():
    files = """
    - foo:
        - a:
            - b
            - c
        - d:
            - empty
        - e:
            - f:
                - g: |
                    hello world
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        (root / 'foo').renames('bar')
        newfiles = [f.relpath(root).replace('\\', '/')
                    for f in root.glob('**/*')]
        print(newfiles)
        assert 'bar/a/b' in newfiles
        assert 'bar/a/c' in newfiles
        assert 'bar/e/f/g' in newfiles
        assert 'bar/d' not in newfiles


def test_utime():
    files = """
        a
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        t = time.time()
        _stat = root.utime()
        assert abs(_stat.st_atime - t) < 1


def test_chmod():
    files = """
        a
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        (root / 'a').chmod(0o0400)  # only read for only current user
        # (root / 'a').chmod(stat.S_IREAD)
        if sys.platform == 'win32':
            # doesn't appear to be any way for a user to create a file that he
            # can't unlink on linux.
            with pytest.raises(OSError):
                (root / 'a').unlink()
        assert root.listdir() == ['a']
        (root / 'a').chmod(stat.S_IWRITE)
        (root / 'a').unlink()
        assert root.listdir() == []


def test_unlink():
    files = """
        - a
        - b
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert {p.relpath(root) for p in root} == {'a', 'b'}

        b = root / 'b'
        b.unlink()
        assert [p.relpath(root) for p in root] == ['a']

        a = root / 'a'
        a.remove()
        assert [p.relpath(root) for p in root] == []


def test_rm():
    files = """
        - a
        - b
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert {p.relpath(root) for p in root} == {'a', 'b'}

        b = root / 'b'
        b.rm()
        assert [p.relpath(root) for p in root] == ['a']

        root.rm('a')
        assert [p.relpath(root) for p in root] == []

        root.rm('c')  # shouldn't raise
        assert [p.relpath(root) for p in root] == []


def test_glob():
    files = """
        - a.py
        - b:
            - a.txt
            - aa.txt
        - d
        - e:
            - a:
                - b
        - f
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert [p.relpath(root) for p in root.glob('**/*.py')] == ['a.py']
        assert [p.relpath(root) for p in root.glob('*.py')] == ['a.py']
        assert [p.relpath(root) for p in root.glob('b/a?.txt')] == [
            opjoin('b', 'aa.txt')
        ]
        assert [p.relpath(root) for p in root.glob('**/a.*')] == [
            'a.py', opjoin('b', 'a.txt')
        ]


def test_subdirs():
    files = """
        - a.py
        - b:
            - a.txt
            - aa.txt
        - d
        - e:
            - a:
                - b
        - f
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert sorted([d.relpath(root) for d in root.subdirs()]) == ['b', 'e']


def test_files():
    files = """
        - a.py
        - b:
            - a.txt
            - aa.txt
        - d
        - e:
            - a:
                - b
        - f
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        print("LISTDIR:", os.listdir('.'))
        assert {d.relpath(root) for d in root.files()} == {
            'a.py', 'd', 'f'
        }


def test_makedirs():
    files = """
        a:
            - b:
                - empty
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        e = root.makedirs('a/b/c/d')
        # print "root", root
        # print 'E:', e
        assert e.isdir()
        assert e.relpath(root) == path.Path('a')/'b'/'c'/'d'

        e2 = root.makedirs('a/b/c/d')
        assert e2.isdir()

        b = root.mkdir('b')
        assert b.isdir()


def test_commonprefix():
    files = """
        - a.py
        - b:
            - a.txt
            - aa.txt
        - d
        - e:
            - a:
                - b
        - f
    """
    with create_files(files) as _root:
        r = path.Path(_root)
        assert r.commonprefix(r) == r
        assert r.commonprefix(r/'a.py', r/'d', r/'b'/'a.txt') == r


def test_abspath():
    assert os.path.normcase(os.path.abspath('empty')) == path.Path('empty').abspath()


def test_drive():
    assert os.path.splitdrive('empty')[0] == path.Path('empty').drive()


def test_drivepath():
    assert os.path.splitdrive('empty')[1] == path.Path('empty').drivepath()


def test_basename():
    assert os.path.basename('empty') == path.Path('empty').basename()


def test_dirname():
    assert os.path.dirname('empty') == path.Path('empty').dirname()


def test_exists():
    assert os.path.exists('empty') == path.Path('empty').exists()


def test_expanduser():
    assert os.path.expanduser('empty') == path.Path('empty').expanduser()


def test_expandvars():
    assert os.path.expandvars('empty') == path.Path('empty').expandvars()


def test_getatime():
    files = """
        b: hello
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert os.path.getatime(root/'b') == (root/'b').getatime()


def test_getctime():
    files = """
        b: hello
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert os.path.getctime(root/'b') == (root/'b').getctime()


def test_getmtime():
    files = """
        b: hello
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert os.path.getmtime(root/'b') == (root/'b').getmtime()


def test_access():
    files = """
        b: hello
    """
    with create_files(files) as _root:
        b = path.Path(_root) / 'b'
        assert b.access(os.R_OK)


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
    assert os.path.normcase(os.path.realpath('empty')) == path.Path('empty').realpath()


def test_relpath():
    assert os.path.relpath('empty') == path.Path('empty').relpath()


def test_path_to():
    parent = os.path.abspath('..')
    assert path.Path('.').path_to(parent) == '..'


def test_split():
    assert os.path.split('empty') == path.Path('empty').split()
    assert 'string variable'.split() == path.Path('string variable').split()


def test_splitdrive():
    assert os.path.splitdrive('empty') == path.Path('empty').splitdrive()


def test_splitext():
    assert os.path.splitext('empty') == path.Path('empty').splitext()


def test_ext():
    assert path.Path('hello.world').ext == '.world'


def test_switchext():
    assert path.Path('foo.dot').switchext('.svg') == 'foo.svg'


def test_list():
    assert path.Path('.').list(lambda x: False) == []


def test_list2():
    files = """
      - a
      - b
    """
    with create_files(files) as d:
        assert len(path.Path(d).list()) == 2
        assert len(path.Path(d).list(lambda fname: fname[-1] > 'a')) == 1


def test_listdir():
    assert [os.path.normcase(p) for p in os.listdir('.')] == path.Path('.').listdir()


def test_lstat():
    assert os.lstat(__file__) == path.Path(__file__).lstat()


def test_stat():
    assert os.stat(__file__) == path.Path(__file__).stat()


def test_cd():
    files = """
        a:
          - b
    """
    with create_files(files) as _root:
        root = path.Path(_root)
        assert 'a' in os.listdir('.')
        with (root/'a').cd():
            assert 'b' in os.listdir('.')
        assert 'a' in os.listdir('.')


def test_cd_contextmanager():
    files = """
        a:
          - b
    """
    with create_files(files) as _root:
        # root = path.Path(_root)
        assert 'a' in os.listdir('.')
        with cd('a'):
            assert 'b' in os.listdir('.')
        assert 'a' in os.listdir('.')
