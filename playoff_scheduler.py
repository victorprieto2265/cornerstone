#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, sys

# from function_definitions import grid_rearranger
from standard_scheduler import standard_schedule
from cornerstone_input import (playoff_bracket_names,
                               team_code_dict, code_team_dict,
                               teamcode_group_dict,
                               playoff_room_dict)
from tournament_format import (tier_count,
                               advance_count,
                               playoff_group_count,
                               prelim_round_count)
from prelim_analysis import (sorted_list,
                             placement_team,
                             team_ppb)  # these might get used for repeat check
from function_definitions import (playoff_team, snake_seed, split_list,
                                  duplicate_checker)

# place additional modules here

header = """

Created on Sat Oct  9 18:37:20 2021 Eastern Time

This script accepts the prelim_analysis output and reorders teams into
a list for playoffs.

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s Eastern Time' % time.ctime())

# %% generate new list of teams, divided by playoff bracket

# split sorted_list into several tiers
# for non-NSC tournaments this will almost certainly be one tier
split_sorted_list = split_list(sorted_list, tier_count)

for tier in split_sorted_list:
    seeded_list = snake_seed(tier, playoff_group_count/tier_count)

# snake seed brackets, yielding seeded_bracket_list (of brackets)
seeded_team_list = []
for tier in split_sorted_list:
    seeded_list = snake_seed(tier, int(playoff_group_count/tier_count))
    for j in seeded_list:
        seeded_team_list.append(j)

# split the above list by number of playoff brackets, creating list of lists
list_of_teams = split_list(seeded_team_list, playoff_group_count)

# %% repeat checker (checks to see if two teams ended up in same bracket?)

print('\n')
for index, bracket_name in enumerate(playoff_bracket_names):
    list_of_groups = list((i[1] for i in list_of_teams[index]))
    print(f'Prelim groups advancing to playoff bracket {bracket_name}:')
    print(list_of_groups)
    result = duplicate_checker(list_of_groups)
    print(f'Duplicates in {bracket_name}: {result}\n')
print('\n')

# %% generate playoff seed / team dictionary

# key is a playoff bracket name and a seed (i.e. Berg6)
# value is the corresponding team (i.e. Great Valley A for Berg6)
# also created a dictionary where the two values are team codes (i.e. GVA)
playoff_team_dict = {}
playoff_teamcode_dict = {}
teamcode_playoff_dict = {}
for index, bracket_name in enumerate(playoff_bracket_names):

    # visual debugging
    print(f'\n\nbracket_name = {bracket_name}')

    for index2, team in enumerate(list_of_teams[index]):

        key = bracket_name + str(index2+1)
        value = team[0]
        playoff_team_dict[key] = value

        value = team_code_dict[value]
        playoff_teamcode_dict[key] = value

        # visual debugging
        print(f'\nkey = {key}')
        print(f'team = {team}')

# creating a dictionary where k:v pairs are flipped
        teamcode_playoff_dict[value] = key

# create list for sunday scheduler to detect carryover opponents?
playoff_team_list = []
for k, v in teamcode_playoff_dict.items():
    name = code_team_dict[k]
    code = k
    prelim_group = teamcode_group_dict[code][0:-1]
    playoff_bracket = v[0:-1]
    playoff_seed = v[-1]
    playoff_team_temp = playoff_team(name, code, prelim_group,
                                     playoff_bracket, playoff_seed)
    playoff_team_list.append(playoff_team_temp)

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
