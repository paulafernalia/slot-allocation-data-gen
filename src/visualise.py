#!/usr/bin/env python
"""
This script generates a report taking all generated instances found in
capacity and demand folders and presenting various distributions of demand
and capacity related parameters
"""

import os
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rc
import utils_flights
import utils_dates
import utils_cap
import utils_times

font = {'size': 8}
rc('font', **font)


def main():
    """
        Main function that takes all generated instances and creates a report
        exploring different demand/capacity distributions for each one
    """
    dirpath = os.path.join(os.getcwd(), "schedules", "demand")
    dem_filenames = [f for f in os.listdir(dirpath) if is_file(f, dirpath)]

    for dem_file in dem_filenames:
        print(dem_file)

        cap_file = dem_file[:-10] + "capacity.csv"

        dem_df = pd.read_csv(os.path.join("schedules", "demand", dem_file))
        cap_df = pd.read_csv(os.path.join("schedules", "capacity", cap_file))

        dem_df = dem_df.replace(np.nan, '', regex=True)

        cap_lims = utils_cap.df_to_cap_lims(cap_df)

        demand = utils_flights.get_initial_demand(dem_df, cap_lims)

        # For each capacity limit
        pdf_file = dem_file[:-10] + "report.pdf"
        pdf_dir = os.path.join('schedules', 'reports')
        is_exist = os.path.exists(pdf_dir)
        if not is_exist:
            # Create a new directory because it does not exist
            os.makedirs(pdf_dir)
            print(f"New directory {pdf_dir} created")

        pdf_path = os.path.join(pdf_dir, pdf_file)

        with PdfPages(pdf_path) as pdf:
            visualise_summary_stats(dem_df, pdf)
            visualise_demand_vs_capacity(demand, cap_lims, pdf)


def is_file(filename, dir_):
    """
        Check whether an item in a directory is a file
    """
    filepath = os.path.join(dir_, filename)
    if not os.path.isfile(filepath):
        return False
    if "DS_Store" in filename:
        return False
    return True


def legend_without_duplicate_labels(axis):
    """
        Create a legend that aggregates repeated handles/labels
    """
    handles, labels = axis.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if
              l not in labels[:i]]

    axis.legend(*zip(*unique))


def visualise_demand_vs_capacity(demand, cap_lims, pdf):
    """
        Plot demand vs. capacity curves for each type of capacity constraint
    """
    xticks = [hour * 2 * 60 for hour in range(12)]
    xticklabels = [f"{hour * 2}h" for hour in range(12)]

    fig, axes = plt.subplots(len(cap_lims), 1, figsize=(8.27,
                             2 * len(cap_lims)), dpi=100)

    for c_idx, cap_lim in enumerate(cap_lims):
        assert cap_lim["Resource"] == "P" or cap_lim["Resource"] == "M"

        res = "T" if cap_lim["Resource"] == "P" else "R"
        frequency = cap_lim["Time"][1] - cap_lim["Time"][0]

        # For each date
        for _, yvals in demand[c_idx].items():
            xvals = []
            for time in cap_lim["Time"]:
                assert time < 288 * 5
                xvals.append(time)

            axes[c_idx].plot(xvals, yvals, label="demand", linewidth=.75,
                             color="royalblue", alpha=0.3)

        axes[c_idx].set_title(c_idx, fontsize=8)
        axes[c_idx].set_xlabel("Time")

        assert res in ("T", "R")
        if res == "T":
            axes[c_idx].set_ylabel("Passengers")
        else:
            axes[c_idx].set_ylabel("Flights")

        # Plot capacity
        axes[c_idx].axhline(y=np.mean(cap_lim["Limit"]), color='salmon',
                            linestyle='-', label="capacity")

        axes[c_idx].set_xticks(xticks)
        axes[c_idx].set_xticklabels(xticklabels)
        axes[c_idx].set_xlim([0, 287 * 5])
        legend_without_duplicate_labels(axes[c_idx])

        if cap_lim["DomInt"] == "D":
            dom_int = "/Dom"
        elif cap_lim["DomInt"] == "I":
            dom_int = "/Int"
        else:
            assert cap_lim["DomInt"] == "T"
            dom_int = ""

        axes[c_idx].set_title(res + str(cap_lim["Duration"]) +
                              "/" + str(frequency) + "/" +
                              cap_lim["ArrDep"] + dom_int)

    fig.tight_layout()
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()

    return fig, axes


def plot_num_weeks(dem_df, ax):
    """
        Plot histogram with distribution of number of weeks per request
    """
    start_dates = pd.to_datetime(dem_df["StartDate"])
    end_dates = pd.to_datetime(dem_df["EndDate"])

    start_week = start_dates.apply(lambda x: int(x.strftime("%U"))).values
    end_week = end_dates.apply(lambda x: int(x.strftime("%U"))).values

    num_weeks = end_week - start_week
    bins = np.arange(0, np.max(num_weeks) + 1)

    num_weeks_distr, _ = np.histogram(num_weeks, bins=bins)
    ax.bar(bins[:-1], num_weeks_distr, color="royalblue")
    ax.set_title("Number of weeks per request")
    ax.set_xlabel("Number of weeks")
    ax.set_ylabel("Number of requests")


