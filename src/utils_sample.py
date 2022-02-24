#!/usr/bin/env python
"""
This script contains support functions for generate.py and visualise.py scripts
"""

import numpy as np
import utils_times


np.random.seed(seed=42)


def sample_par_from_list(probs, size=1, replace=False):
    """
        Take a parameter or multiple parameters, with or without replacement,
        at random from a list of possible options
    """
    idx = np.arange(len(probs))

    # Ensure probabilities add up to 1
    probs = np.array(probs)
    probs /= probs.sum()

    return np.random.choice(idx, size=size, p=probs, replace=replace)


def sample_par_from_dict(dict_, size=1, replace=False):
    """
        Take a parameter or multiple parameters, with or without replacement,
        at random from a dictionary of possible options
    """
    probs = np.array(list(dict_.values()))

    # Ensure probabilities add up to 1
    probs = probs / probs.sum()

    choices = list(dict_.keys())

    # Chose size elements from the keys
    return np.random.choice(choices, size=size, p=probs, replace=replace)


def sample_num_days(parameters):
    """
        Sample parameter indicating number of days in the schedule
    """
    profile = parameters["schedule_size"]
    return np.random.randint(profile["min_days"], profile["max_days"])


def sample_dom_int_proportion(parameters):
    """
        Sample parameter indicating proportion of domestic/international flights
    """
    profile = parameters["dom_req"]
    return np.random.uniform(profile["min_p"], profile["max_p"])


def sample_slf(parameters):
    """
        Sample profile with seat load factor distributions
    """
    profile = parameters["seat_load_factor"]
    return sample_par_from_dict(profile)[0]


def sample_seats(parameters):
    """
        Sample number of seats in the flight from uniform distribution between
        limits specified in parameters["seats"]
    """
    profile = parameters["seats"]
    seats = sample_par_from_dict(profile)[0]

    return int(seats)


def sample_flight_time(parameters, arr_dep):
    """
        Sample hour in 5-minute buckets
    """

    profile = parameters["daily_demand"]
    assert 1440 % len(profile[arr_dep]) == 0

    interval_len = 288 / len(profile[arr_dep])
    minutes = sample_par_from_list(profile[arr_dep])[0] * interval_len * 5

    minutes = minutes + np.random.randint(0, interval_len) * 5

    # Correct if it goes to following day
    assert minutes // (288 * 5) == 0

    hour = int(minutes // 60)
    minute = int(minutes % 60)

    assert minute % 5 == 0
    assert 0 <= hour <= 23

    return hour, minute


def sample_weekdays(parameters):
    """
        Sample frequency of request
    """

    # Generate number of weekdays
    profile = parameters["weeklyfreq_a"]
    num_weekdays = sample_par_from_dict(profile)[0]

    # Generate specific days of the week
    profile = parameters["weeklyfreq_b"]
    weekdays = sample_par_from_dict(profile, size=num_weekdays)

    return weekdays


def sample_start_end_week(parameters, first_week):
    """
        Sample first and last week of a request
    """

    # Generate number of weeks in the request
    profile = parameters["start_end_weeks"]
    startend_str = sample_par_from_dict(profile)[0]

    start, end = startend_str.split(",")
    rel_start = int(start) - first_week
    rel_end = int(end) - first_week

    assert rel_start >= 0
    assert rel_end >= rel_start

    return rel_start, rel_end


def sample_total_demand(parameters):
    """
        Sample parameter indicating total number of ops in the schedule
    """
    out = 1000 * np.random.randint(
        parameters["season_demand"]["min_k"],
        parameters["season_demand"]["max_k"])

    return out


def is_flight_linked(parameters):
    """
        Sample parameter indicating whether a request is linked
    """
    profile = parameters["proportion_linked"]
    return np.random.binomial(1, profile) * .5


def is_flight_domestic(parameters):
    """
        Sample parameter indicating whether a request is domestic
    """
    profile = parameters["dom_req"]
    return np.random.binomial(1, profile)


def generate_turn_time(flight, parameters):
    """
        Sample parameter indicating turnaround time requested
    """
    profile = parameters["turn_times"]
    ground_time = sample_par_from_dict(profile)[0]

    if flight["ArrDep"] == "D":
        ground_time *= -1
    linked_time_str = utils_times.add_minutes_to_time(
        flight["Req"], ground_time)

    linked_hour, _ = utils_times.str_to_time(linked_time_str)
    init_hour, _ = utils_times.str_to_time(flight["Req"])

    if flight["ArrDep"] == "D" and linked_hour > init_hour:
        return None

    if flight["ArrDep"] == "A" and linked_hour < init_hour:
        return None

    return linked_time_str


def choose_profiles(parameters):
    """
        Choose one option from all options available for each parameter
        required to generate data
    """
    instance_profiles = dict()
    filtered_params = dict()
    non_profile_fields = [
        "schedule_size", "season_demand", "seat_load_factor",
        "capacity_ratios", "dom_req"
    ]

    for key, value in parameters.items():
        if key not in non_profile_fields:
            instance_profiles[key] = np.random.choice(list(value.keys()))
            filtered_params[key] = parameters[key][instance_profiles[key]]
        else:
            filtered_params[key] = parameters[key]

    filtered_params["dom_req"] = sample_dom_int_proportion(parameters)

    return filtered_params


def sample_terminal(parameters):
    """
        Sample terminal number
    """
    return np.random.choice(parameters["Terminals"])
