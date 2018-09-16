"""dkfileutils - simple, common file utilities.
"""
__version__ = "1.4.2"

from .path import Path

PurePath = Path
PurePosixPath = Path
PureWindowsPath = Path
PosixPath = Path
WindowsPath = Path

_windows_flavour = Path
_posix_flavour = Path

# pathlib conformance
import os, sys
supports_symlinks = True
if os.name == 'nt':
    import nt
    if sys.getwindowsversion()[:2] >= (6, 0):
        # from nt import _getfinalpathname
        supports_symlinks = False
        _getfinalpathname = None
    else:
        supports_symlinks = False
        _getfinalpathname = None
else:
    nt = None
