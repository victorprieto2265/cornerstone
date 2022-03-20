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

team_placement = {rows[0]: (rows[2], str(rows[3])) for rows in list_of_teams}
team_ppb = {rows[0]: (rows[4]) for rows in list_of_teams}
placement_team = {(rows[2] + str(rows[3])): rows[0] for rows in list_of_teams}

advance_count = format_dict['the number of teams that advance to each bracket'
                            + ' (e.g. top 2 or top 3)']

# %% reorganization attempt 5

crossover = format_dict['crossover']

# sort list by index 1 descending, index 2 ascending
# print(*list_of_teams, sep='\n')
sorted_list = sorted(list_of_teams, key=lambda x: (x[3], -x[4]))
if crossover != 'N':
    # ignore PPB if using crossover schedule
    # TODO I don't know if this is best method but it works for now
    sorted_list = sorted(list_of_teams, key=lambda x: (x[3]))
# print(*sorted_list, sep='\n')


# # %% reorganization attempt 1

# # sum up PPB for each pair of teams and rank them

# bracket_score = 0
# count = 0
# bracket_ranking = []

# for team, placement in sorted(team_placement.items(),
#                               key=by_value):
#     bracket_score += float(team_ppb.get(team))

#     # for visual debugging
#     # print(f'\nteam = {team}')
#     # print(f'placement = {placement}')
#     # print(f'team_ppb = {float(team_ppb.get(team))}')
#     # print(f'bracket_score = {bracket_score}')

#     if count == 0:
#         previous_group = placement[0]
#     count += 1

#     if count % advance_count == 0:

#         temp = (placement[0],
#                 count-(advance_count-1),
#                 bracket_score)

#         bracket_ranking.append(temp)
#         bracket_score = 0

#     # print(placement[0])
#     # print(previous_group)
#     if placement[0] != previous_group:
#         # print('new group')
#         count = 0
#     else:
#         # print('same group')
#         continue
#     previous_group = placement[0]
#     # if count == prelim_team_count:
#     #     count = 0

# # for visual debugging
# # print('\n\n*** bracket_ranking ***\n\n')
# # print(*bracket_ranking, sep='\n')

# # %% reorganization attempt 2

# # sort list by index 1 descending, index 2 ascending
# sorted_list = sorted(bracket_ranking, key=lambda x: (x[1], -x[2]))

# # print('\n\n*** sorted_list ***\n\n')
# # print(*sorted_list[0:20], sep='\n')
# # print('continued...')

# '''
# sorted_list is a list of lists.

# Each element has a number at index 1 corresponding to the advance count.
# That value refers to the number of teams whose PPBs are being grouped
# together. Example: if the numbers are 1/3/5/7, then teams are being
# grouped into pairs: 1/2, 3/4, 5/6, 7/8.

# The group name at index 0 indicates the prelim group that the
# teams are from.

# The number at index 2 is the sum of team PPBs from that subset of teams in
# the prelim group.

# Full example: The 3rd and 4th place teams in prelim group Caracas scored 17.20
# and 15.44, respectively. Their combined PPB is 32.64; therefore, there is an
# element that reads ('Caracas', 3, 32.64).

# This list is sorted by index 1 and then index 2, meaning in the example above,
# the first elements are the 1/2 seeds, and those elements are sorted by their
# combined PPB at index 2.

# '''

# # %% reorganization attempt 3

# # convert sorted_list into a list of teams instead of a list of brackets

# # print('\n\nnew section\n\n')

# final_list = []
# for i in sorted_list:
#     bracket = i[0]
#     for rank in range(0, advance_count):
#         team = placement_team[f'{bracket}{rank+i[1]}']
#         placement = rank+i[1]
#         prelim_ppb = team_ppb[team]
#         # print(f'\n{team}')
#         # print(f'placement: {bracket}, {placement}')
#         final_list.append((team, bracket, placement, prelim_ppb))

# # print(*final_list, sep='\n')

# sorted_list = final_list

# # %% reorganization attempt 4

# print(bracket_ranking)

# # sort list by index 1 descending, index 2 ascending
# sorted_list = sorted(final_list, key=lambda x: (x[2], -x[3]))


# %% for visual debugging
print('\n\n*** sorted_list ***\n\n')
print(*sorted_list[0:25], sep='\n')
print('continued...')
