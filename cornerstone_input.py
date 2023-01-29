#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sys
import pandas as pd

from pylatex import NoEscape

header = """

This script imports all of the input files, except tournament format,
which is handled by the tournament_format script.

TODO uncomment sys.exit at end of this script for testing
TODO figure out how to handle blank spaces and/or none in input file...
There was an unusual error where integers were being converted to floats
if one of the cells in a range was empty instead of string 'none'.
TODO apparently bracket names (and presumably other things) are case-sensitive.

@author: Victor Prieto

"""


# starts program runtime
start_time = time.time()
print('\n', header)
print('start time: %s Eastern Time\n' % time.ctime())

# TODO there must be a better way to do this
error = 0

# %% function definitions


# checks for duplicates and (optional) character limits
def error_check(alist, listname, max_length=float('inf'), max_duplicates=1):
    global error  # TODO this is apparently a no no, but works for now
    print('\n')
    # duplicate checker
    seen = {}
    duplicates = []
    for item in alist:
        if item not in seen:
            seen[item] = 1
        else:
            seen[item] += 1
            if seen[item] > max_duplicates:
                duplicates.append(' - ' + item)
    if not duplicates:
        if max_duplicates > 1:
            print(f'No excess duplicates detected for {listname}.')
        else:
            print(f'No duplicates detected for {listname}.')
    else:
        # error = True
        error += 1
        print(f'\nDuplicates detected for {listname}:')
        print(*duplicates, sep='\n')

    # character length checker
    long_items = [' - ' + item for item in alist if len(item) > max_length]
    if not long_items:
        print(f'No character lengths exceeded for {listname}.')
    else:
        error += 1
        # error = True
        print(f'Character lengths exceeded for {listname}:')
        print(*long_items, sep='\n')


def old_analyze_input(filename, list_index=None):
    df = pd.read_excel(f'{filename}.xlsx')
    temp_list = df.values.tolist()  # note: temp_list may be multiple lists!
    return temp_list


def analyze_input(sheet_name, df_dict):
    df = df_dict[sheet_name]
    temp_list = df.values.tolist()  # note: temp_list may be multiple lists!
    return temp_list


# %% new excel import section

# step 0 = identify which excel files to pull? (not implemented while testing)
print('\n***\nAre you uploading excel sheets for prelim schedule creation'
      + ' or rebracketing for playoffs?')
# tournament_phase = input('   enter "prelims" or "playoffs" => ')
tournament_phase = 'playoffs'

while tournament_phase not in ['prelims', 'playoffs', 'super']:
    print('\n***incorrect input provided, please retry***')
    print('\nSelect either prelim schedule creation or '
          + 'rebracketing for playoffs:')
    tournament_phase = input('   enter "prelims" or "playoffs" => ')

# step 1 = import excel file
data_input_location = f'./data input/{tournament_phase}_data.xlsx'
# # TODO Tkinter file select is commented below
# from tkinter import filedialog
# data_input_location = filedialog.askopenfilename()

try:
    sheet_names = ['tournament format', 'list of teams', 'team codes',
                   'group names', 'room assignments',
                   'QR codes', 'text input']
    df_dict_prelim = pd.read_excel(data_input_location,
                                   sheet_name=sheet_names)
    list_of_teams = analyze_input('list of teams', df_dict_prelim)
    team_codes = analyze_input('team codes', df_dict_prelim)
    room_assignments = analyze_input('room assignments', df_dict_prelim)
    qr_codelist = analyze_input('QR codes', df_dict_prelim)
    textlist = analyze_input('text input', df_dict_prelim)
    tournament_format = analyze_input('tournament format', df_dict_prelim)

except FileNotFoundError:
    print('\nNo file found!')

    sys.exit()

# if tournament_phase == 'prelims':
#     prelim_group_names = analyze_input('group names', df_dict_prelim)
# elif tournament_phase == 'playoffs':
#     rows = analyze_input('group names', df_dict_prelim)
#     prelim_group_names = [row[0] for row in rows]
#     playoff_bracket_names = [row[1] for row in rows]
#     playoff_bracket_names = [x for x in playoff_bracket_names
#                              if str(x) != 'nan']
# elif tournament_phase == 'super':
#     pass

group_names = analyze_input('group names', df_dict_prelim)
prelim_group_names = [row[0] for row in group_names]
if tournament_phase in ['playoffs', 'super']:
    playoff_bracket_names = [row[1] for row in group_names]
    playoff_bracket_names = [x for x in playoff_bracket_names
                             if str(x) != 'nan']
if tournament_phase == 'super':
    super_bracket_names = [row[2] for row in group_names]
    super_bracket_names = [x for x in super_bracket_names
                             if str(x) != 'nan']

