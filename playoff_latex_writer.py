#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% import section
import time
from pylatex import (Document, Section, Tabularx, Command,
                     NewPage, LineBreak, LongTable, HugeText,
                     VerticalSpace, Center, LargeText, NewLine)
from pylatex.utils import NoEscape, italic

from function_definitions import (start_latex, close_latex,
                                  header_stringify, playoff_team,
                                  alternating_rows, qr_code)
from playoff_scheduler import (full_schedule_grid,
                               teamcode_playoff_dict,
                               prelim_round_count,
                               crossover,
                               first_playoff_rooms)
# from tournament_format import (tournament_name, tournament_location,
#                                tournament_date, playoff_team_count,
#                                )
from cornerstone_input import (list_of_teams, playoff_bracket_names,
                               code_team_dict, team_code_dict,
                               qr_toggle, text_toggle,
                               qr_codes, qr_captions,
                               texts)
from specific_functions import (get_team_list,
                                get_room_list,
                                specific_team_scheduler,
                                specific_room_scheduler,
                                clean_up_grid)

# %% header, runtime
header = r"""

Writes .tex file outputs for playoff schedules.

Created on Mon Nov 1 14:16:49 2021 Eastern Time

@author: Victor Prieto

"""

# starts program runtime
start_time = time.time()
print('\n', header, '\n')
print('start time: %s Eastern Time' % time.ctime())

# %% define some variables common to all prints

# define number for first round in schedule
round_start = prelim_round_count+1


# %% create team index

filename = 'playoff_team_index'
docname = 'Playoffs - Team Index'

# sort teams to be in alphabetical order, and not by seed
list_of_teams = sorted(list_of_teams, key=lambda x: (x[0]))

doc = start_latex(filename, docname)

# # TODO remove me after NSC
# normal_text = r'\lfoot{All teams begin playoffs with a record of 0-0.}'
# doc.append(NoEscape(normal_text))

doc.append(NoEscape(r'\rowcolors{3}{gray!15}{white}'))

alternating_rows(doc, 'gray!15')
with doc.create(LongTable('|l|lcc|l|')) as table:
    table.append(NoEscape(r'\rowcolor{gray!30}'))
    head_foot_row = (r'\textbf{Team Name} '
                     + r'&\textbf{Prelim Bracket}'
                     + r'&\textbf{Finish}'
                     + r'&\textbf{PPB}'
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
        teamcode = team_code_dict[i[0]]
        playoff_seed = teamcode_playoff_dict[teamcode][-1]
        prelim_finish = i[2]
        ppb = '%s' % '%.2f' % i[3]
        playoff_bracket = teamcode_playoff_dict[teamcode][:-1]
        team = playoff_team(i[0], teamcode, i[1],
                            playoff_bracket, playoff_seed)
        table.add_row(team.name,
                      team.prelim_group, prelim_finish,
                      ppb, team.playoff_bracket)

# # # %% team index crossover text
# if crossover != 'N':
#     normal_text = 'Teams with an odd number in the "Prelim Finish" column begin playoffs with one win, while teams with an even number begin playoffs with one loss.'
#     italic_text = ' Exception: any team who was the only team to advance from their prelim bracket starts with no wins and no losses.'
#     doc.append(normal_text)
#     doc.append(italic(italic_text))

doc = close_latex(filename, doc)


# %% create full standard grid schedule

filename = 'playoff_full_schedule'
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

filename = 'playoff_individual_schedules'
docname = 'Playoffs - Individual Team Schedules'
doc = start_latex(filename, docname)

# TODO remove me after NSC
# normal_text = r'\lfoot{All teams begin superplayoffs with a record of 0-0.}'
# doc.append(NoEscape(normal_text))


for index, schedule_grid in enumerate(full_schedule_grid):

    bracket = playoff_bracket_names[index]

    room_list = get_room_list(schedule_grid)
    team_list = get_team_list(schedule_grid)

    round_count = len(team_list)
    basic_schedule_grid = clean_up_grid(schedule_grid)
    
    # iterate for each team in teamlist
    for team in team_list:
        
        
        team_name = code_team_dict[team]

        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText(team_name))
        doc.append(VerticalSpace('12pt'))
        doc.append(LineBreak())
        doc.append(LargeText(f'Playoff Bracket - {bracket}'))
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

filename = 'playoff_individual_room_schedules'
docname = 'Playoffs - Individual Room Schedules'
doc = start_latex(filename, docname)

for index, schedule_grid in enumerate(full_schedule_grid):

    bracket = playoff_bracket_names[index]

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
        doc.append(NoEscape(fr'Playoff Bracket: {bracket} \hfill Room: {room}'))
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

# %% create schedule for first round of playoffs, "Quickstart"

filename = 'playoff_quickstart'
docname = 'Playoffs - Quickstart'
doc = start_latex(filename, docname)

doc.append(NoEscape(r'\begin{center}'))
doc.append(HugeText('First Playoff Room for All Teams'))
doc.append(VerticalSpace('12pt'))
doc.append(LineBreak())
doc.append(NoEscape(r'\end{center}'))

doc.append(NoEscape(r'\rowcolors{3}{gray!15}{white}'))

alternating_rows(doc, 'gray!15')
with doc.create(LongTable('|l|ccc|')) as table:
    table.append(NoEscape(r'\rowcolor{gray!30}'))
    head_foot_row = (r'\textbf{Team Name} '
                      + r'&\textbf{Prelim Bracket}'
                      + r'&\textbf{Playoff Bracket}'
                      + r'&\textbf{First Playoff Room}\\')
    table.add_hline()
    table.append(NoEscape(head_foot_row))
    table.end_table_header()
    table.append(NoEscape(r'\rowcolor{gray!25}'))
    table.append(NoEscape(head_foot_row))
    table.end_table_footer()
    table.append(NoEscape(r'\hline\rowcolor{gray!25}'))
    table.append(NoEscape(head_foot_row))
    table.end_table_last_footer()
    table.add_hline()

    for i in list_of_teams:
        teamcode = team_code_dict[i[0]]
        playoff_seed = teamcode_playoff_dict[teamcode][-1]
        prelim_finish = i[2]
        ppb = '%s' % '%.2f' % i[3]
        playoff_bracket = teamcode_playoff_dict[teamcode][:-1]
        team = playoff_team(i[0], teamcode, i[2],
                            playoff_bracket, playoff_seed)
        first_room = first_playoff_rooms[teamcode]
        table.add_row(team.name,
                      team.prelim_group,
                      team.playoff_bracket,
                      first_room)
        
    table.add_hline()

doc = close_latex(filename, doc)


# %% end runtime

# for visual debugging
# print('\n\n***full schedule grid 1***\n\n')
# print(*full_schedule_grid[0:3], sep='\n\n')

print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
