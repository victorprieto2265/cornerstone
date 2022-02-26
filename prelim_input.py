#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% import modules/functions, header
import time
# place additional modules here

header = """

Created on Sat Feb 19 10:58:19 2022

@author: Victor Prieto

"""


# %% start runtime
start_time = time.time()
print('\n', header)
print('start time: %s' % time.ctime())

# %% insert code below




# %% end runtime
print('end time: %s' % time.ctime())
print("--- %s seconds ---" % '%.3f' % (time.time() - start_time))
print("--- %s minutes ---" % '%.3f' % (time.time()/60 - start_time/60))
