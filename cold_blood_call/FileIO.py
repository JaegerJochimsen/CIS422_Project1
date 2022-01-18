"""
File: FileIO.py
Description: Contains functions that allows the system to interace with files
    in order to save/maintain/read data. (Also contains test for this module)
Dependencies: None
Author(s): Nick Johnstone
Dates: 1/12/2022, 1/13/2022, 1/14/2022, 1/15/2022, 1/16/2022, 1/17/2022
       1/18/2022
Credit: N/A
"""
import sys
from os import listdir, getcwd, mkdir
from datetime import date, datetime
from operator import itemgetter
from re import search


# Delimiter represents how each field in the files are separated
DELIMITER = '\t'


def _checkValidRoster(rosterFile:str)->str:
    """
    Parameter:
        rosterFile  -   a string that represents a file name of a roster

    Called by:
        FileIO.py - readRoster()

    Calls:
        re  -   search()

    Modifies:
        N/A

    Return:
        string that is either VALID or an error message

    Description:
        This functions makes sure that the roster file passed in is a valid file.
        It does this by first checking that the length of each line which should
        represent each student is correct. Then the function uses regular
        expressions to check that the student IDs and emails are in the
        correct format. If the file does not pass these checks a specific error
        message is returned to be displayed on the GUI. If the file does pass
        all of the tests the string "VALID" is returned.
    """

    # store the open file object in open_roster
    open_roster = open(rosterFile, "r")
    # initial a list to store each line in the file
    roster_list = list()
    for line in open_roster:
        roster_list.append(line.strip().split(f"{DELIMITER}"))

    # check that the length of each line is corrent
    # if not return false right away
    # then check for valid ID and email
    for i, student in enumerate(roster_list):
        # check length of each line
        if (len(student) != 4) and (len(student) != 6):
            open_roster.close()
            return (f"Invalid number of fields for student on line: {i+1}")

        # regex check for ID (3rd element should always be ID according to SRS)
        if search("[0-9]{9}", student[2]) == None:
            open_roster.close()
            return (f"Invalid student ID number on line: {i+1}")

        # regex check for email (4th element should always be email according to SRS)
        if search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", student[3]) == None:
            open_roster.close()
            return (f"Invalid email on line: {i+1}")

    # will only reach here if roster is valid
    open_roster.close()
    return "VALID"


def readRoster(rosterFile:str="initial_roster.txt")->(list, bool) or str:
    """This function will return a list of lists
    or if a roster is unable to be found it returns False
    """

    initial = True
    if ".saved_boot.txt" in listdir():
        roster = open(".saved_boot.txt", "r")
        initial = False
        print("READING SAVED BOOT")
    elif "initial_roster.txt" in listdir():
        roster_status = _checkValidRoster("initial_roster.txt")
        if roster_status == "VALID":
            print("READING DEFAULT")
            roster = open("initial_roster.txt", "r")
        else:
            return roster_status
    elif rosterFile != "initial_roster.txt":
        roster_status = _checkValidRoster(rosterFile)
        if roster_status == "VALID":
            print("READING CUSTOM")
            roster = open(rosterFile, "r")
        else:
            return roster_status
    else:
        return "Please provide an initial roster"

    student_list = list()
    for line in roster:
        student_list.append(line.strip().split(f'{DELIMITER}'))

    if initial:
        for student in student_list:
            if len(student) == 4: # if no phonetic and no reveal code
                student.append("None") # no phonetic
                student.append("None") # no reveal code
            student.append("False") # spoken initially False (first class)
            student.append("0") # previous contributions initially 0 (first class)
            student.append("0") # previous flags initially 0 (first class)

    roster.close()
    sorted_student_list = sorted(student_list, key=itemgetter(1))
    return (sorted_student_list, initial)



