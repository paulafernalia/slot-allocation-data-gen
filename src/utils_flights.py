#!/usr/bin/env python
"""
This script contains support functions for generate.py and visualise.py scripts
"""

import numpy as np
import utils_dates
import utils_times


dom_airports = ["ZZJ", "ZZD"]


def get_count_flights(start_date_str, end_date_str, freq):
    """
        For a given service (row), select all days between start and end data
        that match the days of the week given in the frequency field.
        Return a list of all selected dates for each service.
    """
    start_date = utils_dates.str_to_date(start_date_str)
    end_date = utils_dates.str_to_date(end_date_str)

    weekdays = utils_dates.freq_str_to_weekdays(freq)
    start_weekday = start_date.weekday()

    # Calculate intervals to add these movements
    day_count = 0
    for day in range((end_date - start_date).days + 1):
        if (start_weekday + day) % 7 + 1 in weekdays:
            day_count += 1

    return day_count


def is_linked(turnCarrier):
    """
        Checks whether a request is linked
    """
    if turnCarrier == "":
        return False

    return True


def get_opposite_arr_dep(arr_dep):
    """
        If arrDep is A it returns D and viceversa
    """
    if arr_dep == "A":
        return "D"

    return "A"


def is_domestic(orig_dest):
    """
        Checks whether a request is domestic
    """
    if orig_dest in dom_airports:
        return True

    return False


def is_compatible(flight, cap_lim):
    """
        Checks if a request is relevant for a given capacity constraint
    """
    if cap_lim["ArrDep"] != "T" and flight["ArrDep"] != cap_lim["ArrDep"]:
        return False

    if cap_lim["Resource"] == "P" and flight["Seats"] == 0:
        return False

    flight_dom_int = "D" if is_domestic(flight["OrigDest"]) else "I"

    if cap_lim["DomInt"] != "T" and flight_dom_int != cap_lim["DomInt"]:
        return False

    return True


def get_relevant_time_idx_from_min(flight_minutes, cap_lim):
    """
        Get starting time of relevant constraint for a given slot
    """
    relevant_time_idx = []

    for j, time in enumerate(cap_lim["Time"]):
        if time + cap_lim["Duration"] - 1 < flight_minutes:
            continue

        if time > flight_minutes:
            break

        relevant_time_idx.append(j)

    return relevant_time_idx


def get_relevant_time_idx_from_flight(flight_row, cap_lim):
    """
        Get starting time of relevant constraint for a given slot taken
        from the flight dep/arr time
    """
    hour, minute = utils_times.str_to_time(flight_row["Req"])
    minutes = hour * 60 + minute

    relevant_time_idx = get_relevant_time_idx_from_min(minutes, cap_lim)

    return relevant_time_idx


def get_initial_demand(schedule_df, cap_lims):
    """
        Populate dictionaries with demand curves for each capacity constraint
        using times given in "Time" field of each request
    """
    first_date, last_date = utils_dates.get_first_last_dates(schedule_df)

    # Initialise demand data structure
    demand = [0 for elem in range(len(cap_lims))]
    for c_idx, cap_lim in enumerate(cap_lims):
        limit_size = np.zeros(len(cap_lim["Time"]))
        demand[c_idx] = dict()

        # Initialise demand as all zeros for all c, j, d
        for date in utils_dates.date_range(first_date, last_date):
            demand[c_idx][utils_dates.date_to_str(date)] = limit_size.copy()

    # Get valid dates for each flight
    schedule_df["valid_dates"] = schedule_df.apply(
        lambda x: utils_dates.select_dates(x), axis=1)

    for c_idx, cap_lim in enumerate(cap_lims):
        # Get subset of flights compatible with this capacity constraint
        compat = schedule_df.apply(lambda x: is_compatible(x, cap_lim), axis=1)
        subset_df = schedule_df[compat]

        # Get relevant times for each flight
        relevant_time_idx = subset_df.apply(
            lambda x: get_relevant_time_idx_from_flight(x, cap_lim), axis=1)

        # For each flight
        for i_idx, flight_row in subset_df.iterrows():
            # Define resource to add
            if cap_lim["Resource"] == 'P':
                if "Pax" not in flight_row.index:
                    resource = int(flight_row["Seats"] * 0.88)
                else:
                    resource = flight_row["Pax"]
            elif cap_lim["Resource"] == 'M':
                resource = 1

            # For each date
            for date in flight_row["valid_dates"]:
                # For each time
                for j_idx in relevant_time_idx[i_idx]:
                    date_str = utils_dates.date_to_str(date)
                    demand[c_idx][date_str][j_idx] += resource

    schedule_df.drop("valid_dates", axis=1)

    return demand


def get_percentile_demand(demand, percentile_q):
    """
        Get the qth percentile of all demand points corresponding to each
        capacity constraint
    """
    percentiles = []

    for _, elem_c in enumerate(demand):

        limits = []
        for _, elem_d in elem_c.items():
            # assert elem_d.sum() > 0
            limits.extend(list(elem_d))

        percentiles.append(np.percentile(limits, percentile_q))

    return percentiles