def plot_seasonal_demand(dem_df, axis):
    """
        Plot line chart with number of flights in each day in the season
    """
    seasonal_prof = {}

    for _, flight_row in dem_df.iterrows():
        dates = utils_dates.select_dates(flight_row)

        for date in dates:
            datekey = str(date.year) + \
                      str(date.month).zfill(2) + str(date.day).zfill(2)

            if datekey not in seasonal_prof.keys():
                seasonal_prof[datekey] = 1
            else:
                seasonal_prof[datekey] += 1

    ordered_dict = collections.OrderedDict(sorted(seasonal_prof.items()))
    axis.plot(ordered_dict.values(), color="royalblue")
    axis.set_title("Number of flights in each day of the season")
    axis.set_xlabel("Date")
    axis.set_ylim([0, np.max(list(seasonal_prof.values())) * 1.1])
    axis.set_ylabel("Number of flights")


def plot_number_of_weekdays(dem_df, axis):
    """
        Plot histogram of number of week days in each series
    """
    weekdays = dem_df["FREQ"].apply(
        lambda x: len(utils_dates.freq_str_to_weekdays(x))).values

    yvals, _ = np.histogram(weekdays, bins=np.arange(8) + 1)

    axis.set_title("Number of week days per request")
    axis.set_ylabel("Number of requests")
    axis.set_xlabel("Number of week days")

    axis.bar(np.arange(7) + 1, yvals, color="royalblue")


def plot_weekdays(dem_df, axis):
    """
        Plot bar chart with number of requests including each day of the week
    """
    weekdays = dem_df["FREQ"].apply(
        lambda x: utils_dates.freq_str_to_weekdays(x)).values

    counts = np.zeros(7)
    for elem in weekdays:
        for day in elem:
            counts[day - 1] += 1

    axis.bar(np.arange(7) + 1, counts, color="royalblue")
    axis.set_title("Number of requests in each week day")
    axis.set_xlabel("Day of week")
    axis.set_ylabel("Number of requests")
    axis.set_xticks(np.arange(7) + 1)
    axis.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])


def plot_seats_and_pax(dem_df, axis):
    """
        Plot line charts with number of requests for each no. of seats/pax
    """
    bins = np.arange(0, int(np.max(dem_df["Seats"]) + 5))[::5]
    seats_5buckets, _ = np.histogram(dem_df["Seats"], bins=bins)
    pax_5buckets, _ = np.histogram(dem_df["Pax"], bins=bins)

    axis.plot(bins[:-1], seats_5buckets, label="seats", color="royalblue")
    axis.plot(bins[:-1], pax_5buckets, label="pax", color="salmon")
    axis.legend()
    axis.set_title("Distribution of seats/pax per flight")
    axis.set_xlabel("Seats/Pax (5 seat buckets)")
    axis.set_ylabel("Number of requests")


def plot_dom_int(dem_df, axis):
    """
        Plot distribution of requests by dom/int split
    """
    is_dom = dem_df["OrigDest"].apply(
        lambda x: utils_flights.is_domestic(x)).values

    dom_req = is_dom.sum()
    int_req = len(dem_df) - dom_req

    axis.bar([0, 1], [dom_req, int_req], color="royalblue")
    axis.set_xticks([0, 1])
    axis.set_xticklabels(["Domestic", "International"])
    axis.set_title("Domestic / International split")
    axis.set_ylabel("Number of requests")


def plot_linked(dem_df, axis):
    """
        Plot distribution of requests by linked/not linked split
    """
    is_linked = dem_df["TurnCarrier"].apply(
        lambda x: utils_flights.is_linked(x)).values

    linked = is_linked.sum()
    not_linked = len(dem_df) - linked

    axis.bar([0, 1], [linked, not_linked], color="royalblue")
    axis.set_xticks([0, 1])
    axis.set_xticklabels(["Linked", "Not linked"])
    axis.set_title("Proportion of linked requests")
    axis.set_ylabel("Number of requests")


def plot_turnaround_times(dem_df, axis):
    """
        Plot histogram of turnaround time distributions
    """
    linked_arr = dem_df[(dem_df['ArrDep'] == 'A') & (dem_df["TurnCarrier"] != "")]
    linked_dep = dem_df[(dem_df['ArrDep'] == 'D') & (dem_df["TurnCarrier"] != "")]

    turn_times = []
    for _, arr in linked_arr.iterrows():
        valid_deps = linked_dep[
            (linked_dep['Carrier'] == arr['TurnCarrier']) &
            (linked_dep['FlNum'] == arr['TurnFlNum']) &
            (linked_dep['StartDate'] == arr['StartDate'])]

        dep = valid_deps.iloc[0]

        ahour, aminute = utils_times.str_to_time(arr["Req"])
        arr_time = ahour * 60 + aminute

        dhour, dminute = utils_times.str_to_time(dep["Req"])
        dep_time = dhour * 60 + dminute

        turn_times.append(dep_time - arr_time)

    bins = np.arange(200)[::5]
    yvals, _ = np.histogram(turn_times, bins=bins)

    axis.bar(bins[:-1], yvals, width=5, color="royalblue")
    axis.set_title("Turnaround times")
    axis.set_xlabel("Turnaround time")
    axis.set_ylabel("Number of requests")


def visualise_summary_stats(dem_df, pdf):
    """
        Plot 8 graphs with different summary demand distributions
    """

    _, axes = plt.subplots(4, 2, figsize=(8.27, 11.69), dpi=100)

    plot_num_weeks(dem_df, axes[0, 0])
    plot_seasonal_demand(dem_df, axes[0, 1])
    plot_number_of_weekdays(dem_df, axes[1, 0])
    plot_weekdays(dem_df, axes[1, 1])
    plot_seats_and_pax(dem_df, axes[2, 0])
    plot_dom_int(dem_df, axes[2, 1])
    plot_linked(dem_df, axes[3, 0])
    plot_turnaround_times(dem_df, axes[3, 1])

    plt.suptitle("Demand distributions")
    plt.tight_layout()
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()


if __name__ == "__main__":
    main()
