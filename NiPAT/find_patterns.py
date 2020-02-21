__author__ = 'ASR'

import create_directory
import collect_or_merge_input_file
import move_non_program
import find_clones
import fix_broken_xml
import set_appearance
import os


def main():
    #txl_program_directory = os.path.normpath(input("Enter Txl program directory path(c:/txl)(case insensitive): "))     # os.path.normpath will make the pathname consistent
    txl_program_directory = os.path.normpath("C:/Users/ASR/Desktop/Txl106a7_32")  

    source_program_directory = os.path.normpath(input("Enter source program directory path containing Grm and Txl files (case insensitive): "))
    cygwin_terminal_path = ["C:/cygwin64/bin/mintty.exe", "-"]

    # Find out the folder one folder back of the given source_program_directory
    # Collected/Merged files must be put in a folder other than the source directory
    slash_index = source_program_directory.rindex('\\')
    source_input_directory = source_program_directory[:slash_index]

    extension_ok = False
    extension = []    # Tuple to hold extension
    report_col_cell_width = "640"  # default cell width for rules.

    while True:
        user_choice = input("Enter your choice for finding:\n1> Patterns in grammar only.\n2> Patterns in rule only. \n3> Patterns in grammar+rule together.")
        if user_choice == "1" or user_choice == "2" or user_choice == "3":

            # Take extension input from user
            while not extension_ok:
                extension_input = input("Enter space separated File extension to search for(.ext1 .ext2 .ext3...)(Case Insensitive):").lower()

                if '.' in extension_input and ',' not in extension_input:
                    extension_input = extension_input.split()   # Space separated extension
                    extension = tuple(extension_input)
                    extension_ok = True
                    if user_choice == "1":
                        print("Files with extension:", extension_input, "will be stored with *.grm extension.")
                    elif user_choice == "2":
                        print("Files with extension:", extension_input, "will be stored with *.txl extension.")
                    else:
                        print("Files with extension:", extension_input, "will be stored with *.jm extension.")
                    #print(extension_input)
                    #print(extension)
                else:
                    print("Extension not in format.")
                    try_again = input("Want to change extension?(y/n):").lower()
                    if try_again == 'n':
                        print("Program will search for Default Extensions.")
                        break  # while not extension_ok
            break   # while True
        else:
            print("Wrong Choice!")

    # Create source_input_directory path where retrieved/merged input files will be stored.
    if user_choice == "1":
        user_choice = "grm"     # it will help later to understand the code instead of 1,2,3
        source_input_directory = os.path.join(source_input_directory, "GRMfiles")  # os.path.join will place the separator automatically
        create_directory.main(source_input_directory, user_choice)
        collect_or_merge_input_file.main(txl_program_directory, source_program_directory, source_input_directory, user_choice, extension)
        print(".grm files containing Txl Grammars have been stored in:", source_input_directory)
        report_col_cell_width = "500"
    elif user_choice == "2":
        user_choice = "txl"
        source_input_directory = os.path.join(source_input_directory, "TXLfiles")
        create_directory.main(source_input_directory, user_choice)
        collect_or_merge_input_file.main(txl_program_directory, source_program_directory, source_input_directory, user_choice, extension)
        print(".txl files containing Txl Rules have been stored in:", source_input_directory)
    else:
        user_choice = "jm"
        non_program_jm_directory = os.path.join(source_input_directory, "RemovedNonProgramJM")
        source_input_directory = os.path.join(source_input_directory, "JMfiles")
        create_directory.main(source_input_directory, user_choice)
        print("Step 1 of 5: Merging Grm and Txl files...")
        collect_or_merge_input_file.main(txl_program_directory, source_program_directory, source_input_directory, user_choice, extension)    # Step1: Merge Grammar & Txl into gm files
        print(".jm files containing Txl Grammars and Rules have been stored in:", source_input_directory)

        # remove those jm file which do not have the main rule/function
        print("Step 2 of 5: Moving non-program *.jm files...")
        move_non_program.main(source_input_directory, non_program_jm_directory)
        print("Non-program *.jm files have been moved from the JM directory")


    print("Step 3 of 5: Use NiCAD command to generate clones...")
    if user_choice == "grm":  # Work only on Grammar
        print("granularity = grammar\nlanguage = grm \nnormalization = blocknormalize/blindnormalize")
    elif user_choice == "txl":  # Work only on Rules
        print("granularity = rules\nlanguage = txl \nnormalization = blocknormalize/blindnormalize")
    elif user_choice == "jm":  # Work on both
        print("granularity = txl\nlanguage = jm \nnormalization = blocknormalize/blindnormalize")

    find_clones.find_clones_main(cygwin_terminal_path)              # Step2: Invoke Cygwin terminal allowing user to run NiCAD
    print("Clone generation has been finished using NiCAD.")

    print("Step 4 of 5: Fixing broken xml tags...")
    nicad_generated_clone_with_source = os.path.normpath(input("Enter the path of NiCAD generated clone file with extension(c:/myfolder/myfile.xml):"))

    # Generate the output file name with the same name given by NiCAD but with xml_fixed.xml extension.
    dot_index_in_nicad_name = nicad_generated_clone_with_source.rindex('.')            # Find the extension of the file in reverse
    slash_index_in_nicad_name = nicad_generated_clone_with_source.rindex('\\')
    nicad_generated_file_name = nicad_generated_clone_with_source[slash_index_in_nicad_name+1:dot_index_in_nicad_name]  # Extract only the file name with path..no extension
    xml_fixed_file_name = nicad_generated_file_name + "_xml_fixed.xml"       # Add _xml_fixed word with the output file

    # slash_index = source_input_directory.rindex('\\')  # dscard the folder name at the end of source_input_directory
    source_input_directory = source_input_directory[:slash_index]  # Take working directory one folder back
    xml_fixed_file_path = os.path.join(source_input_directory, xml_fixed_file_name)
    # fix_broken_xml.fix_broken_xml_tags_main(txl_program_directory, nicad_generated_clone_with_source, xml_fixed_file_path)   # to use txl fix program Step3: Fix the broken xml tags in clone class with source file by NiCAD
    fix_broken_xml.main(nicad_generated_clone_with_source, xml_fixed_file_path)   # Step3: Fix the broken xml tags in clone class with source file by NiCAD
    print("Broken xml tags have been fixed.")

    print("Step 5 of 5: Finding Patterns...")
    summary_file_name = nicad_generated_file_name + "_pattern_summary.txt"
    pattern_summary_path = os.path.join(source_input_directory, summary_file_name)

    report_file_name = nicad_generated_file_name + "_pattern_by_file_row_view.html"
    pattern_report_path_row_view = os.path.join(source_input_directory, report_file_name)

    report_file_name = nicad_generated_file_name + "_pattern_by_file_col_view.html"
    pattern_report_path_col_view = os.path.join(source_input_directory, report_file_name)

    report_file_name_xml = nicad_generated_file_name + "_pattern_by_file.xml"
    pattern_report_path_xml = os.path.join(source_input_directory, report_file_name_xml)

    set_appearance.main(xml_fixed_file_path, pattern_summary_path, pattern_report_path_row_view, pattern_report_path_col_view, report_col_cell_width, pattern_report_path_xml)  # Step4: Find clone set

# Start main
main()