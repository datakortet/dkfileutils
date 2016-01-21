# -*- coding: utf-8 -*-
"""Poor man's pathlib.

   (Path instances are subclasses of str, so interoperability with existing
   os.path code is greater than with Python 3's pathlib.)
"""
# pylint:disable=C0111,R0904
# R0904: too many public methods in Path
import os
import re


def doc(srcfn):
    def decorator(fn):
        fn.__doc__ = srcfn.__doc__.replace(srcfn.__name__, fn.__name__)
        return fn
    return decorator


class Path(str):
    """Poor man's pathlib.
    """

    def __div__(self, other):
        return Path(os.path.join(self, other))

    @doc(os.unlink)
    def unlink(self):
        os.unlink(self)

    def open(self, mode='r'):
        return open(self, mode)

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
        super(Path, self).__contains__(item)

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

    @doc(os.path.split)
    def split(self, **kwargs):
        return os.path.split(self)

    def parts(self):
        return re.split(r"\\|/", self)

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

    @doc(os.chmod)
    def chmod(self, *args, **kw):
        return os.chmod(self, *args, **kw)

    @doc(os.listdir)
    def listdir(self):
        return [Path(p) for p in os.listdir(self)]

    def list(self, filterfn=lambda x: True):
        """Return all direct descendands of directory `self` for which
           `filterfn` returns True.
        """
        return [self / p for p in self.listdir() if filterfn(self / p)]

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
    def makedirs(self, path, mode=0777):
        pth = os.path.join(self, path)
        try:
            os.makedirs(pth, mode)
        except OSError:
            pass
        return Path(pth)

    @doc(os.mkdir)
    def mkdir(self, path, mode=0777):
        pth = os.path.join(self, path)
        os.mkdir(pth, mode)
        return Path(pth)

    @doc(os.remove)
    def remove(self):
        return os.remove(self)

    @doc(os.removedirs)
    def removedirs(self):
        return os.removedirs(self)

    @doc(os.rename)
    def rename(self, *args, **kw):
        return os.rename(self, *args, **kw)

    @doc(os.renames)
    def renames(self, *args, **kw):
        return os.renames(self, *args, **kw)

    @doc(os.rmdir)
    def rmdir(self):
        return os.rmdir(self)

    if hasattr(os, 'startfile'):
        @doc(os.startfile)
        def startfile(self, *args, **kw):
            return os.startfile(self, *args, **kw)

    @doc(os.stat)
    def stat(self, *args, **kw):
        return os.stat(self, *args, **kw)

    @doc(os.utime)
    def utime(self, *args, **kw):
        return os.utime(self, *args, **kw)

    # def __getattr__(self, attr):
    # if hasattr(os.path, attr):
    #         a = getattr(os.path, attr)
    #         if inspect.isfunction(a):
    #             return lambda *args, **kwargs: a(self, *args, **kwargs)
    #     raise AttributeError(attr)
