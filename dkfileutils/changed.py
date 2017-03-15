# -*- coding: utf-8 -*-
"""Check if contents of directory has changed.
"""
import argparse
import os
import hashlib
from .listfiles import list_files
from .path import Path


def digest(dirname):
    """Returns the md5 digest of all interesting files in `dirname`.
    """
    md5 = hashlib.md5()
    fnames = [fname for _, fname in list_files(Path(dirname))]
    for fname in sorted(fnames):
        md5.update(open(os.path.join(dirname, fname), 'rb').read())
    return md5.hexdigest()


def changed(dirname, filename='.md5', args=None):
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
    
    _digest = digest(dirname)
    if args and args.verbose:  # pragma: nocover
        print "md5:", _digest
    has_changed = current_digest != _digest

    if has_changed:
        with open(os.path.join(dirname, filename), 'w') as fp:
            fp.write(_digest)

    return has_changed


class Directory(Path):
    def changed(self, filename='.md5'):
        return changed(self, filename)


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
