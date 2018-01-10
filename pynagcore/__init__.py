# -*- name: pynagcore -*-

"""
pynagcore: Framework for basic Nagios Core command handling.
"""

def _checkPython():
    # Only support tested version of Python
    import sys

    version = getattr(sys, "version_info", (0,))
    if version < (2, 7):
        raise ImportError("PyNagCore requires Python 2.7 or later.")
    elif version >= (3, 0) and version < (3, 3):
        raise ImportError("PyNagCore on Python 3 requires Python 3.3 or later.")

_checkPython()

# setup version
from pynagcore._version import __version__ as version
__version__ = version.short()
