#!/usr/bin/env python
"""
This script contains support functions for generate.py and visualise.py scripts
"""

def time_to_str(hour, minute):
    """
        Converts a pair of integers representing hour and minutes to a string
        'HHMM'
    """
    assert 0 <= hour <= 23
    return str(hour).zfill(2) + str(minute).zfill(2)


def add_minutes_to_time(time_str, delta_minutes):
    """
        Offsets a time in string format by amount given by int delta_minutes
    """
    hour, minutes = str_to_time(time_str)

    initial_minutes = hour * 60 + minutes
    modified_minutes = initial_minutes + delta_minutes

    if modified_minutes >= 24 * 60:
        modified_minutes -= 24 * 60

    if modified_minutes < 0:
        modified_minutes += 24 * 60

    return time_to_str(modified_minutes // 60, modified_minutes % 60)


def str_to_time(time):
    """
        Converts string with time in 'HHMM' format into a pair (hour, minute)
    """
    time_str = str(time).zfill(4)
    hour = int(time_str[:2])
    minute = int(time_str[2:])

    assert 0 <= hour <= 23
    assert 0 <= minute <= 55

    return hour, minute
