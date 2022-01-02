#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% import modules/functions, header
import time
import os
import sys

from cornerstone_input import super_input, super_room_dict
from playoff_scheduler import playoff_team_list
from function_definitions import remove_duplicates
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

# %% super input analysis

super_input.sort(key=lambda x: (x[4], x[5]))

print(*super_input, sep='\n')
sys.exit()

super_bracket_list = [sublist[3] for sublist in super_input]
carryover_brackets = [sublist[3] for sublist in super_input
                      if sublist[6] != 0]

super_bracket_list = remove_duplicates(super_bracket_list)
crossover_brackets = remove_duplicates(carryover_brackets)

# create super_teamcode_dict (super_room_dict imported already)
# TODO shift this over to input?
super_team_dict = {}
super_teamcode_dict = {}
for i in super_input:
    print(i)
    key = i[3] + str(i[5])  # bracket-seed
    value = i[0]  # team name
    super_team_dict[key] = value

    value = i[1]  # team code
    super_teamcode_dict[key] = value


# %% super grid scheduling

full_schedule_grid = []

for index, super_bracket in enumerate(super_bracket_list):
    if super_bracket in crossover_brackets:
        crossover = "B"  # FIXME hardcoded to use schedule B
    else:
        crossover = False

    schedule_grid = (standard_schedule(super_bracket,
                                       super_teamcode_dict,
                                       super_room_dict,
                                       crossover=crossover))
    full_schedule_grid.append(schedule_grid)


# for visual debugging
for index, super_bracket in enumerate(super_bracket_list):
    print(f'\nSuper Group: {super_bracket}')
    print(*full_schedule_grid[index], sep='\n')


# %% end runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
