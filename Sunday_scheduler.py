#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% import modules/functions, header
import time
import os

from cornerstone_input import sunday_input
from playoff_scheduler import playoff_team_list

scriptname = os.path.basename(__file__)

description = f"""

*** script executed = {scriptname} ***

This script analyzes [various inputs to be described later] and passes
a schedule grid for sunday_latex_writer to read.

TODO: there is a potential bug in this script: it is possible (although rare)
that, when rebracketing, some teams will carry over a game while others
do not. This will present a problem when attempting to figure out
which teams have a carryover game. This is a rare enough occurrence that it
probably isn't worth dealing with now, but keep it in mind.

Created on Thu Dec 23 19:25:05 2021

@author: Victor Prieto

"""


# %% start runtime
start_time = time.time()
print('\n', description)
print('start time: %s' % time.ctime())

# %% insert code below

for sublist in sunday_input:
    print(sublist)
print('\n\n')

sunday_bracket_list = [sublist[3] for sublist in sunday_input]
carryover_brackets = [sublist[3] for sublist in sunday_input
                      if sublist[5] != 0]
# TODO remove duplicates from both of those lists
# TODO see description in script header


for index, bracket in enumerate(sunday_bracket_list):
    print(f'\nbracket currently being scheduled: {bracket}')
    if index == 8:
        break

    


    
# %% end runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
