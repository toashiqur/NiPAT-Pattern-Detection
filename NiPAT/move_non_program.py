__author__ = 'ASR'
import os
import shutil


def create_non_program_directory(move_to):
    # Create Result directory
    try:
        if os.path.exists(move_to):        # Does the directory Exist?
            shutil.rmtree(move_to)         # Then remove the previous directory
        os.makedirs(move_to)               # Always create a fresh directory
        # print("Creating directory:", move_to, "to move non_program jm files.")
    except OSError:
        print("Error in creating directory:", move_to, "for holding non program JM files...Exiting")
        exit(1)


def main(source_input_directory, non_program_jm_directory):
    non_program_src = []   # Empty list to hold the files without main
    str1 = "rule main"
    str2 = "function main"
    total_jm_file = 0
    total_prgrm_move_error = 0

    non_program_summary_file = open(non_program_jm_directory + "_Summary.txt", 'w')   # its a technique-- when adding extension and creating a file it consider the last portion of the path as the file name and creates
    print("---- Summary Report on Non-Program JM files ----\n", file=non_program_summary_file)

    for dir_contents in os.listdir(source_input_directory):
        if dir_contents.endswith(".jm"):                  # ensure that its a jm file not a folder
            total_jm_file += 1
            is_txl_program = False                                 # Assume this file is a non-program
            file_path = os.path.join(source_input_directory, dir_contents)     # generate file path
            file_content = open(file_path)
            for line in file_content:
                if str1 in line or str2 in line:
                    is_txl_program = True
                    # print(file_path, "is a txl main program.")
                    break

            file_content.close()    # Close the file
            if not is_txl_program:
                non_program_src.extend([file_path])                # Add file to list for removing
                print(file_path, "<NonProgramTxl>")
                print(file_path, "<NonProgramTxl>", file=non_program_summary_file)

    if len(non_program_src) > 0:   # Do the move if non-program file exists
        create_non_program_directory(non_program_jm_directory)       # Create Directory for moving files
        for src in non_program_src:
            try:
                shutil.move(src, non_program_jm_directory)
            except shutil.Error as shutil_error:
                total_prgrm_move_error += 1
                print("Error in moving non-program jm file", src, "->", non_program_jm_directory, "using shutil.move:", type(shutil_error).__name__)
        if total_prgrm_move_error == 0:
            print("All non Program JM files have been moved successfully to:", non_program_jm_directory)
            print("\nAll non Program JM files have been moved successfully to:", non_program_jm_directory, file=non_program_summary_file)
        else:
            print("\nNon Program JM files have been moved to:", non_program_jm_directory, "Move Error:", total_prgrm_move_error)
    else:
        print("No non-program found")
        print("No non-program found", file=non_program_summary_file)

    print("Total JM files found: ", total_jm_file, "\nTotal Non-Program JM files found: ", len(non_program_src), "\nUnknown Move Error: ", total_prgrm_move_error)
    print("Total JM files found: ", total_jm_file, "\nTotal Non-Program JM files found: ", len(non_program_src), "\nUnknown Move Error: ", total_prgrm_move_error, file=non_program_summary_file)

    non_program_summary_file.close()




# Unblock to test individually
# jm_result_directory = "F:/jmfile"
# move_non_program_jm_main(jm_result_directory)
