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
        if (len(student) != 4) and (len(student) != 5):
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


def readRoster(rosterFile:str="initial_roster.txt")->(list, bool) or (str, bool):
    """
    Parameter:
        rosterFile  -   a string that represents a file name of a roster

    Called by:
        Main.py - main()

    Calls:
        FileIO.py  -   _testCheckValidRoster()

    Modifies:
        N/A

    Return:
        tuple with 2 elements:
            1. list of lists where each internal list holds data for a student
            2. boolean that is True if it is the initial bootup, False on
            subsequent bootups
        OR
        tuple with 2 elements:
            1. string that is an error message if an invalid roster was provided
            2. True value because it has to be initial if the roster is invalid

    Description:
        This functions reads a roster file in and splits up each student into a
        list where each element of the list is a data field associated with that
        student.
        The data fields are as follows:
            1. First Name
            2. Last Name
            3. ID Number
            4. Email
            5. Phonetic (optional)
            for internal system use:
            6. Spoken Boolean (str(True) if spoken before all others have spoken)
            7. Previous Contributions (a tally of how many times the student spoke)
            8. Previous Flags (a tally of the previous flags the student has)
        Each of these lists is returned in a main list that is passed to main.py
        to be converted to Student Objects.

        Alternatively, an error message in the form of a string can be returned
        when the roster is invalid. This message will be eventually displayed on
        the users screen.
    """

    # first check if the system data directory exists
    if ".sysData" not in listdir():
        # if not get the current working directory information
        cwd = getcwd()
        # create the path of the new data directory
        new_dir = cwd + "/.sysData"
        # create the data directory
        mkdir(new_dir)

    # variable to represent if it is the first bootup of the system
    initial = True

    # check if the system datafile exists
    if "saved_boot.txt" in listdir(".sysData/"):
        # assign the roster to the system's store data file
        roster = open(".sysData/saved_boot.txt", "r")
        # not the first bootup
        initial = False
        print("READING SAVED BOOT")

    # check if the defualt name for the initial roster exists
    elif "initial_roster.txt" in listdir():
        # roster_status stores the validity of the initial roster
        roster_status = _checkValidRoster("initial_roster.txt")
        # if the initial roster is valid
        if roster_status == "VALID":
            print("READING DEFAULT")
            # roster now contains the initial roster
            roster = open("initial_roster.txt", "r")
        # if the initial roster is not in a valid format return error message
        else:
            return (roster_status, True)

    # if a roster with an alternate name is being used
    elif rosterFile != "initial_roster.txt":
        # roster_status stores the validity of the initial roster
        roster_status = _checkValidRoster(rosterFile)
        # if the initial roster is valid
        if roster_status == "VALID":
            print("READING CUSTOM")
            # roster now contains the initial roster with a custom name
            roster = open(rosterFile, "r")
        # if the initial roster is not in a valid format return error message
        else:
            return (roster_status, True)
    # no roster is provided, return a message that prompts the user to input a file
    else:
        return ("Please provide an initial roster", True)

    # initialize a list that will hold each student
    student_list = list()
    # parse through each line in the roster file
    for line in roster:
        # add a list split on the delimiter that holds data for the given student
        student_list.append(line.strip().split(f'{DELIMITER}'))

    # if this is the initial bootup the system will add additional fields
    if initial:
        # parse through each student
        for student in student_list:
            # is roster with no phonetic, add none value to that field
            if len(student) == 4: # if no phonetic
                student.append("None") # no phonetic
            # add initial values for each student in the following fields:
            # spoken recently initially False (first session)
            student.append("False")
            # previous contributions initially 0 (first session)
            student.append("0")
            # previous flags initially 0 (first session)
            student.append("0")
            # previous absences initially 0 (first session)
            student.append("0")

    roster.close()
    # return the list sorted by last name
    sorted_student_list = sorted(student_list, key=itemgetter(1))
    return (sorted_student_list, initial)




def writeToSavedBootRoster(students:list)->None:
    """
    Parameter:
        students  -   a list of lists where each of the internal lists contain
                      data entries for the student (this argument is the return
                      value of toStrList() from Student.py)

    Called by:
        Main.py - main()

    Calls:
        N/A

    Modifies:
        N/A

    Return:
        None
        (Produces a file, see desciption for details)

    Description:
        This function takes the list of lists produced by toStrList in Student.py
        and creates a file called "saved_boot_roster.txt" in the .sysData/
        directory that stores that data in the following format:

        <first_name><tab><last_name><tab><UO_ID><tab><email><tab>
        <phonetic><tab><spoken_recently(True/False)><tab>
        <previous_contributions(including current session)><tab>
        <flagged_count(including current session)><\n>

        This file will then be used in subsequent bootups to insure continuity
        between class sessions. The file will also be hidden from the user as
        it should not be modified, except by the system.

    """

    # create the .saved_boot_roster.txt file
    new_roster = open(".sysData/saved_boot.txt", "w")

    # parse through the student list and write to each attribute to the file
    for student in students:
        # write first name
        new_roster.write(f"{student[0]}{DELIMITER}")

        # write last name
        new_roster.write(f"{student[1]}{DELIMITER}")

        # write UO ID
        new_roster.write(f"{student[2]}{DELIMITER}")

        # write email
        new_roster.write(f"{student[3]}{DELIMITER}")

        # write phonetic
        new_roster.write(f"{student[4]}{DELIMITER}")

        # write spoken recently (True/False)
        new_roster.write(f"{student[6]}{DELIMITER}")

        # calculate new previous contributions current + previous
        previous_contributions = str((int(student[9]) + int(student[8])))
        # write new previous_contributions
        new_roster.write(f"{previous_contributions}{DELIMITER}")

        # calculate the new previous_flags
        previous_flags = str(int(student[7]) + int(student[10]))
        # write the new previous_flags
        new_roster.write(f"{previous_flags}{DELIMITER}")

        # check if the student was absent
        if student[5] == "False":
            # if present is false, increment absences
            print(student[11])
            new_roster.write(f"{str(int(student[11]) + 1)}\n")
        else:
            # if the student was present, do not increment absences
            new_roster.write(f"{student[11]}\n")

    new_roster.close()


