#!/usr/bin/env python
"""
This script cleans output files in capacity, demand, metadata and reports
folders
"""

import os


def main():
    """
        Clean output files (demand, capacity, metadata and reports)
    """
    # Get schedule files
    for folder in ["demand", "capacity", "reports", "metadata"]:
        dirpath = os.path.join(os.getcwd(), "schedules", folder)

        if not os.path.exists(dirpath):
            continue

        filenames = [f for f in os.listdir(dirpath) if is_file(f, dirpath)]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            os.remove(filepath)


def is_file(filename, dir_):
    """
        Check if a file in a given directory is actually a file
    """
    filepath = os.path.join(dir_, filename)
    if not os.path.isfile(filepath):
        return False
    if "DS_Store" in filename:
        return False
    return True


if __name__ == "__main__":
    main()
