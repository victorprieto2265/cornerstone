#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from cornerstone_input import (playoff_bracket_names,
                               team_code_dict,
                               playoff_room_dict,
                               format_dict)
from standard_scheduler import standard_schedule
from prelim_analysis import sorted_list
from nsc_scheduler import playoff_seeding, code1, code2, code3, code4

# place additional modules here

header = """

Created on Sat Oct  9 18:37:20 2021 Eastern Time

This script accepts the prelim_analysis output and reorders teams into
a list for playoffs.

@author: Victor Prieto

"""

# %% import list of teams and format according to schedule codes


# def code_1_scheduler(teamlist, code):
#     code_1 = code.split(',')
#     newlist = []
#     for i in code_1:
#         newlist.append(teamlist[int(i)-1])
#     return newlist


# def code_2_scheduler(teamlist, code):
#     code_2 = code.split(',')
#     code_2 = [int(i) for i in code_2]
#     newlist = []
#     for index, element in enumerate(code_2):
#         slice1 = sum(code_2[0:index])
#         slice2 = slice1 + element
#         newlist.append(teamlist[slice1:slice2])
#     return newlist


# # reorganize sorted_list according to the playoff schedule code 1
# schedule_code_1 = format_dict['playoff schedule code 1']
# sorted_list = code_1_scheduler(sorted_list, schedule_code_1)

# # split sorted_list according to playoff schedule code 2
# schedule_code_2 = format_dict['playoff schedule code 2']
# sorted_list = code_2_scheduler(sorted_list, schedule_code_2)

# TODO remove specific nsc scheduler script at some point after NSC...
# unless the nsc scheduler is actually a better way of seeding?
sorted_list = playoff_seeding(sorted_list, code1, code2, code3, code4)

prelim_round_count = format_dict['number of prelim rounds '
                                 + '(do not include tiebreakers)']

crossover = format_dict['crossover']
if crossover == 'N':
    crossover = False

# %% generate playoff seed / team dictionary

# key is a playoff bracket name and a seed (i.e. Berg6)
# value is the corresponding team (i.e. Great Valley A for Berg6)
# also created a dictionary where the two values are team codes (i.e. GVA)
playoff_team_dict = {}
playoff_teamcode_dict = {}
teamcode_playoff_dict = {}

for index, bracket_name in enumerate(playoff_bracket_names):

    # # visual debugging
    # print(f'\n\nbracket_name = {bracket_name}')

    for index2, team in enumerate(sorted_list[index]):

        key = bracket_name + str(index2+1)
        value = team[0]
        playoff_team_dict[key] = value

        # # visual debugging
        # print(f'team = {team}')
        # print(f'key = {key} \nvalue = {value}\n')

        value = team_code_dict[value]
        playoff_teamcode_dict[key] = value


# creating a dictionary where k:v pairs are flipped
        teamcode_playoff_dict[value] = key

# # create list for sunday scheduler to detect carryover opponents?
# playoff_team_list = []
# for k, v in teamcode_playoff_dict.items():
#     name = code_team_dict[k]
#     code = k
#     prelim_group = teamcode_group_dict[code][0:-1]
#     playoff_bracket = v[0:-1]
#     playoff_seed = v[-1]
#     playoff_team_temp = playoff_team(name, code, prelim_group,
#                                       playoff_bracket, playoff_seed)
#     playoff_team_list.append(playoff_team_temp)

# %% create full schedule grid

full_schedule_grid = []

# perform this process for each prelim group, add to full_schedule_grid
for bracket_name in playoff_bracket_names:

    # this schedule grid will contain all match information split up by line
    schedule_grid = (standard_schedule(bracket_name,
                                       playoff_teamcode_dict,
                                       playoff_room_dict,
                                       crossover=crossover,
                                       roundstart=prelim_round_count+1))

    full_schedule_grid.append(schedule_grid)

# # prints output for visual debugging
# for index, playoff_bracket in enumerate(playoff_bracket_names):
#     print(f'\nPlayoff Bracket: {playoff_bracket}')
#     print(*full_schedule_grid[index], sep='\n')
