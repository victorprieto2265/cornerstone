# -*- coding: utf-8 -*-

# %% import section, docstring

from timeit import default_timer as timer
import sys

docstring = """

A special playoff scheduler created for NSC, which is able to swap teams around
to avoid repeat matches in the afternoon.

CRITICAL: there are hardcoded format codes in this script. They should rely
on the codes imported in df_dict_prelim in cornerstone_input.py instead.

Created on April 25, 2022

@author: Victor Prieto
"""

print(docstring)
start = timer()
start_time = start

# %%  function, list definitions

def teamlist_sorter(teamlist, code):
    """


    Parameters
    ----------
    teamlist : list
        a list of teams, generally in format[name, prelim group, finish, ppb]
    code : list
        a list of integers used to identify indexes of teams for sorting

    Returns
    -------
    newlist : list
        the same list of teams organized by indexes provided to teamlist_sorter

    """
    newlist = []
    for i in code:
        i = i-1  # need to subtract one for zero-indexing
        team = teamlist[int(i)]
        newlist.append(team)
    return newlist

def teamlist_splitter(teamlist, code):
    """


    Parameters
    ----------
    teamlist : list
        a list of teams, generally in format[name, prelim group, finish, ppb]
    code : list
        a list of integers for determining the size of the final groups created
        by the splitter function

    Returns
    -------
    newlist : list
        the same list of teams split into groups, whose sizes are dictated by
        the code provided to teamlist_splitter

    """
    newlist = []
    for index, element in enumerate(code):
        slice1 = sum(code[0:index])
        slice2 = slice1 + element
        newlist.append(teamlist[slice1:slice2])
    return newlist

def check_repeats(alist):
    group_list = [team[1] for team in alist]
    dups = set([x for x in group_list if group_list.count(x) > 1])
    if dups:
        print('*** DUPLICATES DETECTED ***\n', dups)
        sys.exit()

def code_lister(codestring):
    codelist = codestring.split(',')
    return [int(i) for i in codelist]

# sample list of 72 teams for function testing
original_list = [['Team D1', 'Drive', 1, 23.48], ['Team B1', 'Bayou', 1, 22.0], ['Team A1', 'Avenue', 1, 20.16], ['Team C1', 'Circle', 1, 20.0], ['Team E1', 'Expressway', 1, 19.82], ['Team G1', 'Glen', 1, 17.0], ['Team H1', 'Harbor', 1, 16.93], ['Team F1', 'Ford', 1, 16.85], ['Team J1', 'Junction', 1, 15.71], ['Team L1', 'Landing', 1, 15.06], ['Team K1', 'Knoll', 1, 14.79], ['Team I1', 'Inlet', 1, 14.0], ['Team B2', 'Bayou', 2, 22.0], ['Team J2', 'Junction', 2, 21.0], ['Team C2', 'Circle', 2, 19.0], ['Team E2', 'Expressway', 2, 18.67], ['Team H2', 'Harbor', 2, 18.3], ['Team D2', 'Drive', 2, 18.24], ['Team F2', 'Ford', 2, 16.0], ['Team L2', 'Landing', 2, 15.81], ['Team I2', 'Inlet', 2, 15.37], ['Team K2', 'Knoll', 2, 15.11], ['Team A2', 'Avenue', 2, 14.22], ['Team G2', 'Glen', 2, 13.5], ['Team A3', 'Avenue', 3, 20.0], ['Team B3', 'Bayou', 3, 19.43], ['Team D3', 'Drive', 3, 18.2], ['Team C3', 'Circle', 3, 18.0], ['Team E3', 'Expressway', 3, 17.37], ['Team G3', 'Glen', 3, 15.04], ['Team F3', 'Ford', 3, 15.0], ['Team H3', 'Harbor', 3, 14.83], ['Team L3', 'Landing', 3, 13.49], ['Team J3', 'Junction', 3, 13.07], ['Team I3', 'Inlet', 3, 13.0], ['Team K3', 'Knoll', 3, 12.62], ['Team A4', 'Avenue', 4, 19.0], ['Team B4', 'Bayou', 4, 18.1], ['Team E4', 'Expressway', 4, 17.68], ['Team D4', 'Drive', 4, 17.47], ['Team C4', 'Circle', 4, 17.0], ['Team F4', 'Ford', 4, 14.0], ['Team G4', 'Glen', 4, 13.81], ['Team H4', 'Harbor', 4, 13.4], ['Team L4', 'Landing', 4, 13.03], ['Team J4', 'Junction', 4, 12.85], ['Team K4', 'Knoll', 4, 12.6], ['Team I4', 'Inlet', 4, 12.5], ['Team A5', 'Avenue', 5, 18.0], ['Team B5', 'Bayou', 5, 17.84], ['Team C5', 'Circle', 5, 16.0], ['Team G5', 'Glen', 5, 15.93], ['Team H5', 'Harbor', 5, 15.24], ['Team D5', 'Drive', 5, 13.52], ['Team F5', 'Ford', 5, 13.0], ['Team K5', 'Knoll', 5, 12.88], ['Team E5', 'Expressway', 5, 12.84], ['Team J5', 'Junction', 5, 12.55], ['Team L5', 'Landing', 5, 12.24], ['Team I5', 'Inlet', 5, 12.0], ['Team B6', 'Bayou', 6, 17.64], ['Team A6', 'Avenue', 6, 17.0], ['Team E6', 'Expressway', 6, 15.18], ['Team D6', 'Drive', 6, 15.02], ['Team C6', 'Circle', 6, 15.0], ['Team K6', 'Knoll', 6, 12.75], ['Team J6', 'Junction', 6, 12.35], ['Team L6', 'Landing', 6, 12.32], ['Team F6', 'Ford', 6, 12.0], ['Team G6', 'Glen', 6, 11.57], ['Team H6', 'Harbor', 6, 11.5], ['Team I6', 'Inlet', 6, 10.75]]

