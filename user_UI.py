# -*- coding: utf-8 -*-

import time
import tkinter as tk
from tkinter import(Tk, ttk, StringVar, Label, Entry,
                    Listbox, Scrollbar, Button, filedialog)
import sys
import shutil
import os.path

docstring = """
Created on Thu Feb 10 10:49:45 2022

@author: Victor Prieto
"""

# %% start runtime
print(docstring)
print(time.ctime)
start_time = time.time()

# %% testing section 3

# print('\n***\nAre you creating a prelim schedule or rebracketing for playoffs?\n')
# program_status = input('   enter "prelims" or "playoffs" => ')

# while program_status not in ['prelims', 'playoffs']:
#     print('\n***incorrect input provided, please retry***')
#     print('Select either prelim schedule creation or rebracketing for playoffs:\n')
#     program_status = input('   enter "prelims" or "playoffs" => ')

# %% possible tournament formats (hard coded for now)

input_dict = {}

input_dict['4'] = ('\nOption A: triple round-robin (9 rounds, 9 games, 2 rooms)\n'                   + 'Option B: quadruple round-robin (12 rounds, 12 games, 2 rooms)')
input_dict['9'] = ('\nOption A: full round-robin (9 rounds, 8 games minimum, 4 rooms)\n'
                   + 'Option B: round-robin into top3/middle 3/bottom 3 split (12 rounds, 10 games minimum, 4 rooms)\n'
                   + 'Option C: round-robin into top 5/bottom 4 split (14 rounds, 11 games minimum, 4 rooms)')

input_dict['12'] = ('\nOption A: two prelim groups of 6 into two playoff brackets of 6, no repeat matches (8 rounds, 8 games, 6 rooms)\n'
                   + 'Option B: two prelim groups of 6 into two playoff brackets of 6, repeat matches (10 rounds, 10 games, 6 rooms)\n'
                   + 'Option C: full round-robin (11 rounds, 11 games, 6 room)s\n'
                   + 'Option D: full round-robin with byes (12 rounds)')

input_dict['24'] = ('\nOption A: four prelim groups of 6 into six playoff brackets of 4, with two parallel top brackets (8 rounds, 8 games, 12 rooms)\n'
                   + 'Option B: three prelim groups of 8 into four playoff brackets of 6 (11 rounds, 11 games, 12 rooms)\n'
                   + 'Option C: four prelim groups of 6 into three playoff brackets of 8 (11 rounds, 11 games, 12 rooms)\n'
                   + 'Option D: three prelim groups of 8 with byes into four playoff brackets of 6 (12 rounds, 11+ games, 12 rooms'
                   + 'Option E: 6 by 5 into 6 by 5')  # TODO update this

input_dict['25'] = ('one option', '\nFive prelim groups of 5 into five playoff groups of 5, with two parallel top brackets of 5 (10 rounds, 8 games, 10 rooms)\n')
input_dict['26'] = ('one option', '\n Four prelim groups of 5 and one prelim group of 6 into four playoff brackets of 5 and one playoff bracket of 6, with two parallel top brackets (10 rounds, 8+ games, 11 prelim rooms, 11 playoff rooms)')
input_dict['27'] = ('one option', '\nTwo prelim groups of 6 and three prelim groups of 5 into two playoff brackets of 6 and three playoff brackets of 5, with two parallel top brackets (10 rounds, 8+ games, 12 rooms)')
input_dict['28'] = ('one option', '\nFour prelim groups of 7 into seven playoff brackets of 4, with two parallel top brackets (10 rounds, 9+ games, 12 prelim rooms, 14 playoff rooms)')
input_dict['29'] = ('one option', '\nFour prelim groups of 6 and one prelim group of 5 into four playoff brackets of 6 and one playoff bracket of 5, with two parallel top brackets (10 rounds, 9+ games, 14 rooms)')

input_dict['30'] = ('one option', '\nFive prelim groups of 6 into five playoff brackets of 6, with two parallel top brackets (10 rounds, 10 games, 15 rooms)')
input_dict['31'] = ('one option', '\nThree prelim groups of 8 and one prelim group of 7 into two parallel top brackets of 4, two parallel middle brackets of 4, and 3 lower brackets of 5 (12 rounds, 10+ games, 15 prelim rooms, 14 playoff rooms\n')
input_dict['32'] = ('one option', '\nFour prelim groups of 8 into eight playoff brackets of 4, with two parallel top brackets (10 rounds, 10 games, 16 rooms)')
input_dict['33'] = ('one option', '\nThree prelim groups of 6 and three prelim groups of 5 into three playoff groups of 6 and three playoff groups of 5, with two parallel top brackets of 6 (10 rounds, 8+ games, 15 rooms)\n')
input_dict['34'] = ('one option', '\nFour prelim groups of 6 and two prelim groups of 5 into four playoff groups of 6 and two playoff groups of 5, with two parallel top brackets of 6 (10 rounds, 8+ games, 16 rooms)\n')
input_dict['35'] = ('one option', '\nFive prelim groups of 6 and one prelim groups of 5 into five playoff groups of 6 and one playoff groups of 5, with two parallel top brackets of 6 (10 rounds, 8+ games, 17 rooms)\n')

input_dict['36'] = ('one option', '\nSix prelim groups of 6 into six playoff groups of 6, with two parallel top brackets of 6 (10 rounds, 10 games, 18 rooms)\n')

# %% schedule format logic

print('\n***\nHow many teams are competing in the tournament?\n')
team_count = input('   enter number of teams (digits only) => ')
while team_count.isnumeric() == False:
    print('\n***a non numerical input was provided, please retry***')
    team_count = input('   enter number of teams (digits only) => ')
    

if input_dict[team_count][0] == 'one option':
    print(f'\n***\nWith {team_count} teams, there is only one possible format:')
    print(input_dict[team_count][1])
    input("Press enter to continue.")
    tournament_format = team_count
else:
    print('\n***\nEnter one of the following options below:')
    print(input_dict[team_count])
    tournament_format = team_count + input('   enter single capital letter => ')

for phase in ['prelims', 'playoffs']:
    source = f'./inputs/master_templates/{tournament_format}_{phase}.xlsx'
    destination = f'./data input/{phase}_data.xlsx'
    if os.path.exists(destination) is True:
        print('\n***\nWarning! File exists already. Do you wish to overwrite?')
        exit_status = input('   enter "Y" to overwrite, or press enter to exit => ')
        if exit_status not in ['Y', 'y']:
            print('\n***\n\nExiting script...\n')
        else:
            print('\n***\n\nOverwriting existing file...\n')
            shutil.copyfile(source, destination)
    else:
        shutil.copyfile(source, destination)

# %% end runtime

print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
