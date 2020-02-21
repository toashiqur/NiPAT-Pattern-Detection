__author__ = 'ASR'

import os
import subprocess
import time

def find_clones_main(cygwin_terminal_path):
    '''
    This cmd string was taken from the Cygwin icon's properties that appears on the desktop; icon information has been truncated... otherwise the system will not find
    txl directory. Last '-' at the end will keep the cygwin terminal path ok...'''

    # cygwin_terminal_path = ["C:/cygwin64/bin/mintty.exe", "-"]
    start_time_nicad = time.time()
    invoke_cygwin_terminal = subprocess.call(cygwin_terminal_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    end_time_nicad = time.time()
    # invoke_cygwin_terminal = subprocess.Popen(cygwin_terminal_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print("NiCAD time(including user command):", end_time_nicad-start_time_nicad, "s.")

'''
# start find_clones_main- unblock for individual test
cygwin_terminal_path = ["C:/cygwin64/bin/mintty.exe", "-"]
find_clones_main(cygwin_terminal_path)
'''