#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, sys

from tournament_format import advance_count, prelim_team_count
from cornerstone_input import prelim_results

header = """

Created on Mon Jul 26 15:34:38 2021 Eastern Time

This script analyzes prelim stats and produces a sorted list of teams by:
    1) prelim finish
    2) PPB

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s' % time.ctime())


def by_value(item):
    return item[1]


# =============================================================================
# create dictionaries of relevant data from prelim_results
# =============================================================================

team_placement = {rows[0]: (rows[1], str(rows[2])) for rows in prelim_results}
team_ppb = {rows[0]: (rows[3]) for rows in prelim_results}
bracket_team = {(rows[1] + str(rows[2])): rows[0] for rows in prelim_results}

# =============================================================================
# sum up PPB for each pair of teams and rank them
# =============================================================================

bracket_score = 0
count = 0
bracket_ranking = []

for team, placement in sorted(team_placement.items(),
                              key=by_value):
    bracket_score += float(team_ppb.get(team))

    # for visual debugging
    print(f'\nteam = {team}')
    print(f'placement = {placement}')
    print(f'team_ppb = {float(team_ppb.get(team))}')
    print(f'bracket_score = {bracket_score}')

    # if team == 'Woodland (CT)':
    #     print(bracket_ranking)
    #     sys.exit()

    count += 1

    if count % advance_count == 0:

        temp = (placement[0],
                count-(advance_count-1),
                bracket_score)

        bracket_ranking.append(temp)
        bracket_score = 0

    if count == prelim_team_count:
        count = 0

print('\n\n*** bracket_ranking ***\n\n')
print(*bracket_ranking, sep='\n')

sorted_list = sorted(bracket_ranking, key=lambda x: (x[1], -x[2]))

print('\n\n*** sorted_list ***\n\n')
print(*sorted_list[0:20], sep='\n')
print('continued...')

# =============================================================================
# testing section
# =============================================================================

prelim_results.sort(key=lambda x: (x[2], -x[3]))

sorted_list = prelim_results

# for visual debugging
print('\n\n*** prelim_results ***\n\n')
print(*prelim_results[0:20], sep='\n')
print('continued...')
print('\n\n*** sorted_list ***\n\n')
print(*sorted_list[0:20], sep='\n')
print('continued...')

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
