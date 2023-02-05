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

TODO: this script has big problems with reading tournament format codes. Right
now, it is hard-coded into nsc_scheduler.py, which needs to be changed.

TODO: removed emergency spot check of all teams + assigned codes.

@author: Victor Prieto

"""

# %% import list of teams and format according to schedule codes


def code_1_scheduler(teamlist, code):
    code_1 = code.split(',')
    newlist = []
    for i in code_1:
        newlist.append(teamlist[int(i)-1])
    return newlist


def code_2_scheduler(teamlist, code):
    code_2 = code.split(',')
    code_2 = [int(i) for i in code_2]
    newlist = []
    for index, element in enumerate(code_2):
        slice1 = sum(code_2[0:index])
        slice2 = slice1 + element
        newlist.append(teamlist[slice1:slice2])
    return newlist


# reorganize sorted_list according to the playoff schedule code 1
schedule_code_1 = format_dict['playoff schedule code 1']
sorted_list = code_1_scheduler(sorted_list, schedule_code_1)

# split sorted_list according to playoff schedule code 2
schedule_code_2 = format_dict['playoff schedule code 2']
sorted_list = code_2_scheduler(sorted_list, schedule_code_2)

# TODO remove specific nsc scheduler script at some point after NSC...
# unless the nsc scheduler is actually a better way of seeding?

# TODO this is an emergency visual check to make sure team codes are lined up
# for team in team_code_dict:
#     code = team_code_dict[team]
    # print(f'team: {team}\ncode: {code}\n')
# codecheck = input('\nAre all teams assigned the correct code?\n'
#                   + 'enter "Y" if yes: ')
# if codecheck not in ['Y', 'y', 'yes']:
#     print('\nCodecheck failed. Correct team codes in data input and retry.' +
#           '\nplayoff_scheduler.py')
#     sys.exit()


# %% NSC specific scheduler

# sorted_list = playoff_seeding(sorted_list, code1, code2, code3, code4)

prelim_round_count = format_dict['number of prelim rounds '
                                 + '(do not include tiebreakers)']

crossover = format_dict['crossover']
if crossover == 'N':
    crossover = False

# %% backdoor for manual swaps

# TODO manual swaps
# sorted_list = sorted_list # copy/paste backdoor here

# for i in sorted_list:
#     print(*i, sep='\n')
#     print('\n')

# manual_swaps = input('\nAre manual swaps necessary?\nenter "Y" if yes: ')
# if manual_swaps == 'Y':
#     print('\nMake modifications as necessary in the list below.\n\n')
#     print(sorted_list)
#     print('\n\nAfter completing modifications, copy/paste directly into code'
#           + ' in playoff_scheduler, around line ~68.')
#     sys.exit()

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

# %% create full schedule grid + first playoff room dict

full_schedule_grid = []
first_playoff_rooms = {}

# perform this process for each prelim group, add to full_schedule_grid
for bracket_name in playoff_bracket_names:

    # this schedule grid will contain all match information split up by line
    schedule_grid = (standard_schedule(bracket_name,
                                       playoff_teamcode_dict,
                                       playoff_room_dict,
                                       crossover=crossover,
                                       roundstart=prelim_round_count+1))

    full_schedule_grid.append(schedule_grid)

    # produce roomlist + bye if needed
    roomlist = [k for k, v in list(playoff_room_dict.items())
                if k.startswith(bracket_name)]
    roomlist = [playoff_room_dict[i] for i in roomlist]

    if schedule_grid[0][-1] == 'BYE':
        roomlist.append('BYE')

    # populate first_playoff_rooms dict
    first_row = schedule_grid[1]
    for index, team in enumerate(first_row[1:]):
        room_index = int(index//2)
        first_room = roomlist[room_index]
        first_playoff_rooms[team] = first_room

# # prints output for visual debugging
# for index, playoff_bracket in enumerate(playoff_bracket_names):
#     print(f'\nPlayoff Bracket: {playoff_bracket}')
#     print(*full_schedule_grid[index], sep='\n')


