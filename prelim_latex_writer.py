#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% import section
import time
from pylatex import (Document, Section, Subsection, Tabularx, Command,
                     NewPage, PageStyle, LargeText, HugeText,
                     LineBreak, LongTable, MultiColumn,
                     MultiRow, VerticalSpace, NewLine)
from pylatex.utils import NoEscape
from cornerstone_input import (start_time,
                               list_of_teams, team_code_dict,
                               qr_toggle, text_toggle,
                               qr_codes, qr_captions,
                               texts)

from prelim_scheduler import (full_schedule_grid,
                              code_team_dict,
                              prelim_group_names)
from function_definitions import (prelim_team, start_latex, close_latex,
                                  header_stringify, alternating_rows,
                                  qr_code)
from specific_functions import (get_team_list,
                                get_room_list,
                                specific_team_scheduler,
                                specific_room_scheduler,
                                clean_up_grid)


# %% header, runtime
header = """

Writes .tex file outputs for prelim schedules.

Note: there is a known bug in the latex compiler, and sometimes a file
has to be compiled twice in order for table widths to be formatted properly
in line with their header/footer row. This might be specific to the latex
compiler I'm using, but something to keep aware of.

Created on Wed Oct 13 18:21:31 2021 Eastern Time

@author: Victor Prieto

TODO produce team-specific schedules in alphabetical order, probably not
necessary for room-specific schedules since rooms will be grouped into
brackets? Not a big deal for rooms but definitely helpful for teams.

"""

# starts program runtime
print('\n', header, '\n')
print('start time: %s Eastern Time' % time.ctime())

# %% check if outputs folder exists, if not then create it

# TODO write this, which will enable deleting folder before each test

# TODO this alphabetizer may be key for outputting team-specific schedules
# in alphabetical order, much better for printing organization

# alphabetizes list of teams
# list_of_teams.sort(key=lambda x: x[0])

# %% create team index

filename = 'prelim_team_index'
docname = 'Prelims - Team Index'

# sort teams to be in alphabetical order, and not by seed
list_of_teams = sorted(list_of_teams, key=lambda x: (x[0]))

doc = start_latex(filename, docname)

doc.append(NoEscape(r'\rowcolors{3}{gray!15}{white}'))

alternating_rows(doc, 'gray!15')
with doc.create(LongTable('|ll|c|')) as table:
    table.append(NoEscape(r'\rowcolor{gray!30}'))
    head_foot_row = (r'\textbf{Team Name} & \textbf{Code}'
                     + r'&\textbf{Prelim Group}\\')
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
        team = prelim_team(i[0], team_code_dict[i[0]], i[1], i[2])
        table.add_row(team.name, team.code, team.prelim_group)
doc = close_latex(filename, doc)

# %% create full standard schedule

filename = 'prelim_full_schedule'
docname = 'Prelims - Complete Schedule'

doc = start_latex(filename, docname)

for index, prelim_group in enumerate(prelim_group_names):
    alternating_rows(doc, 'gray!15')
    table_title = f'Prelim Group: {prelim_group}\n'
    with doc.create(Section(table_title, numbering=False)):

        schedule_grid = full_schedule_grid[index]

        # remove first row in order to add hline between header and table
        grid_header = schedule_grid[0]
        basic_schedule_grid = schedule_grid[1:]
        teamcount = len(basic_schedule_grid[0])-1

        # write table using schedule_grid + header_stringify for Tabular string
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

filename = 'prelim_individual_team_schedules'
docname = 'Prelims - Individual Team Schedules'
doc = start_latex(filename, docname)

for index, schedule_grid in enumerate(full_schedule_grid):

    group = prelim_group_names[index]
    print(f'\n{group}\n')

    room_list = get_room_list(schedule_grid)
    team_list = get_team_list(schedule_grid)
    # FIXME does this next line still apply for odd rounds? prob not.
    round_count = len(team_list)
    basic_schedule_grid = clean_up_grid(schedule_grid)

    # iterate for each team in teamlist
    for team in team_list:  # FIXME arrange teams in alphabetical order!
        alternating_rows(doc, 'gray!15')
        team_name = code_team_dict[team]
        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText(team_name))
        doc.append(VerticalSpace('12pt'))
        doc.append(LineBreak())
        doc.append(LargeText(f'Prelim Group - {group}'))
        doc.append(NoEscape(r'\end{center}'))
        doc.append(VerticalSpace('4pt'))

        schedule = specific_team_scheduler(team,
                                           basic_schedule_grid,
                                           room_list,
                                           code_team_dict)

        width = r"\textwidth"
        with doc.create(Tabularx('|c|Y|Y|',
                                 width_argument=NoEscape(width))) as table:

            table.add_hline()
            table.add_row(schedule[0], strict=False)
            table.add_hline()
            for row in schedule[1:]:
                table.add_row(row, strict=False)
            table.add_hline()

        if text_toggle is True:
            doc.append(VerticalSpace('30pt'))
            doc.append(LineBreak())
            doc.append(texts[0])
            doc.append(VerticalSpace('30pt'))
            doc.append(NewLine())
        else:
            doc.append(VerticalSpace('80pt'))  # TODO verify this works
            doc.append(LineBreak())

        if qr_toggle is True:
            qr_codes_1 = qr_codes[0:3]
            qr_captions_1 = qr_captions[0:3]
            qr_code(doc, qr_codes_1, qr_captions_1)

        doc.append(NewPage())

doc = close_latex(filename, doc)

# %% create room-specific schedules

filename = 'prelim_individual_room_schedules'
docname = 'Prelims - Individual Room Schedules'
doc = start_latex(filename, docname)

for index, schedule_grid in enumerate(full_schedule_grid):

    group = prelim_group_names[index]

    room_list = get_room_list(schedule_grid)
    # FIXME do these two lines still apply for odd rounds? prob not.
    team_list = get_team_list(schedule_grid)
    round_count = len(team_list)  # FIXME not sure why this line is here...
    clean_up_grid(schedule_grid)

    # iterate for each room in roomlist
    for room in room_list:

        if room == 'BYE':
            continue

        schedule = specific_room_scheduler(room,
                                           schedule_grid,
                                           room_list,
                                           code_team_dict)

        # put room name above room-specific schedule
        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText('Individual Room Schedule'))
        doc.append(VerticalSpace('16pt'))
        doc.append(LineBreak())
        doc.append(NoEscape(r'\begin{Large}'))
        doc.append(NoEscape(fr'Prelim Group: {group} \hfill Room: {room}'))
        doc.append(NoEscape(r'\end{Large}'))
        doc.append(NoEscape(r'\end{center}'))

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
        doc.append(VerticalSpace('16pt'))
        doc.append(LineBreak())

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

# prints runtime
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
