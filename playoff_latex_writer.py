#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% import section
import time
from pylatex import (Document, Section, Tabularx, Command,
                     NewPage, LineBreak, LongTable, HugeText,
                     VerticalSpace, Center, LargeText)
from pylatex.utils import NoEscape

from function_definitions import (start_latex, close_latex,
                                  header_stringify, playoff_team,
                                  alternating_rows)
from playoff_scheduler import (full_schedule_grid, playoff_teamcode_dict,
                               teamcode_playoff_dict)
from tournament_format import (tournament_name, tournament_location,
                               tournament_date, playoff_team_count,
                               prelim_round_count)
from cornerstone_input import (list_of_teams, playoff_bracket_names,
                               code_team_dict, lorem)
from specific_functions import (get_team_list,
                                get_room_list,
                                specific_team_scheduler,
                                specific_room_scheduler,
                                clean_up_grid)
import os
import os.path

# %% header, runtime
header = r"""

Writes .tex file outputs for playoff schedules.

TODO is NoEscape(\cellcolor{gray}) consistent throughout both latex writers?

Created on Mon Nov 1 14:16:49 2021 Eastern Time

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('\n', header, '\n')
print('start time: %s Eastern Time' % time.ctime())

# %% create team index

filename = './outputs/playoff_team_index'
docname = 'Team Index'

doc = start_latex(filename, docname)

doc.append(NoEscape(r'\rowcolors{3}{gray!15}{white}'))

alternating_rows(doc, 'gray!15')
with doc.create(LongTable('|ll|lc|l|')) as table:
    table.append(NoEscape(r'\rowcolor{gray!30}'))
    head_foot_row = (r'\textbf{Team Name} & \textbf{Code}'
                     + r'&\textbf{Prelim Group}'
                     + r'&\textbf{Prelim Finish}'
                     + r'&\textbf{Playoff Bracket}\\')
    table.add_hline()
    table.append(NoEscape(head_foot_row))
    table.add_hline()
    table.end_table_header()
    table.add_hline()
    table.append(NoEscape(r'\rowcolor{gray!25}'))
    table.append(NoEscape(head_foot_row))
    table.add_hline()
    table.end_table_footer()
    table.add_hline()
    table.append(NoEscape(r'\hline\rowcolor{gray!25}'))
    table.append(NoEscape(head_foot_row))
    table.add_hline()
    table.end_table_last_footer()
    table.add_hline()
    for i in list_of_teams:
        playoff_seed = teamcode_playoff_dict[i[1]][-1]
        playoff_bracket = teamcode_playoff_dict[i[1]][:-1]

        team = playoff_team(i[0], i[1], i[2],
                            playoff_bracket, playoff_seed)
        table.add_row(team.name, team.code, team.prelim_group,
                      team.playoff_seed, team.playoff_bracket)

doc = close_latex(filename, doc)


# %% create full standard grid schedule

filename = './outputs/playoff_full_schedule'
docname = 'Playoffs - Complete Schedule'

doc = start_latex(filename, docname)

for index, playoff_bracket in enumerate(playoff_bracket_names):
    alternating_rows(doc, 'gray!15')
    table_title = f'Playoff Bracket: {playoff_bracket}'
    with doc.create(Section(table_title, numbering=False)):

        schedule_grid = full_schedule_grid[index]

        # remove first row in order to add hline between header and table
        grid_header = schedule_grid[0]
        basic_schedule_grid = schedule_grid[1:]
        teamcount = len(basic_schedule_grid[0])-1

        header_string = header_stringify(teamcount, tabularx=True)
        with doc.create(Tabularx(header_string,
                        width_argument=NoEscape(r"\textwidth"))) as table:
            grid_header[0] = NoEscape('\\cellcolor{gray}')
            table.add_hline()
            table.add_row(grid_header, strict=False)
            table.add_hline()
            for row in basic_schedule_grid:
                table.add_row(row, strict=False)
            table.add_hline()
        doc.append(VerticalSpace('8pt'))
        doc.append(LineBreak())

doc = close_latex(filename, doc)

# %% create team-specific schedules
# TODO expand to schedules with byes

schedule_path = r'./outputs/playoff_team_specific_schedules/'

try:
    os.mkdir(schedule_path)
except FileExistsError:
    None

filename = schedule_path + 'team_specific_schedules'
docname = 'Playoff Schedules - Team Specific'
doc = start_latex(filename, docname)

for index, schedule_grid in enumerate(full_schedule_grid):

    bracket = playoff_bracket_names[index]

    room_list = get_room_list(schedule_grid)
    team_list = get_team_list(schedule_grid)
    # FIXME does this next line still apply for odd rounds? prob not.
    round_count = len(team_list)
    basic_schedule_grid = clean_up_grid(schedule_grid)

    # define number for first round in schedule
    round_start = prelim_round_count+1

    # iterate for each team in teamlist
    for team in team_list:
        team_name = code_team_dict[team]

        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText(team_name))
        doc.append(VerticalSpace('8pt'))
        doc.append(LineBreak())
        doc.append(LargeText(f'Playoff Bracket - {bracket}'))
        doc.append(NoEscape(r'\end{center}'))

        schedule = specific_team_scheduler(team,
                                           basic_schedule_grid,
                                           room_list,
                                           round_start=round_start)

        alternating_rows(doc, 'gray!15')

        width = r"\textwidth"
        with doc.create(Tabularx('|c|Y|Y|',
                                 width_argument=NoEscape(width))) as table:

            table.add_hline()
            table.add_row(schedule[0], strict=False)
            table.add_hline()
            for row in schedule[1:]:
                table.add_row(row, strict=False)
            table.add_hline()
        doc.append(VerticalSpace('8pt'))
        doc.append(LineBreak())

        # for eventual text input
        doc.append(lorem)

        doc.append(VerticalSpace('30pt'))
        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText('QR codes go here'))
        doc.append(NoEscape(r'\end{center}'))

        doc.append(NewPage())

doc = close_latex(filename, doc)


# %% create room-specific schedules

schedule_path = r'./outputs/playoff_room_specific_schedules/'

try:
    os.mkdir(schedule_path)
except FileExistsError:
    None

filename = schedule_path + 'room_specific_schedules'
docname = 'Playoff Schedules - Room Specific'
doc = start_latex(filename, docname)

for index, schedule_grid in enumerate(full_schedule_grid):

    bracket = playoff_bracket_names[index]

    room_list = get_room_list(schedule_grid)
    # FIXME do these two lines still apply for odd rounds? prob not.
    team_list = get_team_list(schedule_grid)
    round_count = len(team_list)  # FIXME not sure why this line is here...
    clean_up_grid(schedule_grid)

    # define number for first round in schedule
    round_start = prelim_round_count+1

    # iterate for each room in roomlist
    for room in room_list:

        schedule = specific_room_scheduler(room,
                                           schedule_grid,
                                           room_list,
                                           round_start=round_start)

        # bracket and room above room specific schedule

        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText('Room Specific Playoff Schedule'))
        doc.append(VerticalSpace('8pt'))
        doc.append(LineBreak())
        doc.append(LargeText(f'Bracket - {bracket}'))
        doc.append(VerticalSpace('8pt'))
        doc.append(LineBreak())
        doc.append(VerticalSpace('8pt'))
        doc.append(LargeText(f'Room - {room}'))
        doc.append(NoEscape(r'\end{center}'))

        # create table with formatting
        alternating_rows(doc, 'gray!15')
        width = r"\textwidth"
        with doc.create(Tabularx('|c|Y|Y|',
                                 width_argument=NoEscape(width))) as table:
            table.add_hline()
            table.add_row(schedule[0], strict=False)
            table.add_hline()
            for row in schedule[1:]:
                table.add_row(row, strict=False)
            table.add_hline()
        doc.append(VerticalSpace('8pt'))

        # for eventual text input
        doc.append(lorem[1:701])

        doc.append(VerticalSpace('140pt'))
        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText('QR codes go here'))
        doc.append(NoEscape(r'\end{center}'))

        doc.append(NewPage())

doc = close_latex(filename, doc)

# %% end runtime

# for visual debugging
# print('\n\n***full schedule grid 1***\n\n')
# print(*full_schedule_grid[0:3], sep='\n\n')

print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
