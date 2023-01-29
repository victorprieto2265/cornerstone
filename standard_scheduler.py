#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% import modules/functions, header
import time, sys
import pandas as pd
from pylatex import MultiColumn


header = """

Created on Mon Nov 22 12:50:12 2021

Definition of functions used for creating a table for a round robin schedule,
between 4 and 14 teams.

TODO create new files for crossover templates other than B8
TODO maybe write function (called pylatex_stringer) that does the following:
1. pylatex writes to a .tex file
2. python reads the .tex file as a string, then deletes the file
TODO if possible, fix pylatex table lines and shading in this function

@author: Victor Prieto

"""


# %% start runtime
start_time = time.time()
print('\n', header)
print('start time: %s' % time.ctime())

# %% function definitions


def standard_schedule(group_name, teamcode_dict, room_dict, roundstart=1,
                      crossover=False, superplayoff=False):
    """


    Parameters
    ----------
    groupname : string
        String of the prelim group or playoff bracket name.
        Example: Lilongwe
    teamcode_dict : dict
        k : v = a group/bracket code : teamcode corresponding to that code
        example: Lilongwe4 = MBA
    room_dict : dict
        k : v = a group/bracket code : room corresponding to that code
        example: Lilongwe2 = Suite 1132
    roundstart : int, optional
        Number for the first round in the schedule. The default is 1.

    Returns
    -------
    schedule_grid : list
        Latex-friendly table. First row = table header, remaining rows =
        schedule for each round.

    """

    # produce teamlist
    teamlist = [k for k, v in list(teamcode_dict.items())
                if k.startswith(group_name)]
    sorted_list = sorted(teamlist)
    teamlist = [teamcode_dict[i] for i in sorted_list]

    # identify number of teams in teamlist and appropriate number of rooms
    teamcount = len(teamlist)
    roomcount = teamcount // 2

    # identify correct rr_schedule and import template
    rr_schedule = f"./templates/rr_schedules/rr_{teamcount}"

    if crossover is not False:
        rr_schedule = f"./templates/rr_schedules/rr_crossover_{crossover}{teamcount}"

    try:
        rr_schedule = pd.read_excel(f'{rr_schedule}.xlsx').values.tolist()
    except FileNotFoundError:
        print(f'*** WARNING ***\nNo file found for "{rr_schedule}"... '
              + 'Or, too many prelim groups or playoff brackets?')
        sys.exit()

    # produce roomlist
    roomlist = [k for k, v in list(room_dict.items())
                if k.startswith(group_name)]
    roomlist = [room_dict[i] for i in sorted(roomlist)]

    # produce header, including bye
    rooms = []
    header = ['']
    for index in range(roomcount):
        room = roomlist[index]
        rooms.append(room)
        header.append(MultiColumn(2, align='c|', data=room))

    if teamcount % 2 == 1:
        header.append('BYE')

    # use rr_schedule template and roundstart to produce rest of schedule grid
    schedule_grid = [header]
    for round_num, row in enumerate(rr_schedule):
        round_num += roundstart
        new_row = [f'Round {round_num}']
        for index in row:
            code = group_name + str(index)
            team = teamcode_dict[code]
            new_row.append(team)
        schedule_grid.append(new_row)

    # for debugging
    print('\n\n***schedule grid***\n\n')
    print(*schedule_grid, sep='\n')
    print('\n\n')

    return schedule_grid


# %% end runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
