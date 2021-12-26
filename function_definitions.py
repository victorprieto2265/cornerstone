#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
from pylatex import (Document, Section, Tabular, Command,
                     NewPage, LineBreak, LongTable, HugeText,
                     VerticalSpace, Center, MultiColumn)
from pylatex.utils import NoEscape
from tournament_format import (tournament_name, tournament_location,
                               tournament_date)


# place additional modules here

header = """

Depository for a bunch of class and function definitions shared across
prelim/playoff scripts.

TODO what if snake seed is fed a list with odd number of teams?

Created on Mon Nov 1 13:53:44 2021 Eastern Time

@author: Victor Prieto

"""


# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s' % time.ctime())

# %% function definitions


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
            for i in range(wanted_parts)]


def snake_seed(list_of_teams, bracket_count):
    """
    Parameters
    ----------
    list_of_teams : list
        A list of teams for reordering into playoff brackets by snake seeding.
    bracket_count : int
        Number of playoff brackets to snake seed across.

    Returns
    -------
    newlist : list
        Same list of teams accepted as input, but reordered by snake seeding.
        Example:
            (1, 2, 3, 4... 23, 24)
            snake seeded across four brackets becomes
            (1, 8, 9, 16, 17, 24, 2, 7, 10, 15, 18... 12, 13, 20, 21)

    """

    # generates sequence of indices for snake seeding
    sequence_length = 2 * bracket_count
    reps = len(list_of_teams) / sequence_length
    sequence = []
    for i in range(0, int(sequence_length/2)):
        for j in range(0, int(reps)):
            sequence.append(i+j*sequence_length)
            sequence.append((sequence_length-1-i)+j*sequence_length)

    # quits program if odd number of teams in list_of_teams
    if (len(list_of_teams)) % 2 == 1:
        print('ODD NUMBER OF TEAMS DETECTED')
        sys.exit()

    # use sequence of indices to generate new list of teams
    newlist = (list_of_teams[index] for index in sequence)
    return newlist


def alternating_rows(doc, color):
    return doc.append(NoEscape(r'\rowcolors{3}{%s}{white}' % color))


def duplicate_checker(alist):
    seen = set()
    for x in alist:
        if x in seen:
            return True
        seen.add(x)
    return False


def start_latex(filename_input, docname, title=True, fontsize=False):
    geometry_options = {
        "includeheadfoot": True
    }
    doc = Document(filename_input, geometry_options=geometry_options)

    # this changed font sizes, but it doesn't work so well
    if fontsize is True:
        doc = Document(filename_input, geometry_options=geometry_options,
                       font_size='')
        doc.append(Command('fontsize', arguments=['12', '12']))
        doc.append(Command('selectfont'))

    doc.preamble.append(Command('title', tournament_name))
    doc.preamble.append(Command('author', tournament_location))
    doc.preamble.append(Command('date', tournament_date))

    doc.append(NoEscape(r'\newcolumntype{Y}{>{\centering\arraybackslash}X}'))

    # TODO vertically center docname text on page
    if title is True:
        doc.append(NoEscape(r'\maketitle'))
        doc.append(VerticalSpace('48pt'))
        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText(docname))
        doc.append(NoEscape(r'\end{center}'))
        doc.append(NewPage())

    return doc


def close_latex(filename_input, doc_input):
    doc_input.generate_tex()

    file = open(filename_input + '.tex')
    latex_string = file.read()
    bad_string = '\\usepackage{lastpage}%'
    good_string = '\\usepackage[table]{xcolor}'
    # print(latex_string)
    latex_string = latex_string.replace(bad_string, good_string)

    # for visual debugging
    # print('\n\n', latex_string[0:700], '\n\n')

    with open(f'{filename_input}.tex', 'w') as f:
        f.write(latex_string)


# %% classes, mostly not in use
# TODO figure out class inheritance for team/prelim_team/playoff_team
class team:
    def __init__(self,
                 name,
                 code):
        self.name = name
        self.code = code


class prelim_team(team):
    def __init__(self,
                 name,
                 code,
                 prelim_group,
                 prelim_seed):
        super().__init__(name, code)
        self.prelim_group = prelim_group
        self.prelim_seed = prelim_seed


class playoff_team():
    def __init__(self,
                 name,
                 code,
                 prelim_group,
                 playoff_bracket,
                 playoff_seed):  # playoff seed also the prelim finish
        self.name = name
        self.code = code
        self.prelim_group = prelim_group
        self.playoff_bracket = playoff_bracket
        self.playoff_seed = playoff_seed


# %% class inheritance examples
team1 = prelim_team('Manheim Township', 'MTA', 'A', 1)
team2 = prelim_team('Great Valley', 'GVA', 'A', 2)
team3 = prelim_team('State College', 'SCA', 'B', 1)
team4 = prelim_team('State College B', 'SCB', 'B', 2)

print(team3.code)

team5 = playoff_team(team1.name, team1.code, team1.prelim_group, 'Accra', 1)
team6 = playoff_team(team3.name, team3.code, team3.prelim_group, 'Accra', 2)
team7 = playoff_team(team2.name, team2.code, team2.prelim_group, 'Belmopan', 1)
team8 = playoff_team(team4.name, team4.code, team4.prelim_group, 'Belmopan', 2)

print(team8.playoff_seed)

# %% more function definitions


def header_stringify(teamcount, tabularx=False):
    """

    Parameters
    ----------
    teamcount : int
        Number of teams in the round robin.
    tabularx : bool, optional
        Changes header string to account for newcolumntype Y, used in tabularx.
        The default is False.

    Returns
    -------
    A string for pylatex to use when defining the table.
    Example: '|l|cc|cc|cc|cc|'

    If tabularx is set to True, returns a string that utilizes newcolumntype Y.
    Example: '|l|Y|Y|Y|Y|Y|Y|'

    """

    roomcount = teamcount // 2

    header_string = '|l' + ('|cc' * roomcount + '|')
    if teamcount % 2 == 1:
        header_string = header_string + 'c|'

    if tabularx is True:
        header_string = '|l' + ('|Y' * teamcount + '|')

    return header_string


# %% prints runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
