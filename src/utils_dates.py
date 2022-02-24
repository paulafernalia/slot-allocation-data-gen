#!/usr/bin/env python
"""
This script contains support functions for generate.py and visualise.py scripts
"""

import numpy as np
import datetime


def weekdays_to_freq_str(weekdays):
    wkd_nums = [weekname_to_num_mon_1_sun_7(d) for d in weekdays]
    out = ''.join([str(d) if d in wkd_nums else '0' for d in np.arange(1, 8)])
    assert len(out) > 0
    return out


def freq_str_to_weekdays(freq_string):
    if isinstance(freq_string, (float, int)):
        freq_string = str(freq_string)

    return np.array([int(d) for d in freq_string if d != '0'])


def date_to_str(date):
    return date.strftime("%d-%b-%y")


def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%d-%b-%y")


def weekname_to_num_mon_1_sun_7(day_str):
    weekday_dict = {
        "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4,
        "Fri": 5, "Sat": 6, "Sun": 7}

    return weekday_dict[day_str]


def weekname_to_num_mon_1_sun_0(day_str):
    weekday_dict = {
        "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4,
        "Fri": 5, "Sat": 6, "Sun": 0}

    return weekday_dict[day_str]


def mon_1_sun_0_to_weekname(day_num):
    weekday_dict = {
        1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu",
        5: "Fri", 6: "Sat", 0: "Sun"}

    return weekday_dict[day_num]


def date_range(date1,
               date2):
    """ Function to iterate over dates
        :param date1: first date to iterate over
        :param date2: last date to iterate over
    """

    while date1 <= date2:
        yield date1
        date1 = date1 + datetime.timedelta(days=1)


def select_dates(flight):

    """ For a given service (row), select all days between start and end data
        that match the days of the week given in the frequency field.
        Return a list of all selected dates for each service."""

    dates = []

    start_date = str_to_date(flight["StartDate"])
    end_date = str_to_date(flight["EndDate"])
    flight_weekdays = freq_str_to_weekdays(flight["FREQ"])

    for date in date_range(start_date, end_date):
        date_weekday = datetime.datetime.weekday(date) + 1

        if date_weekday in flight_weekdays:
            dates.append(date)

    return dates


def week_limits_to_dates(start_week,
                         end_week,
                         weekdays,
                         season_start,
                         season_end,
                         num_weeks):

    weekday_nums = [weekname_to_num_mon_1_sun_0(d) for d in weekdays]
    weekday_nums_sun7 = [weekname_to_num_mon_1_sun_7(d) for d in weekdays]

    # Get start and end week
    start_week_date = season_start + datetime.timedelta(weeks=start_week)
    end_week_date = season_start + datetime.timedelta(
        weeks=min(num_weeks, end_week))

    start_delta = int(min(weekday_nums))
    start_date = start_week_date + datetime.timedelta(days=start_delta)

    end_delta = int(max(weekday_nums))
    end_date = end_week_date + datetime.timedelta(days=end_delta)

    assert end_date >= start_date

    assert start_date.weekday() + 1 in weekday_nums_sun7
    assert end_date.weekday() + 1 in weekday_nums_sun7

    assert start_date >= season_start
    assert end_date <= season_end

    return start_date, end_date


def get_wkday_zero_sunday(weekdays):
    """
    Take a list of weekdays in format 1-7 and convert sundays to zeros

    Parameters
    ----------
    weekdays : ndarray
        1D array containing data with ints ranging from 1 to 7

    Returns:
    ----------
    out : ndarray
        1D array containing data with ints ranging from 0 to 6
    """

    # Get start and end date
    out = weekdays.copy()
    out[np.where(out == 7)] = 0

    return out


def get_first_last_dates(schedule_df):
    all_starts = [str_to_date(d) for d in schedule_df["StartDate"]]
    all_ends = [str_to_date(d) for d in schedule_df["EndDate"]]
    first_date = np.min(all_starts)
    last_date = np.max(all_ends)

    return first_date, last_date