def writeToSavedBootRoster(students:list)->None:
    """
    This function will take an argument in the form of a list of lists where
    the internal list will be a student and the elements will be each attribute
    from the student object

    This function will always produce a file in the following format:
    <first_name><tab><last_name><tab><UO_ID><tab><email><tab><phonetic><tab>
    <reveal_code><tab><spoken_this_session(True/False)><tab>
    <previous_contributions(including current session)><tab>
    <flagged_count(including current session)><\n>
    """
    new_roster = open(".saved_boot.txt", "w")
    for student in students:
        new_roster.write(f"{student[0]}{DELIMITER}") # first name
        new_roster.write(f"{student[1]}{DELIMITER}") # last name
        new_roster.write(f"{student[2]}{DELIMITER}") # UO ID
        new_roster.write(f"{student[3]}{DELIMITER}") # email
        new_roster.write(f"{student[4]}{DELIMITER}") # phonetic
        new_roster.write(f"{student[5]}{DELIMITER}") # reveal code
        new_roster.write(f"{student[6]}{DELIMITER}") # spoken (True/False)
        previous_contributions = str((int(student[9]) + int(student[8])))
        new_roster.write(f"{previous_contributions}{DELIMITER}") # previous contributions = previous_contributions + contributions
        if student[7] == "True": # check if the student was flagged this session
            new_roster.write(f"{str(int(student[10]) + 1)}\n") # increment the flagged count
        else:
            new_roster.write(f"{student[10]}\n") # not flagged, no increment
        #new_roster.write("\n")
    new_roster.close()


def _formatResponseCode(bl:str)->str:
    if bl == "True":
        return "X"
    elif bl == "False":
        return ""
    else:
        return "ERROR"


def _checkIfFileDir()->bool:
    if "MetaData" in listdir():
        return True
    return False


def writeToLogFile(students:list)->None:
    """
    This function will take an argument in the form of a list of lists where
    the internal list will be a student and the elements will be each attribute
    from the student object

    This function will always produce a file that looks like this:
    Log File for <date>

    -----------------------------------------------------
    First Name: <first_name>
    Last Name: <last_name>
    UO ID: <UO_ID>
    Email: <email>
    Phonetic: <phonetic>
    Reveal Code: <reveal_code>
    Contributions This Session: <contributions>
    Flagged: <Yes/No>
    -----------------------------------------------------
    """

    dir_exists = _checkIfFileDir()
    if not dir_exists:
        cwd = getcwd()
        new_dir = cwd + "/MetaData"
        mkdir(new_dir)

    log_name = "LogFile-" + str(datetime.now())
    log_file = open(f"MetaData/{log_name}", "w")
    log_file.write(f"Log File for Cold Call Assist Program\n\
            {str(date.today()).replace('-', '/')}:\n\n")

    log_file.write("----------------------------------------------------\n")

    for student in students:
        if int(student[8]) > 0:
            log_file.write(f"{_formatResponseCode(student[7])}{DELIMITER}")
            log_file.write(f"{student[0]} {student[1]}{DELIMITER}")
            log_file.write(f"{student[3]}\n")

    log_file.close()


