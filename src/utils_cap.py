#!/usr/bin/env python
"""
This script contains support functions for generate.py and visualise.py scripts
"""

import pandas as pd
import utils_times


def cap_lims_to_df(cap_lims):
    capacity_dicts = list()

    for c_idx, cap_lim in enumerate(cap_lims):
        for limit, time in zip(cap_lim["Limit"], cap_lim["Time"]):
            assert cap_lim["Resource"] == 'P' or cap_lim["Resource"] == 'M'

            resource = "Terminal" if cap_lim["Resource"] == 'P' else "Runway"

            capacity_dicts.append({
                "Constraint": c_idx,
                "Resource": resource,
                "ArrDep": cap_lim["ArrDep"],
                "Duration": cap_lim["Duration"],
                "Limit": int(limit),
                "Time": int(utils_times.time_to_str(time // 60, time % 60)),
                "DomInt": cap_lim["DomInt"],
                "Terminal": cap_lim["Terminal"]
            })

            assert resource != "Runway" or cap_lim["Terminal"] == ""

    capacity_df = pd.DataFrame(capacity_dicts)

    return capacity_df


def df_to_cap_lims(cap_df):
    cap_lims = []
    cap_dict = dict()
    cap_dict["Constraint"] = ""

    for _, row in cap_df.iterrows():
        # If we are still exploring the same capacity limit
        if row["Constraint"] == cap_dict["Constraint"]:
            cap_dict["Limit"].append(row["Limit"])

            hour, minute = utils_times.str_to_time(row["Time"])
            cap_dict["Time"].append(hour * 60 + minute)

        # If we start a new capacity limit
        else:
            # Add previous one to list
            if cap_dict["Constraint"] != "":
                cap_lims.append(cap_dict.copy())

            # Restart the dictionary
            cap_dict["Constraint"] = row["Constraint"]

            assert row["Resource"] == "Runway" or row["Resource"] == "Terminal"

            resource = "M" if row["Resource"] == "Runway" else "P"
            cap_dict["Resource"] = resource

            cap_dict["ArrDep"] = row["ArrDep"]
            cap_dict["Duration"] = row["Duration"]
            cap_dict["DomInt"] = row["DomInt"]

            terminal = "" if pd.isna(row["Terminal"]) else row["Terminal"]
            cap_dict["Terminal"] = terminal

            cap_dict["Limit"] = []
            cap_dict["Time"] = []

    return cap_lims
