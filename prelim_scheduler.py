#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
from cornerstone_input import (list_of_teams, room_assignments,
                               team_code_dict, code_team_dict)
from standard_scheduler import standard_schedule
from function_definitions import remove_duplicates


header = """

This script reads the list of prelim teams and the tournament format files
to produce a set of prelim schedules.

Created on Mon Oct 11 19:57:37 2021 Eastern Time

@author: Victor Prieto

"""

# %% input analysis

prelim_group_names = [sublist[1] for sublist in list_of_teams]
prelim_group_names = remove_duplicates(prelim_group_names)

# key is a prelim group name and a seed (i.e. Belmopan6)
# value is the corresponding team (i.e. Great Valley A for Belmopan6)
# also created a dictionary where values are team codes (i.e. GVA)
prelim_team_dict = {}
prelim_teamcode_dict = {}
team_group_dict = {}
teamcode_group_dict = {}
for i in list_of_teams:
    # key = i[2] + str(i[3])
    key = i[1] + str(i[2])
    value = i[0]  # team name
    prelim_team_dict[key] = value
    # also created dictionary where k/v pairs are swapped
    team_group_dict[value] = key
    # value = i[1]  # team code
    value = team_code_dict[value]
    prelim_teamcode_dict[key] = value
    # also created dictionary where k/v pairs are swapped
    teamcode_group_dict[value] = key

# key is prelim group and a number (i.e. Accra1)
# value is corresponding room (i.e. Grand Ballroom A is Accra1)
# also created dictionary where key is a playoff bracket instead
prelim_room_dict = {}
for i in room_assignments:
    key = i[1] + str(i[2])
    value = i[0]
    prelim_room_dict[key] = value

# %% create full schedule grid

full_schedule_grid = []

# perform this process for each prelim group, add to full_schedule_grid
for group_name in prelim_group_names:
    print(f'group name: {group_name}')
    schedule_grid = (standard_schedule(group_name,
                                       prelim_teamcode_dict,
                                       prelim_room_dict))
    full_schedule_grid.append(schedule_grid)

# for visual debugging
for index, prelim_group in enumerate(prelim_group_names):
    print(f'\nPrelim Group: {prelim_group}')
    print(*full_schedule_grid[index], sep='\n')
