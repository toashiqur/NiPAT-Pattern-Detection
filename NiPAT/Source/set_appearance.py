__author__ = 'ASR'

import xml.etree.ElementTree as ET
from operator import itemgetter
import time

def find_all_file_names(xml_fixed_file_path, summary_file, report_file_row, report_file_col, report_file_col_cell_width, report_file_xml):
    '''
    This function parses the given xml_fixed_nicad_clone_with_source_file,
    it finds out all file names and
    generates a list of unique file names in the clone files and
    set of unique file list for each clone class
    finally it passes these two parameters to generate set function for generating set.
    '''

    print("Start...")
    tree = ET.parse(xml_fixed_file_path)  #  phase-2
    '''
    try:
        tree = ET.parse(xml_fixed_file_path)  #  phase-2
    except ET.ParseError as parse_error:
        print("\nParse Failed!\nRemoval of xml tags from NiCAD generated clone file with source was not successful by the default XML fix program.\nSome Grammar/Txl file is containing exceptional use of XML tags or UTF-8 encoding(É).\nPlease change such uses from code to make the file parseable.\n Program Terminated!")
        print(type(parse_error).__name__)
        exit(1)
    '''
    root = tree.getroot()
    file_list = []  # Holds the list of all unique file names
    file_list_by_class = []   # each row indicates a class and holds its files
    row_for_current_class = -1
    total_file = 0

    for clschild in root.findall('class'):              # Take a class node
        # print("Clone class", clschild.get('classid'))
        print("Retrieving file names from Clone Class:", clschild.get('classid'), "...")
        row_for_current_class += 1
        first_element_of_class = True

        for srcchild in clschild.findall('source'):     # Take source node one by one and get the file name
            file_name = srcchild.get('file')
            if len(file_list) > 0 and file_name not in file_list:     # Add the file in the list if it is new..
                file_list.append(file_name)               # Make file list
                total_file += 1
            elif len(file_list) == 0:                                           # Empty set so just append
                file_list.append(file_name)
                total_file += 1

            # If current row has elements then check if it holds the current file otherwise membership checking in an empty list will generate error
            if not first_element_of_class and file_name not in file_list_by_class[row_for_current_class]:
                    file_list_by_class[row_for_current_class].append(file_name)  # Add the file_name for this class otherwise it exists so skip
            elif first_element_of_class:
                file_list_by_class.extend([[file_name]])    # Append a new row-- row_for_current_class
                first_element_of_class = False

    # Generate Summary Report (part-1/2)
    print("Total number of unique file names retrieved from NiCAD generated file:", total_file, file=summary_file)
    for each_file in file_list:
        print(each_file, file=summary_file)

    print("\nList of files in each of", len(file_list_by_class), "NiCAD clone class:", file=summary_file)
    for each_elem_in_file_list_by_cls in file_list_by_class:
        print(each_elem_in_file_list_by_cls, file=summary_file)

    generate_set(file_list, file_list_by_class, root, summary_file, report_file_row, report_file_col, report_file_col_cell_width, report_file_xml)    # Now Call it


