#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% import modules/functions, header
import time
import os
from pylatex import (Document, Section, Subsection, Tabularx, Command,
                     NewPage, PageStyle, LargeText, HugeText,
                     LineBreak, LongTable, MultiColumn,
                     MultiRow, VerticalSpace, NewLine)
from pylatex.utils import NoEscape

from cornerstone_input import (list_of_teams, format_dict,
                               super_bracket_names,
                               qr_toggle, text_toggle,
                               code_team_dict, team_code_dict,
                               qr_codes, qr_captions,
                               texts)
from super_scheduler import (full_schedule_grid,
                             teamcode_super_dict,
                             round_start)
# from playoff_scheduler import (teamcode_playoff_dict)
from function_definitions import (team, start_latex, close_latex,
                                  header_stringify, alternating_rows,
                                  qr_code)
from specific_functions import (get_team_list,
                                get_room_list,
                                specific_team_scheduler,
                                specific_room_scheduler,
                                clean_up_grid)

header = """

Writes .tex outputs for superplayoffs schedule.

Created on Sun Jan  2 15:42:28 2022

@author: Victor Prieto

"""


# %% start runtime
start_time = time.time()
print('\n', header)
print('start time: %s' % time.ctime())

# %% sort teams alphabetically (can change to other orders perhaps)

list_of_teams = sorted(list_of_teams, key=lambda x: (x[0]))

print(list_of_teams)

# %% create team index

filename = 'super_team_index'
docname = 'Team Index'

doc = start_latex(filename, docname)

doc.append(NoEscape(r'\lfoot{*PPB is up to date through playoffs.}'))
doc.append(NoEscape(r'\rowcolors{3}{gray!15}{white}'))

alternating_rows(doc, 'gray!15')
with doc.create(LongTable('|llllc|')) as table:
    table.append(NoEscape(r'\rowcolor{gray!30}'))
    head_foot_row = (r'\textbf{Team Name} & \textbf{Code}'
                     + r'&\textbf{PPB*}'
                     + r'&\textbf{Superplayoff Bracket}'
                     + r'&\textbf{W-L}\\')
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
        teamname = i[0]
        teamcode = team_code_dict[teamname]
        playoff_finish = i[2]
        ppb = '%s' % '%.2f' % i[3]
        super_bracket = teamcode_super_dict[teamcode][:-1]
        super_seed = int(teamcode_super_dict[teamcode][-1])
        if playoff_finish % 2 == 1:
            record = '1-0'
        else:
            record = '0-1'
        table.add_row(teamname, teamcode, ppb,
                      super_bracket, record)

doc = close_latex(filename, doc)

# %% create full standard grid schedule

filename = 'super_full_schedule'
docname = 'Superplayoffs - Complete Schedule'

doc = start_latex(filename, docname)

for index, super_bracket in enumerate(super_bracket_names):
    alternating_rows(doc, 'gray!15')
    table_title = f'Superplayoff Bracket: {super_bracket}'
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

filename = 'super_individual_team_schedules'
docname = 'Superplayoffs - Individual Team Schedules'
doc = start_latex(filename, docname)

# TODO remove me after NSC
normal_text = r'\lfoot{All teams begin superplayoffs with either 1 win or 1 loss.}'
doc.append(NoEscape(normal_text))

for index, schedule_grid in enumerate(full_schedule_grid):

    bracket = super_bracket_names[index]

    room_list = get_room_list(schedule_grid)
    team_list = get_team_list(schedule_grid)
    # FIXME does this next line still apply for odd rounds? prob not.
    round_count = len(team_list)
    basic_schedule_grid = clean_up_grid(schedule_grid)

    # iterate for each team in teamlist
    for team in team_list:
        team_name = code_team_dict[team]

        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText(team_name))
        doc.append(VerticalSpace('12pt'))
        doc.append(LineBreak())
        doc.append(LargeText(f'Superplayoff Bracket - {bracket}'))
        doc.append(NoEscape(r'\end{center}'))
        doc.append(VerticalSpace('4pt'))

        schedule = specific_team_scheduler(team,
                                           basic_schedule_grid,
                                           room_list,
                                           code_team_dict,
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
        doc.append(NewLine())

        if text_toggle is True:
            doc.append(VerticalSpace('30pt'))
            doc.append(LineBreak())
            doc.append(texts[0])
            doc.append(VerticalSpace('30pt'))
            doc.append(NewLine())

        if qr_toggle is True:
            qr_codes_2 = qr_codes[3:6]
            qr_captions_2 = qr_captions[3:6]
            qr_code(doc, qr_codes_2, qr_captions_2)

        doc.append(NewPage())

doc = close_latex(filename, doc)


# %% create room-specific schedules

filename = 'super_individual_room_schedules'
docname = 'Superplayoffs - Individual Room Schedules'
doc = start_latex(filename, docname)

for index, schedule_grid in enumerate(full_schedule_grid):

    bracket = super_bracket_names[index]

    room_list = get_room_list(schedule_grid)
    # FIXME do these two lines still apply for odd rounds? prob not.
    team_list = get_team_list(schedule_grid)
    round_count = len(team_list)  # FIXME not sure why this line is here...
    clean_up_grid(schedule_grid)

    # iterate for each room in roomlist
    for room in room_list:

        schedule = specific_room_scheduler(room,
                                           schedule_grid,
                                           room_list,
                                           code_team_dict,
                                           round_start=round_start)

        # bracket and room above room specific schedule

        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText('Individual Room Schedule'))
        doc.append(VerticalSpace('16pt'))
        doc.append(LineBreak())
        doc.append(NoEscape(r'\begin{Large}'))
        doc.append(NoEscape(fr'Superplayoff Bracket: {bracket} \hfill Room: {room}'))
        doc.append(NoEscape(r'\end{Large}'))
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
                doc.append(NoEscape(r'Score | Initial&|&|\\'))
                table.add_hline()
        doc.append(VerticalSpace('8pt'))
        doc.append(NewLine())

        if text_toggle is True:
            doc.append(texts[1])
            doc.append(VerticalSpace('30pt'))
            doc.append(NewLine())

        if qr_toggle is True:
            qr_codes_2 = qr_codes[3:6]
            qr_captions_2 = qr_captions[3:6]
            qr_code(doc, qr_codes_2, qr_captions_2)

        doc.append(NewPage())

doc = close_latex(filename, doc)

# %% end runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
