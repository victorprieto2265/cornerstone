#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, sys

# from function_definitions import grid_rearranger
from standard_scheduler import standard_schedule
from cornerstone_input import (playoff_bracket_names,
                               team_code_dict,
                               playoff_room_dict)
from tournament_format import (tier_count,
                               advance_count,
                               playoff_group_count,
                               prelim_round_count)
from prelim_analysis import (sorted_list,
                             bracket_team,
                             team_ppb)  # these might get used for repeat check

# place additional modules here

header = """

Created on Sat Oct  9 18:37:20 2021 Eastern Time

This script accepts the prelim_analysis output and reorders teams into
a list for playoffs.

TODO does snake_seed work with odd team numbers? (right now it error catches)

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s Eastern Time' % time.ctime())

# %% function definitions


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
            for i in range(wanted_parts)]


def snake_seed(list_of_teams, bracket_count):

    # generates sequence of indices for snake seeding
    sequence_length = 2 * bracket_count
    reps = len(list_of_teams) / sequence_length
    sequence = []
    for i in range(0, int(sequence_length/2)):
        for j in range(0, int(reps)):
            sequence.append(i+j*sequence_length)
            sequence.append((sequence_length-1-i)+j*sequence_length)

    # quits program if odd number of teams in list_of_teams
    if (len(list_of_teams)) % 2 == 1:
        print('ODD NUMBER OF TEAMS DETECTED')
        sys.exit()

    # use sequence of indices to generate new list of teams
    newlist = (list_of_teams[index] for index in sequence)
    return newlist


# %% generate new list of teams, divided by playoff bracket

print('\n\npoint 1')
print(*sorted_list[0:16], sep='\n\n')

# split sorted_list into several tiers, for non-NSC tournaments this will
# almost certainly be one tier
split_sorted_list = split_list(sorted_list, tier_count)

print('\n\npoint 2')
print(*split_sorted_list[0:2], sep='\n\n')

for tier in split_sorted_list:
    seeded_list = snake_seed(tier, playoff_group_count/tier_count)

# snake seed brackets, yielding seeded_bracket_list (of brackets)
seeded_team_list = []
for tier in split_sorted_list:
    seeded_list = snake_seed(tier, int(playoff_group_count/tier_count))
    for j in seeded_list:
        seeded_team_list.append(j)

print('\n\npoint 3')
print(*seeded_team_list[0:16], sep='\n\n')

# split the above list by number of playoff brackets, creating list of lists
list_of_teams = split_list(seeded_team_list, playoff_group_count)

print('\n\npoint 4')
print(*list_of_teams[0:2], sep='\n\n')


# %% repeat checker (checks to see if two teams ended up in same bracket?)

# TODO actually write the repeat checker
for bracket in list_of_teams:
#    list_of_groups = []
#    for i in bracket:
#        list_of_groups.append(i[1])
    list_of_groups = list((i[1] for i in bracket))

# %% generate playoff seed / team dictionary

# key is a playoff bracket name and a seed (i.e. Berg6)
# value is the corresponding team (i.e. Great Valley A for Berg6)
# also created a dictionary where the two values are team codes (i.e. GVA)
playoff_team_dict = {}
playoff_teamcode_dict = {}
teamcode_playoff_dict = {}
for index, bracket_name in enumerate(playoff_bracket_names):

    # visual debugging
    # print(f'\n\nindex = {index}')
    # print(f'bracket_name = {bracket_name}')

    for index2, team in enumerate(list_of_teams[index]):
        
        # visual debugging
        # print(f'\nindex2 = {index2}')
        # print(f'team = {team}')
        
        key = bracket_name + str(index2+1)
        value = team[0]
        playoff_team_dict[key] = value
        value = team_code_dict[value]
        playoff_teamcode_dict[key] = value

        # creating a dictionary where k:v pairs are flipped
        teamcode_playoff_dict[value] = key

# visual debugging
# print(teamcode_playoff_dict)

# %% create full schedule grid

# set playoff round count to start after the number of prelim rounds
# (e.g. Round 8 is first playoff round, not Round 1)

full_schedule_grid = []

# perform this process for each prelim group, add to full_schedule_grid
for bracket_name in playoff_bracket_names:

    # this schedule grid will contain all match information split up by line
    schedule_grid = (standard_schedule(bracket_name,
                                       playoff_teamcode_dict,
                                       playoff_room_dict,
                                       roundstart=prelim_round_count+1))

    full_schedule_grid.append(schedule_grid)

# prints output for visual debugging
# for index, playoff_bracket in enumerate(playoff_bracket_names):
#     print(f'\nPlayoff Bracket: {playoff_bracket}')
#     print(*full_schedule_grid[index], sep='\n')

print('\n\n')

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
