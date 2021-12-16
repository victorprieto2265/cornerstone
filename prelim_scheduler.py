#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from cornerstone_input import (prelim_group_names,
                               prelim_room_dict,
                               prelim_teamcode_dict)
from standard_scheduler import standard_schedule

header = """

This script reads the list of prelim teams and the tournament format files
to produce a set of prelim schedules.

Created on Mon Oct 11 19:57:37 2021 Eastern Time

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s Eastern Time' % time.ctime())

full_schedule_grid = []

# perform this process for each prelim group, add to full_schedule_grid
for group_name in prelim_group_names:

    schedule_grid = (standard_schedule(group_name,
                                       prelim_teamcode_dict,
                                       prelim_room_dict))
    full_schedule_grid.append(schedule_grid)

# for visual debugging
# for index, prelim_group in enumerate(prelim_group_names):
#     print(f'\nPrelim Group: {prelim_group}')
#     print(*full_schedule_grid[index], sep='\n')

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