def generate_set(file_list, file_list_by_class, root, summary_file, report_file_row, report_file_col, report_file_col_cell_width, report_file_xml):
    start_time = time.time()  # added in CTG
    file_list_len = len(file_list)       # No of total unique files
    file_list_by_class_len = len(file_list_by_class)    # No of clone class entry
    file_set_final = []    # Each row will contain a file set
    set_related_class_final = []  # Each corresponding row will contain the related class set
    found_in_class_temp = []

    for file_index_1 in range(0, file_list_len):
        file1 = file_list[file_index_1]                # Take a file from the file_list
        for file_index_2 in range(file_index_1+1, file_list_len):   # Take only the files in front
            file2 = file_list[file_index_2]            # Take the second file
            found_in_class_temp.clear()     # It will hold the class numbers where the files appear together
            for class_index in range(0, file_list_by_class_len):  # Take class entry one by one and search for the files
                if file1 in file_list_by_class[class_index]:   # Does the first file appear in this class if then
                    if file2 in file_list_by_class[class_index]:    # Does the second file appear in this class
                        # Both files appear in the same class
                        # then save the class and continue with rest of the classes
                        found_in_class_temp.append(class_index+1)  # Class_index+1 will give the original Nicad class no.
                        # print(file1, file2, "Found in Class Temp:", found_in_class_temp)

            if len(found_in_class_temp) > 1:    # then consider the set and classes
                if found_in_class_temp in set_related_class_final:  # if the found in class exists in the final class set
                    i = set_related_class_final.index(found_in_class_temp)
                    if file1 not in file_set_final[i]:      # file1 already exists in the set so add file2
                        file_set_final[i].append(file1)
                    if file2 not in file_set_final[i]:    # file2 already exists in the set so add file1
                        file_set_final[i].append(file2)
                else:  # it is a new entry
                    # found class set does not exist in the final set
                    file_set_final.extend([[file1, file2]])  # Make a list and store the file set in a new row
                    set_related_class_final.extend([found_in_class_temp.copy()])  # Store the related class in the corresponding row

    # for i in range(0, len(file_set_final)):
        # print(file_set_final[i])
        # print(set_related_class_final[i])

    # Generate Summary Report (part-2/2)
    print("\nTotal patterns found=", len(file_set_final))

    end_time = time.time()    # added in CTG
    total_time = end_time-start_time  # added in CTG
    print("\nTotal time needed to generate NiPAT pattern set is:", total_time, "s", file=summary_file)
    print("\nTotal time needed to generate NiPAT pattern set is:", total_time, "s")

    print("\nTotal number of sets found for pattern retrieval:", len(file_set_final), file=summary_file)
    for each_set_index in range(0, len(file_set_final)):
        print("\nPattern File Set:", each_set_index+1, ":", file_set_final[each_set_index], "\nNiCAD Class Set:", set_related_class_final[each_set_index], file=summary_file)

    start_time = time.time()
    print("Generating output file in row view...")
    find_common_code_by_file_row_view(file_set_final, set_related_class_final, root, report_file_row, report_file_xml)
    print("Generating output file in column view...")
    find_common_code_by_file_col_view(file_set_final, set_related_class_final, root, report_file_col, report_file_col_cell_width)

    end_time = time.time()
    total_time = end_time-start_time  # added in CTG
    print("\nTotal time needed to generate output file is:", total_time, "s", file=summary_file)
    print("\nTotal time needed to generate output file is:", total_time, "s")


def find_common_code_by_file_row_view(file_set_final, set_related_class_final, root, report_file, report_file_xml):

    mainTableTdStart = "<td style=\"background-color:#b0c4de; padding:6px; border:2px solid white\">"
    mainTableTdEnd = "</td>"
    mainTablePreStart = "<pre style=\"background-color:white; padding:2px\">"
    mainTablePreEnd = "</pre>"
    # ============================= Show code from each file ===============================

    src_instance = 0  # count the number of source file for xml output
    for set_index in range(0, len(file_set_final)):   # Take set collection one by one.
        file_set = file_set_final[set_index]                    # Take one set of file
        appears_in_class_set = set_related_class_final[set_index]  # class set of each file set can be found at the same index position

        file_set_len = len(file_set)

        print("<tr>", mainTableTdStart, "<font size=\"2\" color=\"blue\">", "PatternID:", set_index+1, "<br>Total files in set:", file_set_len, "<br>", file_set, "<br>Appears in total ", len(appears_in_class_set), "clone classes:", appears_in_class_set, "</font>", mainTableTdEnd, "</tr>", file=report_file)
        print("<pattern patternid=\"", set_index+1, "\" totalfilesinset=\"", file_set_len, "\" fileset=\"", file_set, "\" appearsintotal=\"", len(appears_in_class_set), "\" cloneclasses=\"", appears_in_class_set, "\">", file=report_file_xml)

        # Now take files one by one from the file_set and find out its code in related_class_set
        for file_index in range(0, file_set_len):
            current_file = file_set[file_index]  # Take one file from the set

            print("<tr>", mainTableTdStart, "<font size=\"2\" color=\"blue\">File:", file_index+1, "of", file_set_len, ":", current_file, "</font>", mainTableTdEnd, "</tr>", file=report_file)     # +1 converts file number starting from 1 instead of 0
            print("<sourcefileinfo file=\"", file_index+1, "/", file_set_len, "\" filename=\"", current_file, "\">", file=report_file_xml)

            appearance_total = 1  # count the number of appearance of this file

            # Find the data of the current file
            for clschild in root.findall('class'):              # Take a class node
                class_id_current = int(clschild.get('classid'))  # Convert original string class id to number
                class_similarity = int(clschild.get('similarity'))

                if class_id_current in appears_in_class_set:       # class_id_current exists in common set class of setA
                    print("<tr>", mainTableTdStart, "<font size=\"2\">Code in NiCAD Clone Class:", class_id_current, "...Similarity in NiCAD origin Class:", class_similarity, "... (appearnce no:", appearance_total, ")...</font>", mainTableTdEnd, "</tr>", file=report_file)
                    # appearance_total += 1
                    for srcchild in clschild.findall('source'):   # Read all source content of this class
                        if srcchild.get('file') == current_file:
                            src_instance += 1
                            print("<tr>", mainTableTdStart, mainTablePreStart, srcchild.text, mainTablePreEnd, mainTableTdEnd, "</tr>", file=report_file)       # if its file attribute matches then print whatever this source tag holding
                            print("<source codeinnicadcloneclass=\"", class_id_current, "\" similarityinnicadoriginclass=\"", class_similarity, "\" appearanceno=\"", appearance_total, "\" sourceinstance=\"", src_instance, "\">", srcchild.text, "</source>", file=report_file_xml)

                    appearance_total += 1

            print("</sourcefileinfo>", file=report_file_xml)

        print("</pattern>", file=report_file_xml)


