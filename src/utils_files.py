#!/usr/bin/env python
"""
This script contains support functions for generate.py and visualise.py scripts
"""

import os
import errno


def mkdir_p(path):
    """
        Make a directory if is doesn't exist
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_open(path):
    """
        Open "path" for writing, creating any parent directories as needed.
    """
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')
