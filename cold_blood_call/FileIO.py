"""
File: FileIO.py
Description: Contains functions that allows the system to interace with files
    in order to save/maintain/read data. (Also contains test for this module)
Dependencies: None
Author(s): Nick Johnstone 1/12/22, 1/13/2022
Credit:
"""
import sys
from os import listdir, getcwd, mkdir
from datetime import date
from operator import itemgetter

DELIMETER = '\t'


def _checkInitialBootStatus()->bool:
    if ".saved_boot.txt" in listdir():
        return False
    return True

def _checkIfAnyRoster()->bool:
    if ".saved_boot.txt" in listdir():
        return True
    elif "initial_roster.txt" in listdir():
        return True
    else:
        return False

def _checkIfFileDir()->bool:
    if "MetaData" in listdir():
        return True
    return False

def readRoster(rosterFile="initial_roster.txt")->list or bool:
    """This function will return a list of lists
    or if a roster is unable to be found it returns False
    """

    if not _checkIfAnyRoster(): # check if any roster exists
        return _checkIfAnyRoster()

    initial = _checkInitialBootStatus()
    if initial:
        roster = open(rosterFile, "r")
    else:
        roster = open(".saved_boot.txt", "r")
        print("READING SAVED BOOT")

    student_list = list()
    for line in roster:
        student_list.append(line.strip().split(f'{DELIMETER}'))

    if initial:
        for student in student_list:
            if len(student) == 4: # if no phonetic and no reveal code
                student.append("None") # no phonetic
                student.append("None") # no reveal code
            student.append("False") # spoken initially False (first class)
            student.append("0") # previous contributions initially 0 (first class)
            student.append("0") # previous flags initially 0 (first class)

    roster.close()
    return student_list



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
        new_roster.write(f"{student[0]}{DELIMETER}") # first name
        new_roster.write(f"{student[1]}{DELIMETER}") # last name
        new_roster.write(f"{student[2]}{DELIMETER}") # UO ID
        new_roster.write(f"{student[3]}{DELIMETER}") # email
        new_roster.write(f"{student[4]}{DELIMETER}") # phonetic
        new_roster.write(f"{student[5]}{DELIMETER}") # reveal code
        new_roster.write(f"{student[6]}{DELIMETER}") # spoken (True/False)
        previous_contributions = str((int(student[9]) + int(student[8])))
        new_roster.write(f"{previous_contributions}{DELIMETER}") # previous contributions = previous_contributions + contributions
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

    log_name = "LogFile-" + str(date.today())
    log_file = open(f"MetaData/{log_name}", "w")
    log_file.write(f"Log File for Cold Call Assist Program\n\
            {str(date.today())}:\n\n")

    log_file.write("----------------------------------------------------\n")

    for student in students:
        if int(student[8]) > 0:
            log_file.write(f"{_formatResponseCode(student[7])}{DELIMETER}")
            log_file.write(f"{student[0]} {student[1]}{DELIMETER}")
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
                performance_file.write(f"{str(date.today())}\n") # add the date
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
            prev_file_sorted[i].append(str(date.today()))


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


def _tests():
    """
    # readRoster tests
    rosty = readRoster()
    print(rosty)


    # writeToSavedBootRoster
    test_function_input = [['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu',
        'nook', '848fsdfhkjhe8f9', 'True', 'True', '1', '5', '4']]

    writeToSavedBootRoster(test_function_input)
    # this should produce: ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu',
    #    'nook', '848fsdfhkjhe8f9', 'True', '6', '5']



    # writeToLogFile tests
    test_function_input = [['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu',
        'nook', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4']]
    writeToLogFile(test_function_input)
    # this should produce:
    # X	Nick Johnstone	nsj@uoregon.edu
    """

    # update performance files test
    test_function_input = [
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', '848fsdfhkjhe8f9', 'True', 'True', '1', '5', '4'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', '848fsdfhkjhe8f9', 'True', 'False', '0', '5', '4'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', '848fsdfhkjhe8f9', 'True', 'False', '1', '5', '4']
            ]
    updatePerforanceFile(test_function_input)


if __name__ == "__main__":
    """Testing"""
    if not __debug__:
        _tests()

