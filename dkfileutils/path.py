# -*- coding: utf-8 -*-
"""Poor man's pathlib.

   (Path instances are subclasses of str, so interoperability with existing
   os.path code is greater than with Python 3's pathlib.)
"""
# pylint:disable=C0111,R0904
# R0904: too many public methods in Path
from __future__ import print_function
import os
import re
from contextlib import contextmanager
import shutil

from typing import BinaryIO, Text, Union


def doc(srcfn):
    def decorator(fn):
        if srcfn.__doc__ is None:
            fn.__doc__ = None
        else:
            fn.__doc__ = srcfn.__doc__.replace(srcfn.__name__, fn.__name__)
        return fn
    return decorator


class Path(str):
    """Poor man's pathlib.
    """

    def __new__(cls, *args, **kw):
        if isinstance(args[0], Path):
            return str.__new__(cls, str(args[0]), **kw)
        else:
            return str.__new__(cls, os.path.normcase(args[0]), **kw)

    def __div__(self, other):   # type: (Union[Path, Text]) -> Path
        return Path(
            os.path.normcase(
                os.path.normpath(
                    os.path.join(self, other)
                )
            )
        )
    __truediv__ = __div__

    @doc(os.unlink)
    def unlink(self):   # type: () -> None
        os.unlink(self)

    def open(self, mode='r'):   # type: (str) -> BinaryIO
        return open(str(self), mode)

    def read(self, mode='r'):   # type: (str) -> Text
        with self.open(mode) as fp:
            return fp.read()

    def write(self, txt, mode='w'):
        with self.open(mode) as fp:
            fp.write(txt)

    def append(self, txt, mode='a'):
        with self.open(mode) as fp:
            fp.write(txt)

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
        # print '\n\npat', pat
        # print 'regex:', r
        # print [s.relpath(self).replace('\\', '/') for s in self]
        rx = re.compile(r)

        def match(d):
            m = rx.match(d)
            return not m if negate else m

        return [s for s in self if match(s.relpath(self).replace('\\', '/'))]

    @doc(os.path.abspath)
    def abspath(self):
        return Path(os.path.abspath(self))
    absolute = abspath  # pathlib

    def drive(self):
        """Return the drive of `self`.
        """
        return self.splitdrive()[0]

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

    @doc(os.path.isfile)
    def isfile(self):
        return os.path.isfile(self)

    @doc(os.path.islink)
    def islink(self):
        return os.path.islink(self)

    @doc(os.path.ismount)
    def ismount(self):
        return os.path.ismount(self)

    @doc(os.path.join)
    def join(self, *args):
        return Path(os.path.join(self, *args))

    @doc(os.path.lexists)
    def lexists(self):
        return os.path.lexists(self)

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

    def path_to(self, other):
        """The reverse of relpath.
        """
        return Path(os.path.relpath(str(other), str(self)))

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
        parts = self.abspath().normpath().normcase().parts()
        for i in range(1, len(parts)):
            yield Path(os.path.join(*parts[:-i]))

    @property
    def parents(self):
        return list(self.parent_iter())

    @property
    def parent(self):
        return self.parents[0]

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

    @doc(os.stat)
    def stat(self, *args, **kw):
        return os.stat(self, *args, **kw)

    @doc(os.utime)
    def utime(self, time=None):
        os.utime(self, time)
        return self.stat()

    def __add__(self, other):
        return Path(str(self) + str(other))


@contextmanager
def cd(pth):
    cwd = os.getcwd()
    try:
        os.chdir(pth)
        yield
    finally:
        os.chdir(cwd)
