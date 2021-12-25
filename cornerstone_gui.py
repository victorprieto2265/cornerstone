#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% import modules/functions, header
import time
from tkinter import (Tk, StringVar, Label, Entry,
                     Listbox, Scrollbar, Button)
import sys

from tournament_format import tournament_date

header = """

Created on Wed Dec 22 13:50:27 2021

Creates the GUI interface for cornerstone.

@author: Victor Prieto

"""

# %% start runtime
start_time = time.time()
print('\n', header)
print('start time: %s' % time.ctime())

# %% function definitions


def add_team():
    print('Team added.')


def remove_team():
    print('Team removed.')


# %% create window object
app = Tk()

app.title('Cornerstone')

# set dimensions of window
width = 1200
height = 500

# look up screen width and height
sw = app.winfo_screenwidth()  # screenwidth
sh = app.winfo_screenheight()  # screenheight

# calculate x and y coordinates for Tk window
x = (sw/2) - (width/2)
y = (sh/2) - (height/2)

# set location of window based on screen dimensions
app.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

# %% Tournament Information

name_text = StringVar()
name_label = Label(app, text='Tournament Name', font=('bold', 14), pady=20)
name_label.grid(row=0, column=0, sticky='W')
name_entry = Entry(app, textvariable=name_text)
name_entry.grid(row=0, column=1)

date_text = StringVar()
date_label = Label(app, text='Tournament Date', font=('bold', 14))
date_label.grid(row=0, column=2, sticky='W')
date_entry = Entry(app, textvariable=date_text)
date_entry.grid(row=0, column=3)

location_text = StringVar()
location_label = Label(app, text='Tournament Location', font=('bold', 14))
location_label.grid(row=0, column=4, sticky='W')
location_entry = Entry(app, textvariable=location_text)
location_entry.grid(row=0, column=5)

# Team List (Listbox)
team_list = Listbox(app, height=8, width=50)
team_list.grid(row=2, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# create scrollbar for Team List
scrollbar = Scrollbar(app)
scrollbar.grid(row=2, column=3)
team_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=team_list.yview)

# add some test buttons, don't have a clear vision for window layout yet
add_btn = Button(app, text='Add Team', width=12, command=add_team,
                 bg='blue')
add_btn.grid(row=1, column=0, pady=20)

remove_btn = Button(app, text='Remove Team', width=12, command=remove_team,
                    bg='red')
remove_btn.grid(row=1, column=1, pady=20)

# start program
print('\n*** main window open ***\n')
app.mainloop()

# close program
sys.exit()


# %% end runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
