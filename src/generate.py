#!/usr/bin/env python
"""
This script generates N pairs of capacity and demand files in csv format, where
N is an integer provided by the user as an argument when calling the script
"""


import datetime
import os
import sys
import yaml
import numpy as np
import pandas as pd
import utils_dates
import utils_times
import utils_flights
import utils_sample
import utils_cap
import utils_files


np.random.seed(seed=42)

# Create start and end date
SEASON_START = datetime.datetime(2020, 3, 29)
SEASON_END = datetime.datetime(2020, 10, 24)
FIRST_WEEK = SEASON_START.isocalendar()[1] - (SEASON_START.isoweekday() < 1)
LAST_WEEK = SEASON_END.isocalendar()[1] - (SEASON_END.isoweekday() < 1)


def main():
    """
    Main function to generate synthetic data
    """

    # Number of schedules to generate
    if len(sys.argv) == 1:
        num_schedules = 50
    else:
        num_schedules = int(sys.argv[1])

    with open("parameters.yml") as stream:
        try:
            params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    for j in range(num_schedules):
        print(f"\nSchedule {j}")
        # Choose profiles
        schedule_params = utils_sample.choose_profiles(params)

        # Generate schedule
        dem_dict, schedule_params = generate_schedule(schedule_params)

        dem_df = pd.DataFrame(dem_dict)

        filename = "I" + str(j).zfill(4) + "_demand.csv"
        print(f" - {filename}")

        filedir = os.path.join('schedules', 'demand')
        is_exist = os.path.exists(filedir)
        if not is_exist:
            # Create a new directory because it does not exist
            os.makedirs(filedir)
            print(f"New directory {filedir} created")

        filepath = os.path.join(filedir, filename)
        dem_df.to_csv(filepath, index=None)

        cap_lims, schedule_params = generate_cap_output(schedule_params, dem_df)
        cap_df = utils_cap.cap_lims_to_df(cap_lims)

        # Export capacity file
        filename = "I" + str(j).zfill(4) + "_capacity.csv"
        filedir = os.path.join('schedules', 'capacity')
        is_exist = os.path.exists(filedir)
        if not is_exist:
            # Create a new directory because it does not exist
            os.makedirs(filedir)
            print(f"New directory {filedir} created")

        filepath = os.path.join(filedir, filename)
        cap_df.to_csv(filepath, index=None)

        # Export metadata
        filename = "I" + str(j).zfill(4) + "_metadata.yml"
        filedir = os.path.join('schedules', 'metadata')
        is_exist = os.path.exists(filedir)
        if not is_exist:
            # Create a new directory because it does not exist
            os.makedirs(filedir)
            print(f"New directory {filedir} created")

        filepath = os.path.join(filedir, filename)
        with utils_files.safe_open(filepath) as outfile:
            yaml.dump(schedule_params, outfile, default_flow_style=False)


def generate_schedule(params):
    """
        Generate a single schedule using distributions given in params
    """
    # Generate total demand
    total_demand = utils_sample.sample_total_demand(params)
    params["total_demand"] = total_demand

    n_terminals = int(np.ceil(total_demand / 80000))
    params["Terminals"] = [f"Term{i + 1}" for i in range(n_terminals)]

    # Initialise number of flights to 0
    flight_requests = 0
    slot_requests = 0

    # Generate flights
    flight_list = []

    while True:
        # Generate flight
        flight = generate_single_request(params)

        # Assign id and update number of requests created
        flight["FlNum"] = str(slot_requests).zfill(5)
        slot_requests += 1
        flight_requests += flight["NoOps"]

        # Check if turnaround flight needs to be created
        is_linked = utils_sample.is_flight_linked(params)

        if is_linked:
            # Generate turnaround flight
            turn_fl = generate_turn_flight(flight, params)

            if turn_fl is not None:
                # Assign id and update number of requests created
                turn_fl["FlNum"] = str(slot_requests).zfill(5)

                # Link flights
                turn_fl["TurnCarrier"] = flight["Carrier"]
                flight["TurnCarrier"] = turn_fl["Carrier"]
                turn_fl["TurnFlNum"] = flight["FlNum"]
                flight["TurnFlNum"] = turn_fl["FlNum"]

                slot_requests += 1
                flight_requests += flight["NoOps"]
                flight_list.append(turn_fl)

        flight_list.append(flight)

        # Stop when we reach total demand
        if flight_requests >= total_demand:
            break

    # Truncate schedule to adjust it to the chosen number of days
    trunc_flight_list, trunc_demand = truncate_schedule(flight_list, params)
    assert trunc_demand <= flight_requests

    return trunc_flight_list, params


