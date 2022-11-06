#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cornerstone_input import list_of_teams, format_dict, prelim_group_names

header = """

Created on Mon Jul 26 15:34:38 2021 Eastern Time

This script analyzes prelim stats and produces a sorted list of teams by:
    1) prelim finish
    2) PPB

@author: Victor Prieto

"""


def by_value(item):
    return item[1]


# =============================================================================
# create dictionaries of relevant data from prelim_results
# =============================================================================

team_placement = {rows[0]: (rows[1], str(rows[2])) for rows in list_of_teams}
team_ppb = {rows[0]: (rows[3]) for rows in list_of_teams}
placement_team = {(rows[1] + str(rows[2])): rows[0] for rows in list_of_teams}

advance_count = format_dict['the number of teams that advance to each bracket'
                            + ' (e.g. top 2 or top 3)']

# %% sort by finish and then PPB

crossover = format_dict['crossover']

# sort list by index 1 descending, index 2 ascending
# print(*list_of_teams, sep='\n')
sorted_list = sorted(list_of_teams, key=lambda x: (x[2], -x[3], -x[4]))
if crossover != 'N':
    # ignore PPB if using crossover schedule
    # TODO I don't know if this is best method but it works for now
    sorted_list = sorted(list_of_teams, key=lambda x: (x[2]))


# %% for visual debugging
print('\n\n*** sorted_list ***\n\n')
print(*sorted_list[0:20], sep='\n')
print('continued...')