def updatePerforanceFile(students:list):

    # This is the case when there is no current performance file
    if "Performance-File.txt" not in listdir("MetaData"):
        performance_file = open("MetaData/Performance-File.txt", "w")

        performance_file.write("Performance File for Cold Call Assist Program\n")
        performance_file.write("Total Times  Called\tNumber of Flags\t")
        performance_file.write("First Name\tLast Name\tUO ID\tEmail\t")
        performance_file.write("Phonetic Spelling\tReveal Code\tList of Dates\n")

        for student in students:
            performance_file.write(f"{student[8]}\t") # add the contributions line
            #print(f"ADDED CONTRIBUTIONS for {student[0]}: {student[8]}")
            if student[7] == "True":
                performance_file.write(f"1\t") # add the flag count line
                #print(f"ADDED FLAGS for {student[0]}: 1")
            else:
                performance_file.write(f"0\t") # add the flag count line
                #print(f"ADDED FLAGS for {student[0]}: 0")
            performance_file.write(f"{student[0]}\t") # add the first name
            performance_file.write(f"{student[1]}\t") # add the last name
            performance_file.write(f"{student[2]}\t") # add the id num
            performance_file.write(f"{student[3]}\t") # add the email
            performance_file.write(f"{student[4]}\t") # add the email
            if int(student[8]) > 0:
                performance_file.write(f"{student[5]}\t") # add the reveal code
                performance_file.write(f"{str(date.today()).replace('-', '/')}\n") # add the date
            else:
                performance_file.write(f"{student[5]}\n") # add the reveal code

        performance_file.close()
        return None


    # when the file exists but needs to be updated after the session
    performance_file = open("MetaData/Performance-File.txt", "r")

    # skip the head and collumns lines
    performance_file.readline()
    performance_file.readline()


    # put each student in the old performance_file into a list and split each
    # of their fields into a a seperate element of the internal list
    prev_file = list()
    for student in performance_file:
        prev_file.append(student.strip().split("\t"))

    performance_file.close()

    # sort the list by last name so it lines up with the data that is passed in
    prev_file_sorted = sorted(prev_file, key=itemgetter(3))

    # sort the list that is passed in so it lines up with the old performance_file order
    current_list = sorted(students, key=itemgetter(1))

    # go through each student from the current session and check if they spoke
    # if they did add the date to the list that will be written to the performance_file
    # this includes incrementing the contributions field, as well as the flag field (when applicable)
    for i, student in enumerate(current_list):
        if int(student[8]) > 0:
            # add the number of times the student contributed in the current session to the total
            prev_file_sorted[i][0] = str((int(student[9]) + int(student[8])))
            if student[7] == "True":
                prev_file_sorted[i][1] = str(int(prev_file_sorted[i][1]) + 1)
            prev_file_sorted[i].append(str(date.today()).replace('-', '/'))


    #ready to write to file
    # create a new file, overwriting the old one
    performance_file = open("MetaData/Performance-File.txt", "w")

    performance_file.write("Performance File for Cold Call Assist Program\n")
    performance_file.write("Total Times  Called\tNumber of Flags\t")
    performance_file.write("First Name\tLast Name\tUO ID\tEmail\t")
    performance_file.write("Phonetic Spelling\tReveal Code\tList of Dates\n")

    # add each of the students to the new file
    for student in prev_file_sorted:
        for item in student:
            performance_file.write(f"{item}\t")
        performance_file.write("\n")

    performance_file.close()

    return None


def _testReadRoster():
    # readRoster tests
    rosty = readRoster()
    print(rosty)

def _testWriteToSavedBootRoster():
    # writeToSavedBootRoster
    test_function_input = [
            # FN       LN           UO ID           EMAIL         PONETIC  REVEAL_CODE       SPOKEN  FLAGGED CC   PC   PF
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', '848fsdfhkjhe8f9', 'True', 'True', '1', '5', '4'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', '848fsdfhkjhe8f9', 'True', 'False', '0', '5', '4'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4']
            ]

    writeToSavedBootRoster(test_function_input)
    # this should produce: ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu',
    #    'nook', '848fsdfhkjhe8f9', 'True', '6', '5']

def _testWriteToLogFiles():
    # writeToLogFile tests
    test_function_input = [
            # FN       LN           UO ID           EMAIL         PONETIC  REVEAL_CODE       SPOKEN  FLAGGED CC   PC   PF
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', '848fsdfhkjhe8f9', 'True', 'True', '1', '5', '4'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', '848fsdfhkjhe8f9', 'True', 'False', '0', '5', '4'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4']
            ]
    writeToLogFile(test_function_input)
    # this should produce:
    # X	Nick Johnstone	nsj@uoregon.edu

def _testUpdatePerformanceFile():
    # update performance file test
    test_function_input = [
            # FN       LN           UO ID           EMAIL         PONETIC  REVEAL_CODE       SPOKEN  FLAGGED CC   PC   PF
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', '848fsdfhkjhe8f9', 'True', 'True', '1', '5', '4'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', '848fsdfhkjhe8f9', 'True', 'False', '0', '5', '4'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4']
            ]
    updatePerforanceFile(test_function_input)

def _testCheckValidRoster():
    valid_bool = _checkValidRoster("initial_roster.txt")
    print(valid_bool)


if __name__ == "__main__":
    """Testing"""
    if not __debug__:
        _testReadRoster()
        #_testWriteToSavedBootRoster()
        #_testWriteToLogFiles()
        #_testUpdatePerformanceFile
        #_testCheckValidRoster()

