#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import pandas as pd
# place additional modules here

header = """

Created on Thu Oct 14 00:23:16 2021 Eastern Time

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s Eastern Time' % time.ctime())

# =============================================================================
# input section for tournament format
# =============================================================================

tournament_format = "./inputs/tournament_format"

df = pd.read_excel(f'{tournament_format}.xlsx')

format_list = df.values.tolist()

for i in format_list:

    if i[2] == 'tournament_name':
        tournament_name = i[1]

    if i[2] == 'tournament_location':
        tournament_location = i[1]

    if i[2] == 'tournament_date':
        tournament_date = i[1]

    if i[2] == 'sunday_round_count':
        sunday_round_count = i[1]

    if i[2] == 'prelim_team_count':
        prelim_team_count = i[1]

    if i[2] == 'playoff_team_count':
        playoff_team_count = i[1]

    if i[2] == 'prelim_group_count':
        prelim_group_count = i[1]

    if i[2] == 'playoff_group_count':
        playoff_group_count = i[1]

    if i[2] == 'tier_count':
        tier_count = i[1]

    if i[2] == 'advance_count':
        advance_count = i[1]

    if i[2] == 'prelim_round_count':
        prelim_round_count = i[1]

    if i[2] == 'playoff_round_count':
        playoff_round_count = i[1]

    if i[2] == 'sunday_round_count':
        sunday_round_count = i[1]

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
