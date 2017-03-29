# -*- coding: utf-8 -*-
"""Check if contents of directory has changed.
"""
import argparse
import os
import hashlib
from .listfiles import list_files
from .path import Path


def digest(dirname, glob=None):
    """Returns the md5 digest of all interesting files (or glob) in `dirname`.
    """
    md5 = hashlib.md5()
    if glob is None:
        fnames = [fname for _, fname in list_files(Path(dirname))]
        for fname in sorted(fnames):
            fname = os.path.join(dirname, fname)
            md5.update(open(fname, 'rb').read())
    else:
        fnames = Path(dirname).glob(glob)
        for fname in sorted(fnames):
            md5.update(fname.open('rb').read())
    return md5.hexdigest()


def changed(dirname, filename='.md5', args=None, glob=None):
    """Has `glob` changed in `dirname`

    Args:
        dirname: directory to measure
        filename: filename to store checksum
    """
    root = Path(dirname)
    if not root.exists():
        # if dirname doesn't exist it is changed (by definition)
        return True

    cachefile = root / filename
    current_digest = cachefile.open().read() if cachefile.exists() else ""
    
    _digest = digest(dirname, glob=glob)
    if args and args.verbose:  # pragma: nocover
        print "md5:", _digest
    has_changed = current_digest != _digest

    if has_changed:
        with open(os.path.join(dirname, filename), 'w') as fp:
            fp.write(_digest)

    return has_changed


class Directory(Path):
    def changed(self, filename='.md5', glob=None):
        if glob is not None:
            filename += '.glob-' + ''.join(ch.lower()
                                           for ch in glob if ch.isalpha())
        return changed(self, filename, glob=glob)


def main():  # pragma: nocover
    p = argparse.ArgumentParser()
    p.add_argument(
        'directory',
        help="Directory to check"
    )
    p.add_argument(
        '--verbose', '-v', action='store_true',
        help="increase verbosity"
    )
    args = p.parse_args()

    import sys
    _changed = changed(sys.argv[1], args=args)
    sys.exit(_changed)


if __name__ == "__main__":  # pragma: nocover
    main()