def _formatResponseCode(bl:str)->str:
    if bl == "True":
        return "X"
    elif bl == "False":
        return "S"
    else:
        return "ERROR"


def _checkIfFileDir()->bool:
    if "MetaData" in listdir():
        return True
    return False


def writeToLogFile(students:list)->None:
    """
    Parameter:
        students  -   a list of lists where each of the internal lists contain
                      data entries for the student (this argument is the return
                      value of toStrList() from Student.py)

    Called by:
        Main.py - main()

    Calls:
        datetime    -   now()

    Modifies:
        N/A

    Return:
        None
        (Produces a file, see desciption for details)

    Description:
        This function takes the list of lists produced by toStrList in Student.py
        and creates a file called "LogFile-<date time>" that stores data
        pertaining to the session of the system that was just completed.
        This data includes, a list of students who spoke, a list of students,
        who were absent, and a list of students who were flagged.
        The file will look like the following:

        Log File for Cold Call Assist Program
                    2022/01/19:

        ----------------------------------------------------
        <Spoken/Flagged/Absent>	First Name Last Name	Email
        <Spoken/Flagged/Absent>	First Name Last Name	Email
        <Spoken/Flagged/Absent>	First Name Last Name	Email
        <Spoken/Flagged/Absent>	First Name Last Name	Email
        ----------------------------------------------------

        The purpose of this log file is to allow the user to keep a log of
        student performance for every given class session.
    """

    # check if the data directory already exists
    if not _checkIfFileDir():
        # if not get the current working directory information
        cwd = getcwd()
        # create the path of the new data directory
        new_dir = cwd + "/MetaData"
        # create the data directory
        mkdir(new_dir)

    # create the logfile for the current session
    log_name = "LogFile-" + str(datetime.now())
    log_file = open(f"MetaData/{log_name}", "w")
    # after opening the file, write the header
    log_file.write(f"Log File for Cold Call Assist Program\n\
            {str(date.today()).replace('-', '/')}:\n\n")

    # create a bar to separate the header from the data
    log_file.write("----------------------------------------------------\n")

    # parse through each student in the student list argument
    for student in students:
        # check if the student was absent
        if student[5] == "False":
            # record that they were absent
            log_file.write(f"A{DELIMITER}")
            # record the student's name
            log_file.write(f"{student[0]} {student[1]}{DELIMITER}")
            # record the student's name
            log_file.write(f"{student[3]}\n")

        # check if the student was flagged at all
        elif int(student[7]) > 0:
            # record that they were flagged
            log_file.write(f"X{DELIMITER}")
            # record the student's name
            log_file.write(f"{student[0]} {student[1]}{DELIMITER}")
            # record the student's name
            log_file.write(f"{student[3]}\n")

        # check if the student was spoken but not flagged
        elif int(student[8]) > 0:
            # record if the student spoke but was not flagged
            log_file.write(f"S{DELIMITER}")
            # record the student's name
            log_file.write(f"{student[0]} {student[1]}{DELIMITER}")
            # record the student's email
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
            # FN       LN           UO ID           EMAIL         PONETIC PRESENT SPOKEN  FLAGGED CC   PC   PF
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', 'True', 'True', 'True', '1', '5', '4'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', 'True', 'True', 'False', '1', '5', '4'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', 'False', 'True', 'False', '0', '5', '4'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', 'True', 'False', 'False', '0', '2', '1'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', 'False', 'False', 'False', '0', '5', '4']
            ]
    writeToSavedBootRoster(test_function_input)
    # this should produce: ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu',
    #    'nook', '848fsdfhkjhe8f9', 'True', '6', '5']

def _testWriteToLogFiles():
    # writeToLogFile tests
    test_function_input = [
            # FN       LN           UO ID           EMAIL         PONETIC PRESENT SPOKEN  FLAGGED CC   PC   PF
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', 'True', 'True', 'True', '1', '5', '4'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', 'True', 'True', 'False', '1', '5', '4'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', 'False', 'True', 'False', '0', '5', '4'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', 'True', 'False', 'False', '0', '2', '1'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', 'False', 'False', 'False', '0', '5', '4']
            ]
    writeToLogFile(test_function_input)
    # this should produce:
    # X	Nick Johnstone	nsj@uoregon.edu

def _testUpdatePerformanceFile():
    # update performance file test
    test_function_input = [
            # FN       LN           UO ID           EMAIL         PONETIC PRESENT SPOKEN  FLAGGED CC   PC   PF
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', 'True', 'True', 'True', '1', '5', '4'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', 'True', 'True', 'False', '1', '5', '4'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', 'False', 'True', 'False', '0', '5', '4'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', 'True', 'False', 'False', '0', '2', '1'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', 'False', 'False', 'False', '0', '5', '4']
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
        #_testUpdatePerformanceFile()
        #_testCheckValidRoster()