format_dict = {}
for row in tournament_format:
    key = row[0]  # item, e.g. "tournament name"
    value = row[1]  # input, e.g. "2022 NSC"
    format_dict[key] = value

# convert Excel datetime format to more suitable date string
date = format_dict['tournament date'].strftime('%B %d, %Y')
format_dict['tournament date'] = date

# %% text and qr input section

if format_dict['QR codes'] == 'Y':
    qr_toggle = True

    qr_names = [code[0] for code in qr_codelist]
    qr_codes = [NoEscape(' \\qrcode[height=1in]{' + code[2] + '} ')
                for code in qr_codelist]
    qr_captions = [code[3] for code in qr_codelist]

else:
    qr_toggle = False
    qr_codes = False
    qr_captions = False

if format_dict['text'] == 'Y':
    text_toggle = True
    texts = [text[1] for text in textlist]

    # lorem text, delete later
    lorem = '''

    Lorem ipsum dolor sit amet. Sed iusto reprehenderit ut quis voluptas ea Quis assumenda ut eius magni eum voluptate modi? Id unde libero ad pariatur sunt eos nisi possimus est omnis nisi ut internos laboriosam. Sit nesciunt ducimus et totam maxime est voluptas vero sed itaque nihil. Et expedita culpa et fuga sunt quo esse ipsam eos doloribus autem rem perferendis modi et molestiae vitae.

    Sed cumque odio eum temporibus deleniti ad consequatur consequatur aut molestias maiores. Est doloribus tenetur est dolorem ducimus sit quasi provident. Est facere expedita non expedita molestiae non error magnam vel obcaecati debitis et blanditiis reiciendis est cupiditate voluptatem ea soluta consequatur. Qui tempore ipsam eos asperiores aliquid ex unde velit est repellendus temporibus hic quidem assumenda!

    Non autem maiores aut reprehenderit nulla sit repellendus dolore ut illum incidunt ut dignissimos eaque! Ex aperiam minima eos quis dolor id consequatur eligendi ut culpa galisum. Non fugiat corporis vel doloremque dignissimos sit vero quasi sed voluptatem explicabo.

    '''
else:
    text_toggle = False
    texts = False

# %% error catching

# TODO modify max_duplicates to be flexible on schedule and not hard coded
# or perhaps get rid of max duplicates since it doesn't make a lot of sense
# error check imported lists/sublists
error_check([sublist[0] for sublist in list_of_teams],
            'the team names in list_of_teams',
            max_length=26)

# error_check([sublist[2] for sublist in list_of_teams],
#             'the prelim groups in list_of_teams',
#             max_length=15,
#             )

error_check([sublist[1] for sublist in team_codes],
            'the team codes in team_codes',
            max_length=4)

try:
    error_check(prelim_group_names,
                'the groups in prelim_group_names',
                max_length=15)
except:  # TODO bare except
    None

try:
    error_check(playoff_bracket_names,
                'the brackets in playoff_bracket_names',
                max_length=15)
except:  # TODO bare except
    None

error_check([sublist[0] for sublist in room_assignments],
            'the list of rooms in room_assignments',
            max_length=15)


# %% dictionary creation

# key is team name
# value is team code
# also created a dictionary where the key/value pairs are swapped
team_code_dict = {}
code_team_dict = {}
for row in team_codes:
    team_name = row[0]
    team_code = row[1]
    team_code_dict[team_name] = team_code
    code_team_dict[team_code] = team_name

# key is prelim group and a number (i.e. Accra1)
# value is corresponding room (i.e. Grand Ballroom A is Accra1)
# also created dictionary where key is a playoff bracket instead
prelim_room_dict = {}
playoff_room_dict = {}
super_room_dict = {}
for i in room_assignments:
    key = i[1] + str(i[2])
    value = i[0]
    if tournament_phase == 'prelims':
        prelim_room_dict[key] = value
    elif tournament_phase == 'playoffs':
        playoff_room_dict[key] = value
    elif tournament_phase == 'super':
        super_room_dict[key] = value

# %% error catching

# TODO eventually shunt this over to the round robin schedule script
# prelim_team_count = 6
# halts program if schedule requires RR other than 4, 6, or 8
# if prelim_team_count <= 3 or playoff_team_count <= 3:
#     print('Unable to produce round robins smaller than 4.')
#     sys.exit()

# if prelim_team_count >= 15 or playoff_team_count >= 15:
#     print('Unable to produce round robins larger than 14.')
#     sys.exit()


# pause = input('\n\nVerify no errors occurred. Press enter to continue.\n\n')

if error == 0:
    print('\nNo errors detected upon import.')
else:
    print('\n*** Errors detected during import! ***')
    # sys.exit()
