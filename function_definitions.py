#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
from pathlib import Path
from pylatex import (Document, Tabularx, Command,
                     NewPage, HugeText, Package,
                     VerticalSpace)
from pylatex.utils import NoEscape
from cornerstone_input import format_dict

# place additional modules here

header = """

Depository for a bunch of class and function definitions shared across
prelim/playoff scripts.

TODO what if snake seed is fed a list with odd number of teams?

TODO what if qr_count ≠ 3?

Created on Mon Nov 1 13:53:44 2021 Eastern Time

@author: Victor Prieto

"""


# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s' % time.ctime())

# %% function definitions


def qr_code(doc, qr_codes, qr_captions):

    doc.append(NoEscape(r'\rowcolors{3}{white}{white}'))

    qr_count = len(qr_codes)
    if qr_count != 3:
        print('WARNING: number of qr_codes does not equal 3.')
        sys.exit()
    header_string = 'Y' * qr_count
    width = r"\textwidth"

    with doc.create(Tabularx(header_string,
                             width_argument=NoEscape(width))) as table:
        table.add_row(qr_codes, strict=False)
        table.add_empty_row()
        table.add_row(qr_captions, strict=False)


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
        The list is also split into the number of playoff brackets.
        Example:
            (1, 2, 3, 4... 23, 24)
            snake seeded across four brackets becomes
            ((1, 8, 9, 16, 17, 24), (2, 7, 10, 15, 18... 12, 13, 20, 21))

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


def remove_duplicates(alist):
    newlist = []
    [newlist.append(x) for x in alist if x not in newlist]
    return newlist


def start_latex(filename_input, docname, title=True, fontsize=False):

    Path("./outputs/").mkdir(parents=True, exist_ok=True)
    file_path = r'./outputs/'
    Path(file_path).mkdir(parents=True, exist_ok=True)
    filename = file_path + filename_input        
    
    geometry_options = {
        "includeheadfoot": True
    }

    doc = Document(filename, geometry_options=geometry_options)

    # this changed font sizes, but it doesn't work so well
    if fontsize is True:
        doc = Document(filename_input, geometry_options=geometry_options,
                       font_size='')
        doc.append(Command('fontsize', arguments=['12', '12']))
        doc.append(Command('selectfont'))

    doc.preamble.append(Command('title', format_dict['tournament name']))
    doc.preamble.append(Command('author', format_dict['tournament location']))
    doc.preamble.append(Command('date', format_dict['tournament date']))
    
    doc.packages.append(Package('qrcode'))  # add qrcode to packages
    doc.packages.append(Package('fancyhdr'))  # add qrcode to packages

    doc.append(NoEscape(r'\newcolumntype{Y}{>{\centering\arraybackslash}X}'))

    # TODO vertically center docname text on page
    if title is True:
        doc.append(NoEscape(r'\maketitle'))
        doc.append(VerticalSpace('48pt'))
        doc.append(NoEscape(r'\begin{center}'))
        doc.append(HugeText(docname))
        doc.append(NoEscape(r'\end{center}'))
        doc.append(NewPage())
    
    doc.append(NoEscape(r'\pagestyle{fancy}'))
    doc.append(NoEscape(r'\fancyhf{}'))
    date = '{' + format_dict['tournament date'] + '}'
    name = '{' + format_dict['tournament name'] + '}'
    doc.append(NoEscape(fr'\rhead{date}'))
    doc.append(NoEscape(fr'\lhead{name}'))
    doc.append(NoEscape(r'\rfoot{Created by PACE Cornerstone}'))
        
    return doc


def close_latex(filename_input, doc_input):
    file_path = r'./outputs/'
    filename = file_path + filename_input
    doc_input.generate_tex()

    file = open(filename + '.tex')
    latex_string = file.read()
    bad_string = '\\usepackage{lastpage}%'
    good_string = '\\usepackage[table]{xcolor}%'
    # print(latex_string)
    latex_string = latex_string.replace(bad_string, good_string)

    # for visual debugging
    # print('\n\n', latex_string[0:700], '\n\n')

    with open(f'{filename}.tex', 'w') as f:
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
