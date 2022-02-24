# Slot Allocation Data Generation

## Table of contents
* [Project description](#project-description)
* [Setup](#setup)
* [Usage](#usage)
* [Data Dictionary](#data-dictionary)
* [Future Work](#future-work)


## Project description

Procedure to generate synthetic data for computational experiments on the single airport slot allocation problem.

Inspired by slot request data sets published by [Agencia Nacional de Aviacão Civil (ANAC)](www.anac.gov.br/en/air-services/slot-coordination) we create distributions for a set of parameters that characterise airport demand:

* total number of operations in a summer season
* domestic/international market split
* proportion of flight series including turnaround information
* distribution of requested turnaround times
* distribution of seats per aircraft
* distribution of seat load factors
* distribution of start and end dates of the series
* distribution of weekly frequencies


Inspired by capacity declaration reports published by [Airport Coordination Limited (ACL)](www.acl-uk.org/latest-airport-info/), we create different sets of runway / terminal capacity limits characterised by:

* Type of resource (runway / terminal)
* Arrival / departure / all flights
* Domestic / international / all flights
* Duration of time window each individual capacity limit
* Frequency of start times of each individual capacity limit
* Level of congestion

To generate a single instance, we sample from demand distributions to generate a slot request dataset and we choose a set of capacity constraints and determine the declared limits based on the generated demand to produce a capacity data set.

Possible distributions for each parameter can be found in `parameters.yml`.

## Setup

This project used `Python 3.9`. Install dependencies with 

```
$ pip install -r requirements.txt
```

## Usage

Generate synthetic instances using

```
$ python src/generate.py [NUMBER_OF_INSTANCES]
```

This will create `[NUMBER_OF_INSTANCES]` pairs of capacity and demand files. Demand files will be stored in `schedules/demand/`, with the name `IXXXX_demand.csv`, where XXXX will be a unique identifier of the instance. Capacity files will be stored in `schedules/capacity/` with the name `IXXXX_capacity.csv`, where XXXX will math the unique identifier of its corresponding demand file. It will also create a file `IXXXX_metadata.yml` for each instance in `schedules/metadata/` which will show the distributions and parameters selected for that instance.


Generate PDF reports showing summary statistics of each generated instance found in the `schedules` folder using

```
$ python src/visualise.py
```

Clean all generated instances, metadata and reports using

```
$ python src/clean.py
```


## Data dictionary

Fields in demand file `IXXXX_demand.csv`:

| Field | Description |
| ----------- | ----------- |
| `FREQ` | This field indicates days of the week that a series requests to operate. e.g. "01034007" indicates that the series requests to operate on Tuesdays (1), Thursdays (3), Fridays (4) and Sundays (7) |
| `Carrier`| 3-letter code of dummy name of carrier operating the flight in the series |
| `FlNum`| Flight number of flights in the series | 
| `Airport` | 3-letter code of dummy airport associated with this instance |
| `Season` | 3-letter code in format XYY indicating aviation season under consideration, where "X" indicates whether it's a winter (W) or summer (S) season and "YY" is the year in 2-digit format. All instances generated are based on the 2020 summer season (S20) |
| `ServType` | Type of service, "J" for scheduled in all generated instances |
| `Term`| Name of terminal in which each series operates, e.g. Term1, Term2 |
| `OrigDest`| 3-letter code of dummy origin or destination airport. "ZZD" denotes a domestic airport and "ZZI" an international airport | 
| `StartDate`| First date in the season that the series requests to operate | 
| `EndDate`| Last date in the season that the series requests to operate | 
| `Seats`| Number of seats in every flight in the series | 
| `Pax`| Number of passengers in every flight in the series | 
| `ArrDep`| Arrival or departure | 
| `Req`| Requested slot, in HHMM format | 
| `NoOps`| Number of requested operations in the season. It can be calculated from `StartDate`, `EndDate` and `FREQ` | 
| `TurnCarrier`| Name of the carrier operating the turnaround flight, if this information is provided | 
| `TurnFlNum`| Flight number of the turnaround flight, if this information is provided | 


Fields in demand file `IXXXX_capacity.csv`:

| Field | Description |
| ----------- | ----------- |
| `Constraint` | Unique identifier of a type of capacity constraint, which groups all individual limits with the same `Resource`, `ArrDep`, `Duration`, `DomInt` and `Terminal`|
| `Resource`| Runway (limits the number of flights) or terminal (number of passengers) |
| `ArrDep` | Whether this limit affects arriving flights (A), departures (D) or all flights (T) |
| `Duration`| Duration of the time window of the capacity limit, in minutes |
| `Limit` | Maximum number of flights or passengers allowed within the time window |
| `Time` | Start time of the capacity limit window, in HHMM format |
| `DomInt` | Whether this limit affects domestic flights (D), international flights (I) or all flights (T) |
| `Terminal` | Capacity limit only affects flights operating in this terminal. If empty, flights in any terminal can be affected |

## Future work

* Extend this data generation procedure to generate instances considering interactions in a network of airports
* Extend to level 3 airports with the addition of historic status, historic times and historic seat numbers.