# %% code block 4: main definition for the playoff seeding function

def playoff_seeding(alist, code1, code2, code3, code4):
    
    # convert codes from strings to lists
    code1 = code_lister(code1)
    code2 = code_lister(code2)
    code3 = code_lister(code3)
    code4 = code_lister(code4)
    
    # split sorted list of teams into tiers
    tiered_list = teamlist_splitter(alist, code1)
        
    swapped_list = []    
    for tier in tiered_list:
        
        # assign top seeds to groups based on code2 and code3 respectively
        sorted_list = teamlist_sorter(tier, code2)

        grouped_teams = teamlist_splitter(sorted_list, code3)

        # remove top seeds from tier before continuing group assignments
        x = int(len(tier)/2)
        tier = tier[x:]
        
        # assign remaining teams in tier to groups, avoiding group repeats
        # code4 determines order of group assignments
        for index, group_index in enumerate(code4):
            group_index -= 1  # subtract 1 from group_index for zero indexing
            group = grouped_teams[group_index]
            team_index = 0
            print('\n***\n')
            print(*tier, sep='\n')
            team = tier[team_index]
            prelim_group = team[1]
            grouplist = [team[1] for team in group]

            # is prelim group of 1st unassigned team in destination group?
            while prelim_group in grouplist:
                # assume "yes" to start, move to next unassigned team
                
                # # visual debugging
                # print(f'testing team: {team[0]} from group {team[1]}.')
                # print(f'is {prelim_group} in {grouplist}?')
                # print('yes, skipping to next team.')
                
                # try to retrieve next unassigned team in list...
                try:
                    team_index += 1
                    team = tier[team_index]
                    prelim_group = team[1]
                    
                # unless there are no more teams in the list, then swaps!
                except IndexError:
                    # print('WARNING: no more teams in list. Execute swaps.')
                    prelim_group_temp = prelim_group
                    count = 0
                    while prelim_group_temp in grouplist:
                        count += 1
                        group_index = code4[index-count]
                        team2 = grouped_teams[group_index][-1]
                        prelim_group_temp = team2[1]
                    #     print(f'Will try swapping with {team2} instead.')
                    # print('This swap is acceptable.')
                    grouped_teams[group_index][-1] = tier[0]
                    tier.pop(0)
                    group.append(team2)
                    break
            
            # if assumption "yes" is wrong, assign team to destination group
            else:
                
                # # visual debugging
                # print(f'testing team: {team[0]} from group {team[1]}.')
                # print(f'is {prelim_group} in {grouplist}?')
                # print('no, team will be placed in group.\n')
                
                group.append(team)
                tier.pop(team_index)  # removal from list of unassigned teams
        
        # checks for repeats, if they exists, halts the program
        for i in grouped_teams:
            check_repeats(i)
        
        swapped_list.append(grouped_teams)
        
    # last line flattens the list from tiers into just a list of groups
    return [item for sublist in swapped_list for item in sublist]

