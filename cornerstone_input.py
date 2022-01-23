#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, sys
import pandas as pd

from tournament_format import prelim_team_count, playoff_team_count
from function_definitions import duplicate_checker
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
    global error  # TODO this is apparently a no no, but works for nwo
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



def analyze_input(filename, list_index=None):
    df = pd.read_excel(f'{filename}.xlsx')
    temp_list = df.values.tolist()  # note: temp_list may be multiple lists!
    return temp_list


# %% excel import section, error catching

# file locations
list_of_teams = "./inputs/list_of_teams"
prelim_group_names = "./inputs/prelim_group_names"
room_assignments = "./inputs/room_assignments"
prelim_results = "./inputs/prelim_results"
playoff_bracket_names = "./inputs/playoff_bracket_names"
super_input = "./inputs/super_input"
qr_input = "./inputs/qr_input"

# TODO write separate script that reads above lists + identifies rr schedules
# will need to import list of teams and generate prelim_round_count
rr_schedule = f"./rr_schedules/rr_{prelim_team_count}"
playoff_rr_schedule_input = f"./rr_schedules/rr_{playoff_team_count}"
df3 = pd.read_excel(f'{rr_schedule}.xlsx')
df6 = pd.read_excel(f'{playoff_bracket_names}.xlsx')

# TODO modify max_duplicates to be flexible on schedule and not hard coded
# import files using above file locations, error check imported lists/sublists
list_of_teams = analyze_input(list_of_teams)
error_check([sublist[0] for sublist in list_of_teams],
            'the team names in list_of_teams',
            max_length=26)
error_check([sublist[1] for sublist in list_of_teams],
            'the team codes in list_of_teams',
            max_length=4)
error_check([sublist[2] for sublist in list_of_teams],
            'the prelim groups in list_of_teams',
            max_length=15,
            max_duplicates=8)

prelim_group_names = analyze_input(prelim_group_names)
prelim_group_names = [' '.join(strings) for strings in prelim_group_names]
error_check(prelim_group_names,
            'the groups in prelim_group_names',
            max_length=12)

room_assignments = analyze_input(room_assignments)
error_check([sublist[0] for sublist in room_assignments],
            'the list of rooms in room_assignments',
            max_length=14)

# script does not require playoff or super information to be present
try:
    prelim_results = analyze_input(prelim_results)
    error_check([sublist[0] for sublist in prelim_results],
                'the team names in prelim_results',
                max_length=26)
    error_check([sublist[1] for sublist in prelim_results],
                'the brackets in prelim_results',
                max_length=12,
                max_duplicates=8)

    playoff_brackets = analyze_input(playoff_bracket_names)
    # converts list of lists to list of strings
    playoff_bracket_names = [' '.join(strings) for strings in playoff_brackets]

    super_input = analyze_input(super_input)
    error_check([sublist[0] for sublist in super_input],
                'the team names in super_input',
                max_length=26)
    error_check([sublist[1] for sublist in super_input],
                'the team codes in super_input',
                max_length=4)
    error_check([sublist[2] for sublist in super_input],
                'the playoff brackets in super_input',
                max_length=15,
                max_duplicates=6)

    qr_codelist = analyze_input(qr_input)
    qr_names = [code[0] for code in qr_codelist]
    qr_codes = [NoEscape(' \\qrcode[height=1in]{' + code[1] + '} ')
                for code in qr_codelist]
    qr_captions = [code[2] for code in qr_codelist]


except FileNotFoundError:
    pass


# alphabetizes list of teams
list_of_teams.sort(key=lambda x: x[0])

# %% text input section

# lorem text, delete later
lorem = '''

Lorem ipsum dolor sit amet. Sed iusto reprehenderit ut quis voluptas ea Quis assumenda ut eius magni eum voluptate modi? Id unde libero ad pariatur sunt eos nisi possimus est omnis nisi ut internos laboriosam. Sit nesciunt ducimus et totam maxime est voluptas vero sed itaque nihil. Et expedita culpa et fuga sunt quo esse ipsam eos doloribus autem rem perferendis modi et molestiae vitae.

Sed cumque odio eum temporibus deleniti ad consequatur consequatur aut molestias maiores. Est doloribus tenetur est dolorem ducimus sit quasi provident. Est facere expedita non expedita molestiae non error magnam vel obcaecati debitis et blanditiis reiciendis est cupiditate voluptatem ea soluta consequatur. Qui tempore ipsam eos asperiores aliquid ex unde velit est repellendus temporibus hic quidem assumenda!

Non autem maiores aut reprehenderit nulla sit repellendus dolore ut illum incidunt ut dignissimos eaque! Ex aperiam minima eos quis dolor id consequatur eligendi ut culpa galisum. Non fugiat corporis vel doloremque dignissimos sit vero quasi sed voluptatem explicabo.

'''

# %% dictionary creation

# key is a prelim group name and a seed (i.e. Belmopan6)
# value is the corresponding team (i.e. Great Valley A for Belmopan6)
# also created a dictionary where values are team codes (i.e. GVA)
prelim_team_dict = {}
prelim_teamcode_dict = {}
team_group_dict = {}
teamcode_group_dict = {}
for i in list_of_teams:
    key = i[2] + str(i[3])
    value = i[0]  # team name
    prelim_team_dict[key] = value
    # also created dictionary where k/v pairs are swapped
    team_group_dict[value] = key

    value = i[1]  # team code
    prelim_teamcode_dict[key] = value
    # also created dictionary where k/v pairs are swapped
    teamcode_group_dict[value] = key

# key is team name
# value is team code
# also created a dictionary where the key/value pairs are swapped
team_code_dict = {}
code_team_dict = {}
for team in list_of_teams:
    team_name = team[0]
    team_code = team[1]
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
    prelim_room_dict[key] = value
    key = i[3] + str(i[4])
    playoff_room_dict[key] = value
    try:
        key = i[5] + str(i[6])
        super_room_dict[key] = value
    except IndexError:
        continue

# %% error catching

# TODO eventually shunt this over to the round robin schedule script
prelim_team_count = 6
# halts program if schedule requires RR other than 4, 6, or 8
if prelim_team_count <= 3 or playoff_team_count <= 3:
    print('Unable to produce round robins smaller than 4.')
    sys.exit()

if prelim_team_count >= 15 or playoff_team_count >= 15:
    print('Unable to produce round robins larger than 14.')
    sys.exit()

if error == 0:
    print('\nNo errors detected upon import.')
else:
    print('\n*** Errors detected during import! ***')
    # sys.exit()

# TODO the above, which will cut down the number of input files by two
'''

Not sure what the above comment means, but I'm guessing it has something to
do with reading the lists of teams, offering users a choice of tournament
formats, and providing a bunch of variables to the rest of the program.

'''

# prints runtime
print('\n\n')
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
