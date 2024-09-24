# Slot Allocation Data Generation

## Table of contents
* [Project description](#project-description)
* [Setup](#setup)
* [Usage](#usage)
* [Data Dictionary](#data-dictionary)
* [Instance summary](#instance-summary)
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

## Instance summary
This code was used to generate 100 synthetic instances uploaded to [DataShare Edinburgh](https://datashare.ed.ac.uk/handle/10283/4374). Below you can find a table with summary statistics for each of the instances contained in that data repository:

| instance | series | ops     | Displacement |
|----------|--------|---------|--------------|
| I0000    | 1,920  | 84,075  |              |
| I0001    | 3,041  | 134,068 |              |
| I0002    | 3,942  | 183,014 |              |
| I0003    | 3,126  | 137,050 |              |
| I0004    | 2,303  | 197,047 |              |
| I0005    | 1,333  | 58,031  |              |
| I0006    | 2,801  | 99,104  |              |
| I0007    | 1,538  | 136,052 |              |
| I0008    | 1,032  | 92,069  |              |
| I0009    | 1,062  | 62,029  |              |
| I0010    | 805    | 37,058  |              |
| I0011    | 4,863  | 161,053 |              |
| I0012    | 2,070  | 136,050 |              |
| I0013    | 2,151  | 190,071 |              |
| I0014    | 3,595  | 129,002 |              |
| I0015    | 1,381  | 81,002  |              |
| I0016    | 1,612  | 72,042  |              |
| I0017    | 1,396  | 121,014 |              |
| I0018    | 1,320  | 84,358  |              |
| I0019    | 1,210  | 59,049  |              |
| I0020    | 1,054  | 47,000  |              |
| I0021    | 343    | 22,375  |              |
| I0022    | 2,777  | 128,081 |              |
| I0023    | 1,382  | 97,107  |              |
| I0024    | 2,592  | 116,006 |              |
| I0025    | 938    | 53,276  |              |
| I0026    | 4,100  | 178,419 |              |
| I0027    | 3,559  | 199,069 |              |
| I0028    | 2,234  | 187,015 |              |
| I0029    | 117    | 10,278  |              |
| I0030    | 1,401  | 96,017  |              |
| I0031    | 1,463  | 128,158 |              |
| I0032    | 727    | 33,329  |              |
| I0033    | 1,393  | 122,379 |              |
| I0034    | 337    | 30,161  |              |
| I0035    | 1,874  | 83,051  |              |
| I0036    | 1,551  | 55,051  |              |
| I0037    | 1,128  | 99,310  |              |
| I0038    | 2,692  | 162,118 |              |
| I0039    | 795    | 55,051  |              |
| I0040    | 1,384  | 57,206  |              |
| I0041    | 2,245  | 152,182 |              |
| I0042    | 2,142  | 146,265 |              |
| I0043    | 4,575  | 199,049 |              |
| I0044    | 3,197  | 139,076 |              |
| I0045    | 286    | 23,025  |              |
| I0046    | 234    | 23,137  |              |
| I0047    | 2,165  | 143,016 |              |
| I0048    | 1,953  | 168,015 |              |
| I0049    | 1,933  | 131,019 |              |
| I0050    | 501    | 21,111  |              |
| I0051    | 865    | 36,020  |              |
| I0052    | 2,778  | 188,118 |              |
| I0053    | 958    | 81,023  |              |
| I0054    | 328    | 19,002  |              |
| I0055    | 1,513  | 127,022 |              |
| I0056    | 562    | 20,054  |              |
| I0057    | 2,051  | 145,134 |              |
| I0058    | 4,481  | 156,043 |              |
| I0059    | 2,342  | 162,136 |              |
| I0060    | 1,281  | 84,150  |              |
| I0061    | 669    | 28,285  |              |
| I0062    | 765    | 55,002  |              |
| I0063    | 1,595  | 90,178  |              |
| I0064    | 2,463  | 142,040 |              |
| I0065    | 4,079  | 148,019 |              |
| I0066    | 504    | 44,074  |              |
| I0067    | 223    | 10,058  |              |
| I0068    | 3,015  | 129,260 |              |
| I0069    | 2,461  | 143,314 |              |
| I0070    | 607    | 41,084  |              |
| I0071    | 3,840  | 167,286 |              |
| I0072    | 1,104  | 66,010  |              |
| I0073    | 1,657  | 76,007  |              |
| I0074    | 1,997  | 114,017 |              |
| I0075    | 2,880  | 129,017 |              |
| I0076    | 1,274  | 54,035  |              |
| I0077    | 5,790  | 198,264 |              |
| I0078    | 681    | 57,296  |              |
| I0079    | 2,661  | 172,052 |              |
| I0080    | 2,161  | 148,007 |              |
| I0081    | 1,036  | 50,054  |              |
| I0082    | 305    | 23,044  |              |
| I0083    | 2,356  | 105,058 |              |
| I0084    | 1,651  | 142,106 |              |
| I0085    | 5,727  | 199,024 |              |
| I0086    | 2,047  | 94,267  |              |
| I0087    | 2,852  | 165,050 |              |
| I0088    | 4,875  | 170,009 |              |
| I0089    | 1,716  | 81,261  |              |
| I0090    | 497    | 17,082  |              |
| I0091    | 619    | 27,024  |              |
| I0092    | 1,162  | 55,005  |              |
| I0093    | 331    | 20,123  |              |
| I0094    | 1,360  | 59,012  |              |
| I0095    | 3,130  | 113,124 |              |
| I0096    | 2,207  | 191,021 |              |
| I0097    | 209    | 11,019  |              |
| I0098    | 1,248  | 56,023  |              |
| I0099    | 3,114  | 112,019 |              |


## Future work

* Extend this data generation procedure to generate instances considering interactions in a network of airports
* Extend to level 3 airports with the addition of historic status, historic times and historic seat numbers.



