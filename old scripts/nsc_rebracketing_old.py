#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import csv

header = """

Created on May 20th, 2021

TODO:
in output file, include
count number of unique bracket names
count number of teams per bracket

Rebracketing script for NSC. Steps performed by script:

rank the teams in 10 groups of 8, 1st through 8th.
add up the points for the 1st/2nd teams in each of the 10 groups
    (and so on through 7th/8th).
rank the 10 groups by those point rankings.
pair the 10 groups up, snake seeding style (1 v 10, 2 v 9, etc.)

The .csv file to be read must have the following fields in order:
    team name
    bracket name
    final placement in prelim group (after tiebreaker gameplay)
    PPB

The second .csv file must have the following fields in order:
	seeds
	first room
(need to actually import this file)

@author: Victor Prieto

"""
# starts program runtime
start_time = time.time()
print('start time: %s Eastern Time' % time.ctime())
print(header)

# =============================================================================
# input section
# =============================================================================

# enter number of prelim groups here
group_count = 12

# enter number of teams per prelim group here
team_count = 8

# =============================================================================
# locate csv files to open
# =============================================================================

#playoff_seeds = input(".csv file must be in the same directory as this"
#                     + " script.\nEnter file name here (exclude .csv): ")
playoff_seeds = "first rooms 80 teams"

#stats_export = input(".csv file must be in the same directory as this"
#                     + " script.\nEnter file name here (exclude .csv): ")
stats_export = "prelim_results"


# =============================================================================
# identify and categorize relevant data from csv file
# =============================================================================


def by_value(item):
    return item[1]


# rewrite the below code to avoid csv_file.seek(0)
with open((stats_export + ".csv"), encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file)

    team_placement = {rows[0]: (rows[1], rows[2]) for rows in csv_reader}
    csv_file.seek(0)
    team_ppb = {rows[0]: rows[3] for rows in csv_reader}
    csv_file.seek(0)
    bracket_team = {(rows[1] + rows[2]): rows[0] for rows in csv_reader}

# =============================================================================
# sum up PPB for each pair of teams and rank them
# =============================================================================

with open((playoff_seeds + ".csv"), encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file)


bracket_score = 0
count = 0
bracket_ranking = []

for team, placement in sorted(team_placement.items(),
                              key=by_value):
    bracket_score += float(team_ppb.get(team))

    if count % 2:

        temp = (placement[0],
                count,
                bracket_score)

        bracket_ranking.append(temp)
        bracket_score = 0

    count += 1
    if count == team_count:
        count = 0

sorted_list = sorted(bracket_ranking, key=lambda x: (x[1], -x[2]))


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
            for i in range(wanted_parts)]


four_tier_list = split_list(sorted_list, 4)

for i in four_tier_list:
    for j in (i):
        print(j)

# =============================================================================
# pair brackets against one another by snake seeding
# =============================================================================


def csv_string(team, seed, group, bracket):
    string = (seed, bracket_team.get(team), group, bracket)
    return string


alphabet = ['A', 'B', 'C', 'D', 'E']
alphabet2 = ['K', 'J', 'H', 'G', 'F']

bracket_list = ['Azores', 'Balearic', 'Canary', 'Dodecanese',
                'Elaphiti', 'Falklands', 'Galapagos', 'Hebrides',
                'Juan Fernandez', 'Kuril', 'Leeward', 'Maldives',
                'Nicobar', 'Orkney', 'Pelagie', 'Quirimbas',
                'Ryukyu', 'Seychelles', 'Tonga', 'Vanuatu']

bracket_count = 0
list_of_seeds = []

for tier in four_tier_list:
    for i in range(0, int(group_count/2)):

        bracket = bracket_list[bracket_count]
        print(bracket)

        prelim_group_1 = tier[i][0]

        seed = alphabet[i] + str(tier[i][1])
        team = (prelim_group_1
                + str(tier[i][1]))
        print(csv_string(team, seed, prelim_group_1, bracket))
        list_of_seeds.append(csv_string(team, seed, prelim_group_1, bracket))

        seed = alphabet[i] + str(tier[i][1]+1)
        team = (prelim_group_1
                + str(tier[i][1]+1))
        print(csv_string(team, seed, prelim_group_1, bracket))
        list_of_seeds.append(csv_string(team, seed, prelim_group_1, bracket))

        prelim_group_2 = tier[group_count-1-i][0]

        seed = alphabet2[i] + str(tier[i+1][1])
        team = (prelim_group_2
                + str(tier[group_count-1-i][1]))
        print(csv_string(team, seed, prelim_group_2, bracket))
        list_of_seeds.append(csv_string(team, seed, prelim_group_2, bracket))

        seed = alphabet2[i] + str(tier[i+1][1]+1)
        team = (prelim_group_2
                + str(tier[group_count-1-i][1]+1))
        print(csv_string(team, seed, prelim_group_2, bracket))
        list_of_seeds.append(csv_string(team, seed, prelim_group_2, bracket))

        bracket_count += 1

fields = ['Seed', 'Team', 'Prelim Group', 'Playoff Bracket']

# writing to csv file
with open('playoff_seeds.csv', 'w') as csv_file:
    # creating a csv writer object
    csvwriter = csv.writer(csv_file)

    # writing the fields
    csvwriter.writerow(fields)

    for i in list_of_seeds:
        csvwriter.writerows([i])

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
