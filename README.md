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
This code was used to generate 100 synthetic instances uploaded to [DataShare Edinburgh](https://datashare.ed.ac.uk/handle/10283/4374). Below you can find two tables with summary statistics for each of the instances contained in that data repository. 

In the demand table, `Series` represents the number of series in each instance; `Movements` is the total number of requested operations throughout the season; `Total displacement (min)` is the total displacement in minutes across all operations. There is no column for rejections because none of these instances resulted in any rejections.

| Instance | Series | Movements     | Total displacement (min) |
|----------|--------|---------|--------------|
| I0000    | 1,920  | 84,075  |   22,365           |
| I0001    | 3,041  | 134,068 |   70,310           |
| I0002    | 3,942  | 183,014 |   70,310           |
| I0003    | 3,126  | 137,050 |  1,265            |
| I0004    | 2,303  | 197,047 |  26,490            |
| I0005    | 1,333  | 58,031  |    51,105          |
| I0006    | 2,801  | 99,104  | 10,150             |
| I0007    | 1,538  | 136,052 |   196,200           |
| I0008    | 1,032  | 92,069  | 6,430             |
| I0009    | 1,062  | 62,029  |  21,260            |
| I0010    | 805    | 37,058  | 9,035             |
| I0011    | 4,863  | 161,053 | 30,735             |
| I0012    | 2,070  | 136,050 |  289,025            |
| I0013    | 2,151  | 190,071 |  30,800            |
| I0014    | 3,595  | 129,002 |   16,160           |
| I0015    | 1,381  | 81,002  |   17,240            |
| I0016    | 1,612  | 72,042  |  43,000            |
| I0017    | 1,396  | 121,014 |  108,395            |
| I0018    | 1,320  | 84,358  |  18,415            |
| I0019    | 1,210  | 59,049  |  20,665            |
| I0020    | 1,054  | 47,000  |   25,735           |
| I0021    | 343    | 22,375  |  63,835            |
| I0022    | 2,777  | 128,081 |  44,275            |
| I0023    | 1,382  | 97,107  |   17,825           |
| I0024    | 2,592  | 116,006 |   62,145           |
| I0025    | 938    | 53,276  |       36,785       |
| I0026    | 4,100  | 178,419 |   115,060           |
| I0027    | 3,559  | 199,069 |   212,485           |
| I0028    | 2,234  | 187,015 |  41,555            |
| I0029    | 117    | 10,278  | 1,575             |
| I0030    | 1,401  | 96,017  |  16,630            |
| I0031    | 1,463  | 128,158 |   77,110           |
| I0032    | 727    | 33,329  |  18,215            |
| I0033    | 1,393  | 122,379 |   23,980           |
| I0034    | 337    | 30,161  | 17,385             |
| I0035    | 1,874  | 83,051  |   7,085           |
| I0036    | 1,551  | 55,051  |    217,315          |
| I0037    | 1,128  | 99,310  |   17,825           |
| I0038    | 2,692  | 162,118 |  12,430            |
| I0039    | 795    | 55,051  |  129,510            |
| I0040    | 1,384  | 57,206  |  19,190            |
| I0041    | 2,245  | 152,182 |  94,760            |
| I0042    | 2,142  | 146,265 |  18,965            |
| I0043    | 4,575  | 199,049 |  46,255            |
| I0044    | 3,197  | 139,076 |    30,990          |
| I0045    | 286    | 23,025  |  5,775            |
| I0046    | 234    | 23,137  |   2,330           |
| I0047    | 2,165  | 143,016 |  87,970            |
| I0048    | 1,953  | 168,015 |  517,755           |
| I0049    | 1,933  | 131,019 |  16,625            |
| I0050    | 501    | 21,111  |   19,205           |
| I0051    | 865    | 36,020  |  19,435            |
| I0052    | 2,778  | 188,118 |  162,160            |
| I0053    | 958    | 81,023  |  30,295            |
| I0054    | 328    | 19,002  |  8,595            |
| I0055    | 1,513  | 127,022 |  31,150            |
| I0056    | 562    | 20,054  |   12,130          |
| I0057    | 2,051  | 145,134 |  22,690            |
| I0058    | 4,481  | 156,043 |  133,855            |
| I0059    | 2,342  | 162,136 |  3,260            |
| I0060    | 1,281  | 84,150  |   18,250           |
| I0061    | 669    | 28,285  |  5,020            |
| I0062    | 765    | 55,002  |  48,105            |
| I0063    | 1,595  | 90,178  |  11,055            |
| I0064    | 2,463  | 142,040 |  65,085            |
| I0065    | 4,079  | 148,019 |  3,000            |
| I0066    | 504    | 44,074  |  5,670            |
| I0067    | 223    | 10,058  |  8,145            |
| I0068    | 3,015  | 129,260 |  97,050            |
| I0069    | 2,461  | 143,314 |  4,130            |
| I0070    | 607    | 41,084  |  30,760            |
| I0071    | 3,840  | 167,286 | 29,935             |
| I0072    | 1,104  | 66,010  |  58,975            |
| I0073    | 1,657  | 76,007  |  11,340            |
| I0074    | 1,997  | 114,017 |   136,985           |
| I0075    | 2,880  | 129,017 |   80,270           |
| I0076    | 1,274  | 54,035  |  5,470           |
| I0077    | 5,790  | 198,264 |   14,880           |
| I0078    | 681    | 57,296  |       40,310       |
| I0079    | 2,661  | 172,052 |   3,795           |
| I0080    | 2,161  | 148,007 |   100,365           |
| I0081    | 1,036  | 50,054  |  167,015            |
| I0082    | 305    | 23,044  |  56,385            |
| I0083    | 2,356  | 105,058 |   16,740           |
| I0084    | 1,651  | 142,106 |     44,190         |
| I0085    | 5,727  | 199,024 |    96,990          |
| I0086    | 2,047  | 94,267  |  9,440            |
| I0087    | 2,852  | 165,050 |  43,145            |
| I0088    | 4,875  | 170,009 |  65,155            |
| I0089    | 1,716  | 81,261  | 21,235             |
| I0090    | 497    | 17,082  | 6,415             |
| I0091    | 619    | 27,024  |  45,395            |
| I0092    | 1,162  | 55,005  |  21,730            |
| I0093    | 331    | 20,123  |   12,145           |
| I0094    | 1,360  | 59,012  |  8,300            |
| I0095    | 3,130  | 113,124 |  42,480            |
| I0096    | 2,207  | 191,021 |  43,270            |
| I0097    | 209    | 11,019  |    16,860          |
| I0098    | 1,248  | 56,023  |   28,580           |
| I0099    | 3,114  | 112,019 |  15,945            |

In the capacity table below, `Constraint types` is the number of different families of capacity constraints declared by this ficitious airport, e.g. "max 10 departures in 60-minute periods rolling every 15 minutes". `Runway constraints` and `Terminal constraints` denote how many of those families of constraints correspond to runway and terminal constraints, respectively. `Duration range (min)` shows the shortest and longest time window of any capacity constraint in the instance. `Rolling period range (min)` shows the shortest and longest rolling period of any capacity constraint in the instance. Lastly, `Total constraints per day` show the number of individual capacity constraints that would result for these synthetic "capacity declarations" in any single day.

| Instance | Constraint types | Runway constraints | Terminal constraints | Duration range (min) | Rolling period range (min) | Total constraints per day |
|----------|------------------|--------------------|----------------------|----------------|----------------------|------------------------------|
| I0000    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0001    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0002    | 24               | 6                  | 18                   | 15 - 120       | 15 - 60              | 1,224                        |
| I0003    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0004    | 24               | 6                  | 18                   | 15 - 120       | 15 - 60              | 2,088                        |
| I0005    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0006    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0007    | 17               | 5                  | 12                   | 15 - 120       | 5 - 60               | 936                          |
| I0008    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0009    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0010    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0011    | 23               | 5                  | 18                   | 15 - 120       | 5 - 60               | 1,080                        |
| I0012    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0013    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0014    | 17               | 5                  | 12                   | 15 - 120       | 5 - 60               | 936                          |
| I0015    | 17               | 5                  | 12                   | 15 - 120       | 5 - 60               | 936                          |
| I0016    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0017    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0018    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0019    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 648                          |
| I0020    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0021    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 648                          |
| I0022    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0023    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0024    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0025    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 648                          |
| I0026    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0027    | 23               | 5                  | 18                   | 15 - 120       | 5 - 60               | 1,080                        |
| I0028    | 24               | 6                  | 18                   | 15 - 120       | 15 - 60              | 1,224                        |
| I0029    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0030    | 17               | 5                  | 12                   | 15 - 120       | 5 - 60               | 936                          |
| I0031    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0032    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0033    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0034    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0035    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0036    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 936                          |
| I0037    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0038    | 24               | 6                  | 18                   | 15 - 120       | 15 - 60              | 1,224                        |
| I0039    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 936                          |
| I0040    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 648                          |
| I0041    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0042    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0043    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0044    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0045    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0046    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0047    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0048    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0049    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0050    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0051    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0052    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0053    | 17               | 5                  | 12                   | 15 - 120       | 5 - 60               | 936                          |
| I0054    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 936                          |
| I0055    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0056    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0057    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0058    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0059    | 24               | 6                  | 18                   | 15 - 120       | 15 - 60              | 1,224                        |
| I0060    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0061    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0062    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0063    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0064    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0065    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0066    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0067    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0068    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0069    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0070    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0071    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0072    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0073    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0074    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0075    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0076    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0077    | 23               | 5                  | 18                   | 15 - 120       | 5 - 60               | 1,080                        |
| I0078    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0079    | 23               | 5                  | 18                   | 15 - 120       | 5 - 60               | 1,080                        |
| I0080    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0081    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 936                          |
| I0082    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 936                          |
| I0083    | 17               | 5                  | 12                   | 15 - 120       | 5 - 60               | 936                          |
| I0084    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0085    | 24               | 6                  | 18                   | 15 - 120       | 15 - 60              | 1,224                        |
| I0086    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 936                          |
| I0087    | 24               | 6                  | 18                   | 15 - 120       | 15 - 60              | 1,224                        |
| I0088    | 24               | 6                  | 18                   | 15 - 120       | 15 - 60              | 2,088                        |
| I0089    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |
| I0090    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0091    | 11               | 5                  | 6                    | 15 - 120       | 5 - 60               | 792                          |
| I0092    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 648                          |
| I0093    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0094    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 648                          |
| I0095    | 11               | 11                 | 0                    | 5 - 60         | 5 - 60               | 1,080                        |
| I0096    | 23               | 5                  | 18                   | 15 - 120       | 5 - 60               | 1,080                        |
| I0097    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 648                          |
| I0098    | 12               | 6                  | 6                    | 15 - 120       | 15 - 60              | 648                          |
| I0099    | 18               | 6                  | 12                   | 15 - 120       | 15 - 60              | 1,512                        |


## Future work

* Extend this data generation procedure to generate instances considering interactions in a network of airports
* Extend to level 3 airports with the addition of historic status, historic times and historic seat numbers.



