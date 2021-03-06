__author__ = 'ASR'

'''
input: path to the folder containing grm and txl files
        path to the txl.exe folder
process: Finds out txl files in the given directory then finds out related Grm files and merge them.
output: Generates .jm files for each of the txl files in the given directory.
external process dependency: It uses the merge.txl external file for merging.
'''

import os
import shutil
import subprocess


def start_txl_merge(txl_exe_path, txl_merge_program_path, input_file_path, output_file_path, include_path):
    '''
    txl_exe_path = holds the path of txl.exe
    txl_merge_program_path = holds the path of the txl program which will merge Rules and Grammar
    input_file_path = holds the name of the .txl file which will be processed
    output_file_path = holds the path of the output file which will be used to create the .jm file containing the merged input
    include_path = holds the path where the include file will be searched.
    '''

    # Execution of external process
    # cmd = ["C:/Users/ASR/Desktop/Txl106a7_32/bin/txl.exe", "-o", output_file_path, input_file_path, "C:/Users/ASR/Desktop/Txl106a7_32/bin/merge.txl", "-", "-path", include_path]

    cmd = [txl_exe_path, "-o", output_file_path, input_file_path, txl_merge_program_path, "-", "-path", include_path]
    process = subprocess.call(cmd, stdout=subprocess.PIPE)      # It returns after completion

    # process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    # process = subprocess.Popen(cmd) # it works silently.

    '''
    # It gives all the output generated by the subprocess...
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = ""
    for line in process.stdout:
        output += line.decode('utf8')
    print(output)
    '''


def walk_in_directory_and_merge(source_program_directory, source_input_store_directory, txl_exe_path, txl_merge_program_path, user_choice, extension):
    # current_root holds the current directory name
    # all_dirs holds the directory name under the current_root
    # all_files holds the name of all files in the current directory
    # Reading directory files

    count_file = 0  # Count the number of successful operation
    count_copy_success = 0
    count_same_file = 0  # Count the number of failed operation
    unknown_error = 0


    # Set the extension to search for based on user_choice
    if user_choice == "grm":
        if len(extension) == 0:  # No user choice: load default extension
            extension = (".grm", ".grammar", ".igrm", ".delg", ".txl", ".irul", ".rul", ".rule", ".i", ".module")
        new_extension = ".grm"  # new_extension will be used to rename retrieved/merged file consistently
        summary_file = open(source_input_store_directory + "_Retrieval_Summary.txt", 'w')   # its a technique-- when adding extension and creating a file it consider the last portion of the path as the file name and creates
        print("---- Summary Report on TXL Grammar File Retrieval----\nGrammar Extension searched for:", extension, "\n\nRetrieved File Stored in: ", source_input_store_directory, " <-- Original Source File Path", file=summary_file)
    elif user_choice == "txl":
        if len(extension) == 0:
            extension = (".txl", ".irul", ".rul", ".rule", ".i", ".module")
        new_extension = ".txl"
        summary_file = open(source_input_store_directory + "_Retrieval_Summary.txt", 'w')
        print("---- Summary Report on TXL Rule File Retrieval----\nTXL Rule Extension searched for:", extension, "\n\nRetrieved File Stored in: ", source_input_store_directory, " <-- Original Source File Path", file=summary_file)
    else:  # user_choice is jm
        if len(extension) == 0:
            extension = ".txl"
        new_extension = ".jm"
        summary_file = open(source_input_store_directory + "_Merge_Summary.txt", 'w')
        print("---- Summary Report on TXL Grammar+Rule Merge----\n Grammar Extension searched for:", extension, "\n\nMerged File Stored in: ", source_input_store_directory, " <-- Original Source File Path", file=summary_file)

    for current_root_name, all_dir_names, all_files_name in os.walk(source_program_directory):
        for file_name in all_files_name:
            if file_name.lower().endswith(extension):           # Match the extension after converting it to lowercase
                count_file += 1
                # print(os.path.join(current_root_name, file_name))
                input_file_path = os.path.join(current_root_name, file_name)  # Full path address of the input file
                # print("Input:", input_file_path)

                # prepare the output file name
                dot_index = file_name.rindex('.')           # Find the extension of the file in reverse
                file_name_only = file_name[:dot_index]      # Extract only the file name
                output_file_name = file_name_only.lower() + new_extension  # Add .grm/.txl/.jm extension with the lowercase file name
                output_file_path = os.path.join(source_input_store_directory, output_file_name)   # Create path for the output file
                # print("Output:", output_file_path)

                if user_choice == "jm":  # Prepare JM files by merging
                    # prepare path for finding included files
                    # Assuming that TXL & Grm files will be in the same folder
                    # Add an extra slash to complete the include path name.....
                    include_path = current_root_name + "\\"     # Determine the path where to search for included files
                    # print("Include from:", include_path)
                    start_txl_merge(txl_exe_path, txl_merge_program_path, input_file_path, output_file_path, include_path)  # Generate jm file & merge if needed
                    print(output_file_name, "<--", input_file_path, file=summary_file)
                else:
                    # No need for merging just collect the files with the desired extension
                    try:
                        if os.path.exists(output_file_path):    # Does the file exists? then skip
                            print(output_file_name, "<--", input_file_path, "<SameFileExists><CopySkipped>", file=summary_file)
                            count_same_file += 1
                        else:
                            shutil.copyfile(input_file_path, output_file_path)
                            count_copy_success += 1
                            print(output_file_name, "<--", input_file_path, "<CopySuccess>", file=summary_file)
                    except shutil.Error as shutil_error:
                            unknown_error += 1
                            print("Error in copying using shutil.copyfile:", type(shutil_error).__name__)
                            print(output_file_name, "<--", input_file_path, "<UnknownCopyError>", file=summary_file)
                    except OSError as os_error:
                            unknown_error += 1
                            print("Unhandled Error from OS:", type(os_error).__name__)
                            print(output_file_name, "<--", input_file_path, "<UnknownCopyError>", file=summary_file)

    print("Total file found:", count_file)
    print("\nTotal file found:", count_file, file=summary_file)
    if user_choice != "jm":  # Show number of copy except for merge operation
        print("Copied Successfully:", count_copy_success, "\nSame File found:", count_same_file, "\nUnknown Copy Error:", unknown_error)
        print("Copied Successfully:", count_copy_success, "\nSame File found:", count_same_file, "\nUnknown Copy Error:", unknown_error, file=summary_file)

    summary_file.close()


def main(txl_program_directory, source_program_directory, source_input_store_directory, user_choice, extension):
    txl_exe_path = txl_program_directory + "/bin/txl.exe"
    txl_merge_program_path = txl_program_directory + "/bin/merge.txl"       # txl program to perform the merging

    walk_in_directory_and_merge(source_program_directory, source_input_store_directory, txl_exe_path, txl_merge_program_path, user_choice, extension)  # Search files in the directory - Moon


'''
# Start merge_grm_txl_main() individual test
grm_txl_directory = input("Enter the directory path containing Grm and Txl files (case insensitive): ")
txl_directory = input("Enter the directory path containing txl.exe (case insensitive): ")
jm_result_directory = grm_txl_directory + "/TempJMfiles"
main(txl_directory, grm_txl_directory, jm_result_directory)
'''