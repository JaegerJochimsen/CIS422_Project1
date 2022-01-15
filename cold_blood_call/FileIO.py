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
        student_list.append(line.strip().split('\t'))

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
        new_roster.write(f"{student[0]}\t") # first name
        new_roster.write(f"{student[1]}\t") # last name
        new_roster.write(f"{student[2]}\t") # UO ID
        new_roster.write(f"{student[3]}\t") # email
        new_roster.write(f"{student[4]}\t") # phonetic
        new_roster.write(f"{student[5]}\t") # reveal code
        new_roster.write(f"{student[6]}\t") # spoken (True/False)
        previous_contributions = (int(student[9]) + int(student[8]))
        new_roster.write(f"{previous_contributions}\t") # previous contributions = previous_contributions + contributions
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
            log_file.write(f"{_formatResponseCode(student[7])}\t")
            log_file.write(f"{student[0]} {student[1]}\t")
            log_file.write(f"{student[3]}\n")

    log_file.close()


def _tests():
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

if __name__ == "__main__":
    """Testing"""
    if not __debug__:
        test()

