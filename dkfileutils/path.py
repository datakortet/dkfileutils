# -*- coding: utf-8 -*-
"""Poor man's pathlib.

   (Path instances are subclasses of str, so interoperability with existing
   os.path code is greater than with Python 3's pathlib.)
"""
# pylint:disable=C0111,R0904
# R0904: too many public methods in Path
from __future__ import print_function

import errno
import os
import re
from contextlib import contextmanager
import shutil


def _norm_case_path(p):
    return os.path.normcase(os.path.normpath(p))


def doc(srcfn, note=None):
    if note:
        note = """
        .. note:: {note}
        """.format(note=note)

    def decorator(fn):
        if srcfn.__doc__ is None:
            fn.__doc__ = None or note
        else:
            fn.__doc__ = srcfn.__doc__.replace(srcfn.__name__, fn.__name__)
            if note:
                fn.__doc__ += note
        return fn
    return decorator


class _CallableString(str):
    def __call__(self):
        return self


class Path(str):
    """Poor man's pathlib.
    """
    curdir = os.path.curdir
    pardir = os.path.pardir
    extsep = os.path.extsep
    sep = os.path.sep
    pathsep = os.path.pathsep
    altsep = os.path.altsep
    defpath = os.path.defpath
    devnull = os.path.devnull

    drive_letters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    ext_namespace_prefix = '\\\\?\\'

    reserved_names = (
        {'CON', 'PRN', 'AUX', 'NUL'} |
        set(['COM%d' % i for i in range(1, 10)]) |
        set(['LPT%d' % i for i in range(1, 10)])
    )

    def __new__(cls, *args, **kw):
        def _tostr(a):
            if isinstance(a, cls):
                return str(a)
            elif hasattr(type(a), '__fspath__'):
                return type(a).__fspath__(a)
            elif hasattr(a, '__fspath__'):
                return a.__fspath__()
            if type(a) == str or type(a) == unicode:
                return a
            raise TypeError('%r is not convertible to a path part' % a)

        if len(args) == 0:
            return str.__new__(cls, '.', **kw)
        if len(args) == 1:
            return str.__new__(cls, os.path.normcase(_tostr(args[0])), **kw)

        _args = [_tostr(a) for a in args]
        print("ARGS:", args, map(type, args))
        print("_ARGS:", _args, map(type, _args))
        return str.__new__(cls, _norm_case_path(os.path.join(*_args)), **kw)

    @staticmethod
    def xparse_parts(parts):
        pth = os.path.join(*parts)
        drive, root, _path = Path.splitroot(pth)
        return drive, root, re.split(r"[\\/]", pth)

    @staticmethod
    def parse_parts(parts):
        parsed = []
        sep = Path.sep
        altsep = Path.altsep
        drv = root = ''
        it = reversed(parts)
        for part in it:
            if not part:
                continue
            if altsep:
                part = part.replace(altsep, sep)
            drv, root, rel = Path.splitroot(part)
            if sep in rel:
                for x in reversed(rel.split(sep)):
                    if x and x != '.':
                        parsed.append(x)
            else:
                if rel and rel != '.':
                    parsed.append(rel)
            if drv or root:
                if not drv:
                    # If no drive is present, try to find one in the previous
                    # parts. This makes the result of parsing e.g.
                    # ("C:", "/", "a") reasonably intuitive.
                    for part in it:
                        if not part:
                            continue
                        if altsep:
                            part = part.replace(altsep, sep)
                        drv = Path.splitroot(part)[0]
                        if drv:
                            break
                break
        if drv or root:
            parsed.append(drv + root)
        parsed.reverse()
        return drv, root, parsed

    @property
    def suffix(self):
        """The final component's last suffix, if any."""
        name = self.name
        i = name.rfind('.')
        if 0 < i < len(name) - 1:
            return name[i:]
        else:
            return ''

    @property
    def suffixes(self):
        """A list of the final component's suffixes, if any."""
        name = self.name
        if name.endswith('.'):
            return []
        name = name.lstrip('.')
        return ['.' + suffix for suffix in name.split('.')[1:]]

    # @property
    # def suffix(self):
    #     return Path(os.path.splitext(self)[1])
    #
    # @property
    # def suffixes(self):
    #     res = []
    #     base = self
    #     while 1:
    #         base, ext = os.path.splitext(base)
    #         if not ext:
    #             break
    #         res.append(ext)
    #     return list(reversed(res))
    #
    # @property
    # def stem(self):
    #     return os.path.splitext(self.name)[0]

    @property
    def stem(self):
        """The final path component, minus its last suffix."""
        name = self.name
        i = name.rfind('.')
        if 0 < i < len(name) - 1:
            return name[:i]
        else:
            return name

    @staticmethod
    def _split_extended_path(s, ext_prefix=ext_namespace_prefix):
        prefix = ''
        if s.startswith(ext_prefix):
            prefix = s[:4]
            s = s[4:]
            if s.startswith('UNC\\'):
                prefix += s[:3]
                s = '\\' + s[3:]
        return prefix, s

    # pathlib._WindowsFlavour.splitroot
    @classmethod
    def splitroot(cls, part, sep=sep):
        first = part[0:1]
        second = part[1:2]
        if second == sep and first == sep:
            # XXX extended paths should also disable the collapsing of "."
            # components (according to MSDN docs).
            prefix, part = cls._split_extended_path(part)
            first = part[0:1]
            second = part[1:2]
        else:
            prefix = ''
        third = part[2:3]
        if second == sep and first == sep and third != sep:
            # is a UNC path:
            # vvvvvvvvvvvvvvv    @classmethodvvvvvv root
            # \\machine\mountpoint\directory\etc\...
            #            directory ^^^^^^^^^^^^^^
            index = part.find(sep, 2)
            if index != -1:
                index2 = part.find(sep, index + 1)
                # a UNC path can't have two slashes in a row
                # (after the initial two)
                if index2 != index + 1:
                    if index2 == -1:
                        index2 = len(part)
                    if prefix:
                        return prefix + part[1:index2], sep, part[index2+1:]
                    else:
                        return part[:index2], sep, part[index2+1:]
        drv = root = ''
        if second == ':' and first in cls.drive_letters:
            drv = part[:2]
            part = part[2:]
            first = third
        if first == sep:
            root = first
            part = part.lstrip(sep)
        return prefix + drv, root, part

    def __fspath__(self):
        return str(self)

    def __str__(self):
        return super(Path, self).__str__() or '.'

    def __div__(self, other):
        return Path(_norm_case_path(os.path.join(self, other)))
    __truediv__ = __div__

    def __rdiv__(self, other):
        return Path(_norm_case_path(os.path.join(other, self)))

    @property
    def anchor(self):
        drv, root, _ = self.splitroot(self)
        return Path(os.path.join(drv, root))

    @doc(os.unlink)
    def unlink(self):
        os.unlink(self)

    def open(self, mode='r', **kw):
        return open(self, mode, **kw)

    def read(self, mode='r', **kw):
        with self.open(mode, **kw) as fp:
            return fp.read()

    read_text = read

    def read_bytes(self, **kw):
        return self.read(mode='rb', **kw)

    def write(self, txt, mode='w', **kw):
        with self.open(mode, **kw) as fp:
            fp.write(txt)

    write_text = write

    def write_bytes(self, txt):
        if isinstance(txt, unicode):
            raise TypeError
        return self.write(txt, 'wb')

    def append(self, txt, mode='a'):
        with self.open(mode) as fp:
            fp.write(txt)

    def as_posix(self):
        """Return a string representation of the path with forward slashes (/)
        """
        return self.replace('\\', '/')

    def as_uri(self):
        """Return the path as a 'file' URI.
        """
        if not self.is_absolute():
            raise ValueError("relative path can't be expressed as a file URI")
        return self._flavour.make_uri(self)

    def is_absolute(self):
        """True if the path is absolute (has both a root and, if applicable,
           a drive).
        """
        drv, root, _ = self.splitroot(self)
        return drv and root
        # if not self._root:
        #     return False
        # return not self._flavour.has_drv or bool(self._drv)

    def is_reserved(self, parts):
        # NOTE: the rules for reserved names seem somewhat complicated
        # (e.g. r"..\NUL" is reserved but not r"foo\NUL").
        # We err on the side of caution and return True for paths which are
        # not considered reserved by Windows.
        if not parts:
            return False
        if parts[0].startswith('\\\\'):
            # UNC paths are never reserved
            return False
        return parts[-1].partition('.')[0].upper() in self.reserved_names

    def __iter__(self):
        for root, dirs, files in os.walk(self):
            dotdirs = [d for d in dirs if d.startswith('.')]
            for d in dotdirs:
                dirs.remove(d)
            dotfiles = [d for d in files if d.startswith('.')]
            for d in dotfiles:
                files.remove(d)
            for fname in files:
                yield Path(os.path.join(root, fname))

    def __contains__(self, item):
        if self.isdir():
            return item in self.listdir()
        return super(Path, self).__contains__(item)

    @doc(shutil.rmtree)
    def rmtree(self, subdir=None):
        if subdir is not None:
            shutil.rmtree(self / subdir, ignore_errors=True)
        else:
            shutil.rmtree(self, ignore_errors=True)

    def contents(self):
        res = [d.relpath(self) for d in self.glob('**/*')]
        res.sort()
        return res

    @classmethod
    def curdir(cls):
        """Initialize a Path object on the current directory.
        """
        return cls(os.getcwd())
    cwd = curdir

    def touch(self, mode=0o666, exist_ok=True):
        """Create this file with the given access mode, if it doesn't exist.
           Based on:
            
              https://github.com/python/cpython/blob/master/Lib/pathlib.py)
              
        """
        if exist_ok:
            # First try to bump modification time
            # Implementation note: GNU touch uses the UTIME_NOW option of
            # the utimensat() / futimens() functions.
            try:
                os.utime(self, None)
            except OSError:
                # Avoid exception chaining
                pass
            else:
                return
        flags = os.O_CREAT | os.O_WRONLY
        if not exist_ok:
            flags |= os.O_EXCL
        fd = os.open(self, flags, mode)
        os.close(fd)

    def glob(self, pat):
        """`pat` can be an extended glob pattern, e.g. `'**/*.less'`
           This code handles negations similarly to node.js' minimatch, i.e.
           a leading `!` will negate the entire pattern.
        """
        r = ""
        negate = int(pat.startswith('!'))
        i = negate

        while i < len(pat):
            if pat[i:i + 3] == '**/':
                r += "(?:.*/)?"
                i += 3
            elif pat[i] == "*":
                r += "[^/]*"
                i += 1
            elif pat[i] == ".":
                r += "[.]"
                i += 1
            elif pat[i] == "?":
                r += "."
                i += 1
            else:
                r += pat[i]
                i += 1
        r += r'\Z(?ms)'
        rx = re.compile(r)

        def match(d):
            m = rx.match(d)
            return not m if negate else m

        return [s for s in self if match(s.relpath(self).replace('\\', '/'))]

    def match(self, pat):
        r = ""
        negate = int(pat.startswith('!'))
        i = negate

        while i < len(pat):
            if pat[i:i + 3] == '**/':
                r += "(?:.*/)?"
                i += 3
            elif pat[i] == "*":
                r += "[^/]*"
                i += 1
            elif pat[i] == ".":
                r += "[.]"
                i += 1
            elif pat[i] == "?":
                r += "."
                i += 1
            else:
                r += pat[i]
                i += 1
        r += r'\Z(?ms)'
        rx = re.compile(r)

        def match(d):
            m = rx.match(d)
            return not m if negate else m

        return bool(match(str(self)))

    @doc(os.path.abspath)
    def abspath(self):
        return Path(os.path.abspath(self))
    absolute = abspath  # pathlib

    @classmethod
    def home(cls):
        return Path(os.path.expanduser('~'))

    @property
    def drive(self):
        """Return the drive of `self`.
        """
        return _CallableString(self.splitroot(self)[0])
        # return self.splitdrive()[0]

    @property
    def root(self):
        return self.splitroot(self)[1]

    def drivepath(self):
        """The path local to this drive (i.e. remove drive letter).
        """
        return self.splitdrive()[1]

    @doc(os.path.basename)
    def basename(self):
        return Path(os.path.basename(self))

    @doc(os.path.commonprefix)
    def commonprefix(self, *args):
        return os.path.commonprefix([str(self)] + [str(a) for a in args])

    @doc(os.path.dirname)
    def dirname(self):
        return Path(os.path.dirname(self))

    @doc(os.path.exists)
    def exists(self):
        return os.path.exists(self)

    @doc(os.path.expanduser)
    def expanduser(self):
        return Path(os.path.expanduser(self))

    @doc(os.path.expandvars)
    def expandvars(self):
        return Path(os.path.expandvars(self))

    @doc(os.path.getatime)
    def getatime(self):
        return os.path.getatime(self)

    @doc(os.path.getctime)
    def getctime(self):
        return os.path.getctime(self)

    @doc(os.path.getmtime)
    def getmtime(self):
        return os.path.getmtime(self)

    @doc(os.path.getsize)
    def getsize(self):
        return os.path.getsize(self)

    @doc(os.path.isabs)
    def isabs(self):
        return os.path.isabs(self)

    @doc(os.path.isdir)
    def isdir(self, *args, **kw):
        return os.path.isdir(self, *args, **kw)
    is_dir = isdir

    @doc(os.path.isfile)
    def isfile(self):
        return os.path.isfile(self)
    is_file = isfile

    @doc(os.path.islink)
    def islink(self):
        return os.path.islink(self)

    @doc(os.path.ismount)
    def ismount(self):
        return os.path.ismount(self)

    @doc(os.path.join)
    def join(self, *args):
        return Path(os.path.join(self, *args))

    joinpath = join

    @doc(os.path.lexists)
    def lexists(self):
        return os.path.lexists(self)

    @property
    def name(self):
        _, fname = os.path.split(self)
        return fname

    @doc(os.path.normcase)
    def normcase(self):
        return Path(os.path.normcase(self))

    @doc(os.path.normpath)
    def normpath(self):
        return Path(os.path.normpath(str(self)))

    @doc(os.path.realpath)
    def realpath(self):
        return Path(os.path.realpath(self))

    @doc(os.path.relpath)
    def relpath(self, other=""):
        return Path(os.path.relpath(str(self), str(other)))

    relative_to = relpath
    __sub__ = relpath

    @doc(os.path.split)
    def split(self, sep=None, maxsplit=-1):
        # some heuristics to determine if this is a str.split call or
        # a os.split call...
        sval = str(self)
        if sep is not None or ' ' in sval:
            return sval.split(sep or ' ', maxsplit)
        return os.path.split(self)

    def parts(self):
        res = re.split(r"[\\/]", self)
        if res and os.path.splitdrive(res[0]) == (res[0], ''):
            res[0] += os.path.sep
        return res

    def parent_iter(self):
        # parts = self.abspath().normpath().normcase().parts()
        parts = self.parts()
        for i in range(1, len(parts)):
            yield Path(os.path.join(*parts[:-i]))

    @property
    def parents(self):
        return list(self.parent_iter())

    @property
    def parent(self):
        try:
            return self.parents[0]
        except IndexError:
            return None

    @doc(os.path.splitdrive)
    def splitdrive(self):
        drive, pth = os.path.splitdrive(self)
        return drive, Path(pth)

    @doc(os.path.splitext)
    def splitext(self):
        return os.path.splitext(self)

    @property
    def ext(self):
        return self.splitext()[1]

    def switchext(self, ext):
        return self.splitext()[0] + ext

    if hasattr(os.path, 'splitunc'):  # pragma: nocover
        @doc(os.path.splitunc)
        def splitunc(self):
            return os.path.splitunc(self)

    @doc(os.access)
    def access(self, *args, **kw):
        return os.access(self, *args, **kw)

    @doc(os.chdir)
    def chdir(self):
        return os.chdir(self)

    @contextmanager
    def cd(self):
        cwd = os.getcwd()
        try:
            self.chdir()
            yield self
        finally:
            os.chdir(cwd)

    @doc(os.chmod)
    def chmod(self, *args, **kw):
        return os.chmod(self, *args, **kw)

    def list(self, filterfn=lambda x: True):
        """Return all direct descendands of directory `self` for which
           `filterfn` returns True.
        """
        return [self / p for p in self.listdir() if filterfn(self / p)]

    @doc(os.listdir)
    def listdir(self):
        return [Path(p) for p in os.listdir(self)]

    def subdirs(self):
        """Return all direct sub-directories.
        """
        return self.list(lambda p: p.isdir())

    def iterdir(self):
        if not self.isdir():
            raise OSError(errno=errno.ENOTDIR)
        return iter(self.subdirs())

    def files(self):
        """Return all files in directory.
        """
        return self.list(lambda p: p.isfile())

    @doc(os.lstat)
    def lstat(self):
        return os.lstat(self)

    @doc(os.makedirs)
    def makedirs(self, path=None, mode=0o777):
        pth = os.path.join(self, path) if path else self
        try:
            os.makedirs(pth, mode)
        except OSError:
            pass
        return Path(pth)

    @doc(os.mkdir)
    def mkdir(self, path, mode=0o777):
        pth = os.path.join(self, path)
        os.mkdir(pth, mode)
        return Path(pth)

    @doc(os.remove)
    def remove(self):
        return os.remove(self)

    def rm(self, fname=None):
        """Remove a file, don't raise exception if file does not exist.
        """
        if fname is not None:
            return (self / fname).rm()
        try:
            self.remove()
        except OSError:
            pass

    @doc(os.removedirs)
    def removedirs(self):
        return os.removedirs(self)

    @doc(shutil.move)
    def move(self, dst):
        return shutil.move(self, dst)

    @doc(os.rename)
    def rename(self, *args, **kw):
        return os.rename(self, *args, **kw)

    @doc(os.renames)
    def renames(self, *args, **kw):
        return os.renames(self, *args, **kw)

    @doc(os.rmdir)
    def rmdir(self):
        return os.rmdir(self)

    if hasattr(os, 'startfile'):  # pragma: nocover
        @doc(os.startfile)
        def startfile(self, *args, **kw):
            return os.startfile(self, *args, **kw)

    def samefile(self, other):
        """ .. seealso:: :func:`os.path.samefile` """
        if not hasattr(os.path, 'samefile'):
            other = Path(other).realpath().normpath().normcase()
            return self.realpath().normpath().normcase() == other
        return os.path.samefile(self, other)

    @doc(os.stat)
    def stat(self, *args, **kw):
        return os.stat(self, *args, **kw)

    @doc(os.utime)
    def utime(self, time=None):
        os.utime(self, time)
        return self.stat()

    def __add__(self, other):
        return Path(str(self) + str(other))


Path._flavour = Path


@contextmanager
def cd(pth):
    cwd = os.getcwd()
    try:
        os.chdir(pth)
        yield
    finally:
        os.chdir(cwd)