def find_common_code_by_file_col_view(file_set_final, set_related_class_final, root, report_file, report_file_col_cell_width):

    # header_pre_start = "<pre style=\"background-color:white; padding:1px; font-family:Arial; font-size: 13px; color: blue; white-space: pre-wrap; word-wrap: break-word;\">"
    header_pre_start = "<pre style=\"background-color:#b0c4de; font-family:Arial; font-size: 13px; white-space: pre-wrap; word-wrap: break-word;\">"
    file_name_pre_start = "<pre style=\"font-family:Arial; font-size: 12px; white-space: pre-wrap; word-wrap: break-word;\">"
    code_pre_start = "<pre style=\"background-color:white; border:4px solid white; font-family:Courier New; font-size: 12px; white-space: pre-wrap; word-wrap: break-word;\">"
    pre_end = "</pre>"
    tableWithinTdStart = "<table width=" + report_file_col_cell_width +" style=\"table-layout:fixed; background-color:#b0c4de; padding:4px;\"> <tr><td>"
    tableWithinTdEnd = "</td></tr></table>"

    for set_index in range(0, len(set_related_class_final)):   # Take set collection one by one.
        file_set = file_set_final[set_index]  # file set of each class set can be found at the same index position
        appears_in_class_set = set_related_class_final[set_index]                    # Take one class set

        file_set_len = len(file_set)
        appears_in_set_len = len(appears_in_class_set)  # count the number of classes in the current set.

        print("<tr><td>", tableWithinTdStart, header_pre_start, "PatternID:", set_index+1, "<br>Total files in set:", file_set_len, "<br>", file_set, "<br>Appears in total ", appears_in_set_len, "clone classes:", appears_in_class_set, pre_end, tableWithinTdEnd, "</td></tr>", file=report_file)

        # Now take files one by one from the file_set and find out its code in related_class_set
        for class_index in range(0, appears_in_set_len):
            current_class = appears_in_class_set[class_index]  # Take one class from the set

            # Find the data of the current class
            for clsChild in root.findall('class'):              # Take a class node
                classIdFound = int(clsChild.get('classid'))  # Convert original string class id to number

                if classIdFound != current_class:   # take the next class
                    continue

                # match found with the current_class
                class_similarity = int(clsChild.get('similarity'))
                print("<tr><td>", tableWithinTdStart, header_pre_start, "Class:", class_index+1, "of", appears_in_set_len, "...Code in NiCAD Clone Class:", current_class, "...Similarity in NiCAD origin Class:", class_similarity, pre_end, tableWithinTdEnd, "</td></tr>", file=report_file)

                print("<tr bgcolor=\"#b0c4de\">", file=report_file)
                for targetFileName in file_set:     # Take files one by one from the file set
                    codeList = []  # will hold all code of a particular file in a class [code_header][code]

                    for srcChild in clsChild.findall('source'):   # Read all source content of this class
                        if srcChild.get('file') == targetFileName:  # then take the code
                            code = srcChild.text
                            splitForHeader = code.split(sep=' ', maxsplit=2)  # n-split gives n+1 part, header-type(0) header-name(1) body(2)
                            header_name = splitForHeader[1]      # header-name is expected to be the second word of the header declaration at index 1
                            codeList.extend([[header_name, code]])   # Append all code block header and code in code list

                    codeList.sort(key=itemgetter(0))    # Sort the code based on header such as function name

                    # Read all code from the sorted codeList
                    codeInClass = ''
                    for codeIndex in range(0, len(codeList)):
                        if codeInClass != '':
                            codeInClass += '\n...........................\n'   # separates multiple code chunks inside same class
                        codeInClass += codeList[codeIndex][1]

                    # print the collected code in table cell
                    print("<td valign=\"top\">", tableWithinTdStart, file_name_pre_start, targetFileName, "<br>", "CloneClass=", current_class, "Similarity=", class_similarity, pre_end, code_pre_start, codeInClass, pre_end, tableWithinTdEnd, "</td>", file=report_file)

                print("</tr>", file=report_file)  # Now we shall go for the next class so close the row here..
                break  # current_class will appear only once so break and take the next class as current_class

        #print("</table>", file=report_file)


