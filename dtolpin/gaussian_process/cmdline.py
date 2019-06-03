"""Command line entry points.
"""

import argparse
from . import __version__


def hello():
    """ Hello world sample entry point.
    """
    print("hello world version {}".format(__version__))


def gdbye():
    """ Goodbye sample entry point.
    """
    print("Goodbye version {}".format(__version__))