# %% execution of nsc_swaps function
# this is the part that goes into the playoff rebracketing script

# from nsc_scheduler import playoff_seeding

# TODO THESE ARE HARD CODED, VERY BAD

code1 = '24,24,24'
code2 = '1,8,9,2,7,10,3,6,11,4,5,12'
code3 = '3,3,3,3'
code4 = '4,3,2,1,1,2,3,4,4,3,2,1'

# swapped_list = playoff_seeding(original_list, code1, code2, code3, code4)

# # visual debugging
# for i in swapped_list:
#     print('\n')
#     print(*i, sep='\n\n')
#     [check_repeats(j) for j in i]
# print('\nno repeats detected.\n')

# %% archive of code block 4 with lots of visual debugging

# code2 = '24,24,24'
# tiered_list = code_2_scheduler(original_list, code2)

# code1 = '1,8,9,2,7,10,3,6,11,4,5,12'
# code2 = '3,3,3,3'
# code3 = '1,2,3,4,4,3,2,1,1,2,3,4'
# code3 = '4,3,2,1,1,2,3,4,4,3,2,1'
# code3 = code3.split(',')
# code3 = [int(i)-1 for i in code3]

# swapped_list = []

# for tier in tiered_list[0:2]:
#     print(*tier[:12], sep='\n')
#     sorted_list = code_1_scheduler(tier, code1)
#     grouped_teams = code_2_scheduler(sorted_list, code2)
#     print('\n')
#     print(*grouped_teams, sep='\n')
#     print('\n')
#     tier = tier[12:]
#     print(*tier, sep='\n')
#     print('\npoint 3\n')

#     for index, group_index in enumerate(code3):
#         group = grouped_teams[group_index]
#         team_index = 0
#         team = tier[team_index]
#         prelim_group = team[1]
#         grouplist = [team[1] for team in group]
#         print(f'\nattempting to place team in group:\n{group}')
#         while prelim_group in grouplist:
#             print(f'testing team: {team[0]} from group {team[1]}.')
#             print(f'is {prelim_group} in {grouplist}?')
#             print('yes, skipping to next team.')
#             try:
#                 team_index += 1
#                 team = tier[team_index]
#                 prelim_group = team[1]
#             except IndexError:
#                 print('WARNING: no more teams in list. Execute swaps.')
#                 prelim_group_temp = prelim_group
#                 count = 0
#                 while prelim_group_temp in grouplist:
#                     count += 1
#                     group_index = code3[index-count]
#                     team2 = grouped_teams[group_index][-1]
#                     prelim_group_temp = team2[1]
#                     print(f'Will try swapping with {team2} instead.')
#                 print('This swap is acceptable.')
#                 grouped_teams[group_index][-1] = tier[0]
#                 tier.pop(0)
#                 group.append(team2)
#                 break
#         else:
#             print(f'testing team: {team[0]} from group {team[1]}.')
#             print(f'is {prelim_group} in {grouplist}?')
#             print('no, team will be placed in group.')
#             group.append(team)
#             tier.pop(team_index)

#     for i in grouped_teams:
#         print('\n')
#         print(*i, sep='\n')
#         print(f'number of teams in group = {len(i)}')
#         check_repeats(i)
#     swapped_list.append(grouped_teams)
#     break



#     print('\n\n***\n\n')


# for i in swapped_list:
#     print(*i, sep='\n\n')
#     [check_repeats(j) for j in i]



# %% end of script, runtime

print('---end of script---')
runtime = 1000 * (timer() - start_time)
if runtime > 1000:
    runtime = runtime/1000
    print('runtime : %.1f s' % runtime)
elif runtime > 1000:
    runtime = runtime/60
    print('runtime : %.1f min' % runtime)
else:
    print('runtime : %.1f ms' % runtime)
