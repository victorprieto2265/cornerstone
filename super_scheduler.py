#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% import modules/functions, header
import time
import os
import sys

from cornerstone_input import (super_bracket_names,
                               team_code_dict,
                               super_room_dict,
                               format_dict,
                               list_of_teams)
from standard_scheduler import standard_schedule

scriptname = os.path.basename(__file__)

description = f"""

*** script executed = {scriptname} ***

This script analyzes the super_input.xlsx file and passes
a schedule grid for super_latex_writer to read.

TODO: there is a potential bug in this script: it is possible (although rare)
that, when rebracketing, some teams will carry over a game while others
do not. This will present a problem when attempting to figure out
which teams have a carryover game. This is a rare enough occurrence that it
probably isn't worth dealing with now, but keep it in mind.

TODO selection of crossover schedule is currently hardcoded to B. For NSC, it
will almost certainly always be B, but when figuring out how to adapt playoff
scheduler to incorporate crossovers, we'll need a better way of figuring out
which crossover template to select.

Created on Thu Dec 23 19:25:05 2021

@author: Victor Prieto

"""


# %% start runtime
start_time = time.time()
print('\n', description)
print('start time: %s' % time.ctime())

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

# sorted list: team name, playoff group name, placement, PPB

# reorganize sorted_list according to the playoff schedule code 1
schedule_code_1 = format_dict['playoff schedule code 1']
sorted_list = code_1_scheduler(list_of_teams, schedule_code_1)

# split sorted_list into brackets according to playoff schedule code 2
schedule_code_2 = format_dict['playoff schedule code 2']
sorted_list = code_2_scheduler(sorted_list, schedule_code_2)

# print('\n\noutput sorted_list\n')
# for i in sorted_list:
#     print(*i, sep='\n')
#     print('\n')
# print('\n***\n')

crossover = format_dict['crossover']
if crossover == 'N':
    crossover = False

# define number for first round in schedule
prelim_round_count = format_dict['number of prelim rounds '
                                 + '(do not include tiebreakers)']
playoff_round_count = format_dict['number of playoff rounds '
                                 + '(do not include tiebreakers)']
round_start = prelim_round_count + playoff_round_count + 1

# %% backdoor for manual swaps

sorted_list = sorted_list  # copy/paste backdoor here

for i in sorted_list:
    print(*i, sep='\n')
    print('\n')

manual_swaps = input('\nAre manual swaps necessary?\nenter "Y" if yes: ')
if manual_swaps == 'Y':
    print('\nMake modifications as necessary in the list below.\n\n')
    print(sorted_list)
    print('\n\nAfter completing modifications, copy/paste directly into code.')
    sys.exit()

# %% super input analysis

# TODO this section was originally written to accommodate the unusual feature
# in NSC to have some brackets as crossovers and some not. Deprecated with
# 72-team field but may be useful in future.

# super_input.sort(key=lambda x: (x[4], x[5]))

# super_bracket_list = [sublist[3] for sublist in super_input]
# carryover_brackets = [sublist[3] for sublist in super_input
#                       if sublist[6] != 0]

# super_bracket_list = remove_duplicates(super_bracket_list)
# crossover_brackets = remove_duplicates(carryover_brackets)

# # create super_teamcode_dict (super_room_dict imported already)
# # TODO shift this over to input?
# super_team_dict = {}
# super_teamcode_dict = {}
# teamcode_super_dict = {}
# super_record_dict = {}
# for i in super_input:
#     print(i)
#     key = i[3] + str(i[5])  # bracket-seed
#     value = i[0]  # team name
#     super_team_dict[key] = value

#     value = team_code_dict[value]  # team code
#     print(f'key:value = {key}:{value}')
#     super_teamcode_dict[key] = value

#     # creating a dictionary where k:v pairs are flipped
#     teamcode_super_dict[value] = key

#     if i[6] == 1:
#         record = '1-0'
#     elif i[6] == -1:
#         record = '0-1'
#     else:
#         record = ''
#     super_record_dict[value] = record


# %% super grid scheduling

super_teamcode_dict = {}
teamcode_super_dict = {}
for index, bracket_name in enumerate(super_bracket_names):

    # # visual debugging
    # print(f'\nbracket_name = {bracket_name}')

    for index2, team in enumerate(sorted_list[index]):

        key = bracket_name + str(index2+1)
        team_name = team[0]
        value = team_code_dict[team_name]
        super_teamcode_dict[key] = value
        teamcode_super_dict[value] = key
        # # visual debugging
        # print(f'team = {team_name}')
        # print(f'key = {key} \nvalue = {value}')

full_schedule_grid = []

# TODO figure out crossover scheduler again
for index, super_bracket in enumerate(super_bracket_names):
    crossover = 'B'  # FIXME hardcoded to use crossover schedule B8 for NSC

    # TODO see above in "super input analysis"
    # if super_bracket in crossover_brackets:
    #     crossover = "B"  # FIXME hardcoded to use schedule B
    # else:
    #     crossover = False

    schedule_grid = (standard_schedule(super_bracket,
                                       super_teamcode_dict,
                                       super_room_dict,
                                       crossover=crossover,
                                       roundstart=round_start))
    full_schedule_grid.append(schedule_grid)


# for visual debugging
for index, super_bracket in enumerate(super_bracket_names):
    print(f'\nSuper Group: {super_bracket}')
    print(*full_schedule_grid[index], sep='\n')


# %% end runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