def truncate_schedule(flight_list, params):
    num_days = utils_sample.sample_num_days(params)

    # Get last valid date
    end_date = SEASON_START + datetime.timedelta(days=num_days - 1)

    trunc_flight_list = []
    trunc_demand = 0

    for flight in flight_list:
        flight_start_date = utils_dates.str_to_date(flight["StartDate"])

        # If this flight has some date included in the selected period
        if flight_start_date <= end_date:

            flight_end_date = utils_dates.str_to_date(flight["EndDate"])
            if end_date < flight_end_date:
                flight["EndDate"] = utils_dates.date_to_str(end_date)

                flight["NoOps"] = utils_flights.get_count_flights(
                    flight["StartDate"], flight["EndDate"], flight["FREQ"])

            trunc_flight_list.append(flight)
            trunc_demand += flight["NoOps"]

    return trunc_flight_list, trunc_demand


def generate_turn_flight(flight, parameters):
    # Create copy of original flight
    turn_fl = flight.copy()

    # Assign unique id and update number of requests created
    turn_fl["ArrDep"] = utils_flights.get_opposite_arr_dep(flight["ArrDep"])
    turn_fl["Req"] = utils_sample.generate_turn_time(flight, parameters)

    if turn_fl["Req"] is None:
        return None

    return turn_fl


def generate_single_request(parameters):
    flight = dict()

    weekdays = utils_sample.sample_weekdays(parameters)
    flight['FREQ'] = utils_dates.weekdays_to_freq_str(weekdays)

    # Populate unused fields
    flight["Carrier"] = "ZZ"
    flight["Airport"] = "ZZ2"
    flight["Season"] = "S20"
    flight["ServType"] = "J"

    flight["Term"] = utils_sample.sample_terminal(parameters)

    if utils_sample.is_flight_domestic(parameters):
        flight["OrigDest"] = "ZZD"
    else:
        flight["OrigDest"] = "ZZI"

    # Generate start and end week
    start_week, end_week = utils_sample.sample_start_end_week(
        parameters, FIRST_WEEK)

    # Generate start and end dates
    start_date, end_date = utils_dates.week_limits_to_dates(
        start_week, end_week, weekdays, SEASON_START, SEASON_END,
        LAST_WEEK - FIRST_WEEK - 1)
    flight["StartDate"] = utils_dates.date_to_str(start_date)
    flight["EndDate"] = utils_dates.date_to_str(end_date)

    # Select number of seats
    seats = utils_sample.sample_seats(parameters)
    flight["Seats"] = seats

    # Select number of passengers
    slf = utils_sample.sample_slf(parameters)
    flight["Pax"] = int(flight["Seats"] * slf)

    # Select arrival or departure
    arr_dep = np.random.choice(["A", "D"])
    flight["ArrDep"] = arr_dep

    # Select flight time
    hour, min_ = utils_sample.sample_flight_time(parameters, arr_dep)
    flight["Req"] = utils_times.time_to_str(hour, min_)

    # Get number of operations
    flight["NoOps"] = utils_flights.get_count_flights(
        flight["StartDate"], flight["EndDate"], flight['FREQ'])

    flight["TurnCarrier"] = ""
    flight["TurnFlNum"] = ""

    return flight


def generate_cap_output(parameters, schedule_df):

    terminals = np.unique(schedule_df["Term"]).tolist()
    cap_lims = []

    # Define types of capacity restrictions
    for elem in parameters["capacity"]:
        times = [k * elem[4] for k in range(int(24 * 60 / elem[4]))]

        # If the resource is the runway, add one capacity constraint
        if elem[0] == "M":
            cap_lims.append(
                {"Resource": elem[0],
                 "ArrDep": elem[1],
                 "DomInt": elem[2],
                 "Duration": elem[3],
                 "Limit": None,
                 "Terminal": "",
                 "Time": times})

        else:
            # Otherwise, repeat this capacity constraint for every terminal
            for term in terminals:
                cap_lims.append(
                    {"Resource": elem[0],
                     "ArrDep": elem[1],
                     "DomInt": elem[2],
                     "Duration": elem[3],
                     "Limit": None,
                     "Terminal": str(term),
                     "Time": times})

    # Get demand for each capacity limit
    demand = utils_flights.get_initial_demand(schedule_df, cap_lims)

    # Choose level of cap-dem imbalance
    perc99s = utils_flights.get_percentile_demand(demand, 99)

    # Reset capacity parameters and use extended information
    parameters["capacity"] = []

    for c_idx, cap_lim in enumerate(cap_lims):
        min_q = parameters["capacity_ratios"]["min"]
        max_q = parameters["capacity_ratios"]["max"]

        cap_lim["random_level"] = np.random.uniform(min_q, max_q)
        limit = int(np.ceil(perc99s[c_idx] * cap_lim["random_level"]))

        if cap_lim["Resource"] == 'M':
            limit = max(limit, 2)
        else:
            assert cap_lim["Resource"] == 'P'
            limit = max(limit, 500)

        cap_lim["Limit"] = (np.ones(len(cap_lim["Time"])) * limit).tolist()

        # Add to schedule parameters
        parameters["capacity"].append(cap_lim)

    return cap_lims, parameters


if __name__ == "__main__":
    main()
