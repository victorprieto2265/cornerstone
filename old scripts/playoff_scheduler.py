#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import csv
from prelim_analysis import sorted_list, bracket_team
from tournament_format import tier_count, playoff_group_count
# place additional modules here

header = """

Created on Tue Jul 27 22:06:11 2021 Eastern Time

This script accepts the prelim_analysis output and reads the playoff schedule
input files to produce a list of teams with seeds and playoff rooms.

TODO: provide instructions for playoff schedule input file.

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s Eastern Time' % time.ctime())

# =============================================================================
# function definitions
# =============================================================================


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
            for i in range(wanted_parts)]


def csv_string(team, seed, group, bracket, schedule):
    string = (seed, bracket_team.get(team), group, bracket, schedule)
    return string


# =============================================================================
# prepares dictionary where k/v = seed/[list of playoff rooms]
# =============================================================================

playoff_schedule = "./inputs/other/playoff_schedule"

print('\n\n\n')

seed_rooms = {}

with open((playoff_schedule + ".csv"), encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file)

    for row in csv_reader:
        seed = row[0]
        row.pop(0)
        seed_rooms[seed] = row

# =============================================================================
# bracket organization
# =============================================================================

four_tier_list = split_list(sorted_list, tier_count)

alphabet = ['A', 'B', 'C', 'D', 'E']
alphabet2 = ['K', 'J', 'H', 'G', 'F']

bracket_list = ['Azores', 'Balearic', 'Canary', 'Dodecanese',
                'Elaphiti', 'Falklands', 'Galapagos', 'Hebrides',
                'Juan Fernandez', 'Kuril', 'Leeward', 'Maldives',
                'Nicobar', 'Orkney', 'Pelagie', 'Quirimbas',
                'Ryukyu', 'Seychelles', 'Tonga', 'Vanuatu']

# =============================================================================
# pair brackets against one another by snake seeding
# =============================================================================

bracket_count = 0
list_of_seeds = []

print('\n---\n')

# FIXME group_count is out of date and specific to the 84 team tournament
group_count = 10

for tier in four_tier_list:
    for i in range(0, int(group_count/2)):

        bracket = bracket_list[bracket_count]
        print('\n' + bracket)

        prelim_group_1 = tier[i][0]

        seed = alphabet[i] + str(tier[i][1])
        team = (prelim_group_1
                + str(tier[i][1]))
        print(csv_string(team, seed, prelim_group_1, bracket,
                         seed_rooms.get(seed)))
        list_of_seeds.append(csv_string(team, seed, prelim_group_1, bracket,
                             seed_rooms.get(seed)))

        seed = alphabet[i] + str(tier[i][1]+1)
        team = (prelim_group_1
                + str(tier[i][1]+1))
        print(csv_string(team, seed, prelim_group_1, bracket,
                         seed_rooms.get(seed)))
        list_of_seeds.append(csv_string(team, seed, prelim_group_1, bracket,
                             seed_rooms.get(seed)))

        prelim_group_2 = tier[group_count-1-i][0]

        seed = alphabet2[i] + str(tier[i+1][1])
        team = (prelim_group_2
                + str(tier[group_count-1-i][1]))
        print(csv_string(team, seed, prelim_group_2, bracket,
                         seed_rooms.get(seed)))
        list_of_seeds.append(csv_string(team, seed, prelim_group_2, bracket,
                             seed_rooms.get(seed)))

        seed = alphabet2[i] + str(tier[i+1][1]+1)
        team = (prelim_group_2
                + str(tier[group_count-1-i][1]+1))
        print(csv_string(team, seed, prelim_group_2, bracket,
                         seed_rooms.get(seed)))
        list_of_seeds.append(csv_string(team, seed, prelim_group_2, bracket,
                             seed_rooms.get(seed)))

        bracket_count += 1

playoff_schedule = list_of_seeds

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
