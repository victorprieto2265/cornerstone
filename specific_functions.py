#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pylatex import NoEscape

scriptname = os.path.basename(__file__)

description = f"""

*** script executed = {scriptname} ***

Created on Tue Nov 16 17:11:20 2021

This script defines a few functions needed for specific_latex_writer.py,
which outputs schedules specific to teams and rooms.

@author: Victor Prieto

"""

# %% getteamlist, getroomlist, find opponent, find room functions


# what are the teams in the group?
def get_team_list(schedule_grid):
    team_list = sorted(schedule_grid[1][1:])
    return team_list


# what are the rooms in the group?
def get_room_list(schedule_grid):
    # remove first element in header, which should be a gray box
    header = schedule_grid[0][1:]
    room_list = [i[0] for i in header]
    if 'BYE' in header:
        room_list[-1] = 'BYE'
    return room_list


# for a given team in a given round, what team do they play and where?
def find_opponent(team, row, room_list, code_dict):
    index = row.index(team)
    room = room_list[index]
    if row[-1] == team and room_list[-1] == 'BYE':
        opponent = 'BYE'
    elif index % 2 == 0:
        opponent_code = row[index+1]
        opponent = code_dict[opponent_code]
    else:
        opponent_code = row[index-1]
        opponent = code_dict[opponent_code]
    return room, opponent


# what teams are in a room at a given round?
def find_teams(row, room, roomlist, code_dict):
    index = roomlist.index(room)
    teams = row[2*index:2*index+2]
    teams = [*map(code_dict.get, teams)]
    return sorted(teams)  # alphabetically sorts teams


def clean_up_grid(schedule_grid):
    no_header = schedule_grid[1:]
    basic_schedule_grid = []
    for index, row in enumerate(no_header):
        basic_schedule_grid.append(row[1:])

    return basic_schedule_grid


# %% specific schedulers


def specific_team_scheduler(team, schedule_grid, room_list, code_dict,
                            round_start=1):
    # generate room_list with duplicated values
    # need this for finding an opponent at a particular index
    dup_room_list = [room for room in room_list for _ in (0, 1)]

    # how many rounds in the grid?
    rounds = len(schedule_grid)

    specific_grid = [['', 'Room Name', 'Opponent']]
    for i in range(0, rounds):
        room, opponent = find_opponent(team,
                                       schedule_grid[i],
                                       dup_room_list,
                                       code_dict)

        specific_grid.append([f'Round {round_start+i}', room, opponent])

        specific_grid[0][0] = NoEscape('\\cellcolor{gray}')

    # for visual debugging
    # print(*specific_grid, sep='\n')
    # print('\n\n\n\n')

    return specific_grid


def specific_room_scheduler(room, schedule_grid, room_list,
                            code_dict, round_start=1):
    basic_schedule_grid = clean_up_grid(schedule_grid)
    specific_grid = [['', 'Team 1', 'Team 2']]
    for index, row in enumerate(basic_schedule_grid):
        teams = find_teams(row, room, room_list, code_dict)
        if room == 'BYE':
            return 'BYE'
        specific_grid.append([f'Round {round_start+index}',
                              teams[0], teams[1]])

        specific_grid[0][0] = NoEscape('\\cellcolor{gray}')

    return specific_grid