def main(xml_fixed_file_path, pattern_summary_path, pattern_report_path_row_view, pattern_report_path_col_view, report_file_col_cell_width, pattern_report_path_xml):
    # Create file for writing
    summary_file = open(pattern_summary_path, 'w')
    report_file_row = open(pattern_report_path_row_view, 'w')
    report_file_col = open(pattern_report_path_col_view, 'w')
    report_file_xml = open(pattern_report_path_xml, 'w')

    html_head_start = "<html> <head> <title> Code Pattern Analysis v-1.2 (10th-Jul-15) </title></head>"
    html_body_start = "<body style = \"font-family:Arial\"> <h2> Pattern Report of the appearance of file set in class set </h2>"
    table_head_start = "<table frame=\"box\" style=\"table-layout:auto background-color:white; border:0px solid white; margin-left:auto; margin-right: auto\">"
    print(html_head_start, html_body_start, table_head_start, file=report_file_row)
    print(html_head_start, html_body_start, table_head_start, file=report_file_col)

    print("<patterns> <Title> Pattern Report of the appearance of file set in class set </Title>", file=report_file_xml)

    find_all_file_names(xml_fixed_file_path, summary_file, report_file_row, report_file_col, report_file_col_cell_width, report_file_xml)

    print("</table> </body> </html>", file=report_file_row)
    print("</table> </body> </html>", file=report_file_col)
    print("</patterns>", file=report_file_xml)

    summary_file.close()
    report_file_row.close()
    report_file_col.close()
    report_file_xml.close()


'''
# Start clone set main- Unblock to test individually
xml_fixed_file_path = input("Enter the path of the xml fixed clone file with extension(c:/myfolder/myfile.xml)")
summary_file = open('f:/testsummary.txt', 'w')
report_file = open('f:/testres.html', 'w')
print("<html> <head> <style type=\"text/css\"> body {font-family:Arial} table {background-color:white; border:0px solid white; width:95%; margin-left:auto; margin-right: auto} td {background-color:#b0c4de; padding:16px; border:4px solid white} pre {background-color:white; padding:4px} </style> <title> NiCad Clone Report </title> </head>", file=report_file)
print("<body> <h2> Pattern Report by File </h2>", file=report_file)
find_all_file_names(xml_fixed_file_path, report_file)
print("</html>", file=report_file)
report_file.close()
'''