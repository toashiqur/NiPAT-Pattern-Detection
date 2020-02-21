__author__ = 'ASR'

import os
import shutil
import time


def create(source_input_directory, user_choice):
    # Create input directory to store grm/txl/jm files
    try:
        if os.path.exists(source_input_directory):        # Does the directory Exist?
            print("Cleaning existing directory...", source_input_directory)
            shutil.rmtree(source_input_directory)
            time.sleep(2)   # Delay to allow time for removing directory otherwise create directory may fail.

        os.makedirs(source_input_directory)    # Create the directory

        if user_choice == "grm":
            print("Grammar file will be stored in: ", source_input_directory)
        elif user_choice == "txl":
            print("TXL file will be stored in: ", source_input_directory)
        else:
            print("JM file will be stored in: ", source_input_directory)

    except OSError:
        print("Error in creating Result Directory...Exiting..(create_directory.py")
        exit(1)


def main(source_input_directory, user_choice):
    create(source_input_directory, user_choice)


'''
# unblock for testing
create("G:\my", "3")
'''