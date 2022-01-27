"""
File: DataStream.py

Description: Contains functions that allows the system to interace with files
    in order to save/maintain/read data. (Also contains test for this module)
    The file will take interact with student data in two forms:

    1. Lists of lists where the inner lists contain string with data about each
    student.
    2. Files where each line contains tab or comma delimited data about the
    students.

    The primary job of this module is to read/convert data in the two forms in
    order to tranfer the data from short term memory during progam execution to
    longterm storage when the program is not in execution. The file also stores
    well formatted data in the form of .csv files for the user to be able to use
    Excel to read them.

Dependencies: None

Author(s): Nick Johnstone

Date Created: 1/11/2022

Dates Modified: 1/12/2022, 1/13/2022, 1/14/2022, 1/15/2022, 1/16/2022, 1/17/2022
       1/18/2022, 1/22/2022, 1/24/2022
"""

# import statments for python standard libraries
import sys
from os import listdir, getcwd, mkdir, path
from datetime import date, datetime
from operator import itemgetter
from re import search
from shutil import rmtree


# Delimiter represents how each field in the files are separated
DELIMITER = '\t'

################################################################################
def saveRosterInfo(rosterFile:str)->None:
    """
    Parameter:
        rosterFile  -   a string that represents a file name of a roster

    Called by:
        DataStream.py - readRoster()
        ColdCall.py - main()

    Calls:
        os  -   getcwd()

    Modifies:
        N/A

    Return:
        None

    Description:
        This function saves the roster meta data to a file named
        "roster_info.txt" in the .sysData directory such as file name, and last
        modification date.
    """

    # first check if the system data directory exists
    if ".sysData" not in listdir():
            # if not get the current working directory information
            cwd = getcwd()
            # create the path of the new data directory
            new_dir = cwd + "/.sysData"
            # create the data directory
            mkdir(new_dir)
    # open the file
    roster_info = open(".sysData/roster_info.txt", "w")
    # write the roster file name
    roster_info.write(f"{rosterFile}\n")
    # save the time that it was last modified
    upload_time = path.getmtime(rosterFile)
    # write the modification time to the file
    roster_info.write(f"{upload_time}\n")
    # close the file
    roster_info.close()
################################################################################

################################################################################
def resetSystem()->None:
    """
    Parameter:
        N/A

    Called by:
        ColdCall.py - main()

    Calls:
        shutil  -   rmtree()

    Modifies:
        N/A

    Return:
        None

    Description:
        Deletes the .sysData directory, in turn resetting the system.
    """
    # deletes the .sysData directory
    rmtree(".sysData/")


def checkRosterChange()->(str, bool) or (None, None):
    """
    Parameter:
        N/A

    Called by:
        DataStream.py - readRoster()
        ColdCall.py - main()

    Calls:
        os  -   getmtime()

    Modifies:
        N/A

    Return:
        tuple:
        string - The name of the roster file
        bool - True if the roster has changed, False if it has not.

    Description:
        Checks if the initial roster file has be edited and returns True if it
        has, returns False if it has not.
    """

    # check if the .sysData even exists
    if ".sysData" not in listdir():
        # if not return
        return (None, None)
    # check if the roster_info.txt exists
    elif "roster_info.txt" not in listdir(".sysData"):
        # if not return
        return (None, None)
    # open the roster_info.txt file
    roster_info = open(".sysData/roster_info.txt", "r")
    # initial a list that will hold information about the file
    roster_info_list = list()
    # loop through the file and grab the info, putting it in the list
    for line in roster_info:
        # add data to the list
        roster_info_list.append(line.strip())
    # check the time the roster was last modified
    check_time = path.getmtime(roster_info_list[0])
    # check if the roster was edited
    if float(check_time) == float(roster_info_list[1]):
        # if it was not modified return the file name and False
        return (roster_info_list[0], False)
    # if it was modified return the file name and True
    return (roster_info_list[0], True)
    # close file
    roster_info.close()
################################################################################


################################################################################
def _fixRoster(rosterFile: str)->list:
    """
    Parameter:
        rosterFile - string that is the name of the roster

    Called by:
        DataStream.py - readRoster()

    Calls:
        N/A

    Modifies:
        N/A

    Return:
        list of lists where each internal list holds data for a student

    Description:
        Updates the system roster if the initial roster was modified by the user.
    """

    # open the file saved roster
    saved_roster = open(".sysData/saved_boot.txt", "r")
    # open the initial roster
    initial_roster = open(rosterFile, "r")
    # create two lists that will hold the contents of both files
    saved_roster_list = list()
    initial_roster_list = list()
    # loop through the files
    for line in saved_roster:
        # add each line to the list
        saved_roster_list.append(line.strip().split(f"{DELIMITER}"))
    for line in initial_roster:
        # add each line to the list
        initial_roster_list.append(line.strip().split(f"{DELIMITER}"))
    # close the files
    saved_roster.close()
    initial_roster.close()
    # sort student data by last name
    saved_roster_sorted = sorted(saved_roster_list, key=itemgetter(1))
    initial_roster_sorted = sorted(initial_roster_list, key=itemgetter(1))
    # initialize counters to represent positions in each list
    i = 0
    j = 0
    # save the len of the initial roster
    init_saved_len = len(saved_roster_sorted)
    # create a list of additional fields that will be added to new students
    additional_fields = ["False", "0", "0", "0"]
    # loop through the initial roster
    for _ in range(len(initial_roster_sorted)):
        # if on the last element
        if j == init_saved_len:
            # if a phonetic was added
            if len(initial_roster_sorted[i]) == 5:
                # add a phonetic and the other student information
                saved_roster_sorted.append(initial_roster_sorted[i] + additional_fields)
            # if no phonetic
            elif len(initial_roster_sorted[i]) == 4:
                #  add other information only
                saved_roster_sorted.append(initial_roster_sorted[i] + ["None"] + additional_fields)
            # should not make it here unless roster is incorrect
            else:
                # error message invalid roster
                print("ERROR: invalid roster")
            # increment i
            i += 1
        # if student already appears in both, keep moving
        elif initial_roster_sorted[i][1] == saved_roster_sorted[j][1]:
            # if we have added or modified our phonetic code field AND
            # it is not the same as what we had saved
            if len(initial_roster_sorted[i]) == 5 and saved_roster_sorted[j][4] != initial_roster_sorted[i][4]:
                # update to be homogenous with initial_roster_sorted's phonetic
                saved_roster_sorted[j][4] = initial_roster_sorted[i][4]
            # increment both i and j
            i += 1
            j += 1
        # add a whole new student
        elif initial_roster_sorted[i][1] < saved_roster_sorted[j][1]:
            # if a phonetic was added
            if len(initial_roster_sorted[i]) == 5:
                # add a phonetic and the other student information
                saved_roster_sorted.append(initial_roster_sorted[i] + additional_fields)
            # if no phonetic
            elif len(initial_roster_sorted[i]) == 4:
                #  add other information only
                saved_roster_sorted.append(initial_roster_sorted[i] + ["None"] + additional_fields)
            # should not make it here unless roster is incorrect
            else:
                # error message invalid roster
                print("ERROR: invalid roster")
            # increment i
            i += 1
        # for future features the abilty the remove a student
        else:
            # remove the student
            saved_roster_sorted[j] = None
            # only increment j
            j += 1
    # resort the roster
    saved_roster_sorted = [element for element in saved_roster_sorted if element is not None]
    # sort the final roster
    new_roster = sorted(saved_roster_sorted, key=itemgetter(1))
    # return the resulting roster
    return new_roster
################################################################################


################################################################################
def _checkValidRoster(rosterFile:str)->str:
    """
    Parameter:
        rosterFile  -   a string that represents a file name of a roster

    Called by:
        DataStream.py - readRoster()

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
            # close file and return error message
            open_roster.close()
            return (f"Invalid student ID number on line: {i+1}")
        # regex check for email (4th element should always be email according to SRS)
        # refrenced pattern from:
        # https://www.tutorialspoint.com/checking-for-valid-email-address-using-regular-expressions-in-java
        if search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", student[3]) == None:
            # close file and return error message
            open_roster.close()
            return (f"Invalid email on line: {i+1}")

    # close roster
    open_roster.close()
    # will only reach here if roster is valid to return
    return "VALID"
################################################################################


################################################################################
def readRoster(rosterFile:str="initial_roster.txt")->(list, bool) or (str, bool):
    """
    Parameter:
        rosterFile  -   a string that represents a file name of a roster

    Called by:
        ColdCall.py - main()

    Calls:
        DataStream.py  -   _testCheckValidRoster()
        DataStream.py  -   checkRosterChange()
        DataStream.py  -   _fixRoster()
        DataStream.py  -   saveRosterInfo()

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
        This functions reads a roster file ir and splits up each student into a
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
            9. Previous Absences
        Each of these lists is returned in a main list that is passed to ColdCall.py
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
    # READ FROM THE .sysData/saved_boot.txt ON SUSEQUENT BOOTUPS
    if "saved_boot.txt" in listdir(".sysData/"):
        # assign the roster to the system's store data file
        roster = open(".sysData/saved_boot.txt", "r")
        # not the first bootup
        initial = False
        # store the name of the initial roster as well as a boolean
        # that represents if it has cha
        (roster_name, roster_changed) = checkRosterChange()
        # check if the roster has changed
        if roster_changed:
            # save the initial roster metadata in a file
            saveRosterInfo(roster_name)
            # created a variable that holds the new list from _fixRoster
            student_list = _fixRoster(roster_name)
            # return the student data and False because the roster was not
            # initial bootup
            return (student_list, False)
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
            # return the initial data and True because first bootup
            return (roster_status, True)
    # INITIAL CASE MOST OF THE TIME
    # if a roster with an alternate name is being used
    elif rosterFile != "initial_roster.txt":
        # roster_status stores the validity of the initial roster
        roster_status = _checkValidRoster(rosterFile)
        # if the initial roster is valid
        if roster_status == "VALID":
            # debug statement to help error checking
            #print("READING CUSTOM")
            # roster now contains the initial roster with a custom name
            roster = open(rosterFile, "r")
        # if the initial roster is not in a valid format return error message
        else:
            # return the error message and True because first bootup
            return (roster_status, True)
    # no roster is provided, return a message that prompts the user to input a file
    else:
        return ("Please provide an initial roster", True)

    ################################################################
    # Here the program begins to fill the a list with student data #
    ################################################################
    # initialize a list that will hold each student
    student_list = list()
    # parse through each line in the roster file
    for line in roster:
        # add a list split on the delimiter that holds data for the given student
        student_list.append(line.strip().split(f"{DELIMITER}"))
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
    # close roster file
    roster.close()
    # return the list sorted by last name
    sorted_student_list = sorted(student_list, key=itemgetter(1))
    return (sorted_student_list, initial)
################################################################################


################################################################################
def writeToSavedBootRoster(students:list)->None:
    """
    Parameter:
        students  -   a list of lists where each of the internal lists contain
                      data entries for the student (this argument is the return
                      value of toStrList() from Student.py)

    Called by:
        ColdCall.py - main()

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
        <flagged_count(including current session)<absences_count>><\n>

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
            new_roster.write(f"{str(int(student[11]) + 1)}\n")
        else:
            # if the student was present, do not increment absences
            new_roster.write(f"{student[11]}\n")
    # close file
    new_roster.close()
################################################################################


################################################################################
def writeToLogFile(students:list)->None:
    """
    Parameter:
        students  -   a list of lists where each of the internal lists contain
                      data entries for the student (this argument is the return
                      value of toStrList() from Student.py)

    Called by:
        ColdCall.py - main()

    Calls:
        datetime    -   now()

    Modifies:
        N/A

    Return:
        None
        (Produces a file, see desciption for details)

    Description:
        This function takes the list of lists produced by toStrList in Student.py
        and creates a file called "LogFile-<date time>.csv" that stores data
        pertaining to the session of the system that was just completed.
        This data includes, a list of students who spoke, a list of students,
        who were absent, and a list of students who were flagged.
        The file will look like the following:

        Log File for Cold Call Assist Program
                    2022/01/19:

        First,Name,Last,Name,Email,<Spoken/Flagged/Absent>
        First,Name,Last,Name,Email,<Spoken/Flagged/Absent>
        First,Name,Last,Name,Email,<Spoken/Flagged/Absent>
        First,Name,Last,Name,Email,<Spoken/Flagged/Absent>

        The purpose of this log file is to allow the user to keep a log of
        student performance for every given class session.
    """

    # check if the data directory already exists
    if "Data" not in listdir():
        # if not get the current working directory information
        cwd = getcwd()
        # create the path of the new data directory
        new_dir = cwd + "/Data"
        # create the data directory
        mkdir(new_dir)
    # create the logfile for the current session
    log_name = "LogFile-" + str(date.today()) + ".csv"
    log_file = open(f"Data/{log_name}", "w")
    # after opening the file, write the header
    log_file.write("Log File for Cold Call Assist Program\n")
    log_file.write(f"Date:, {str(date.today()).replace('-', '/')}\n")
    log_file.write(f"Student Name, Email, Spoken/Flagged/Absent\n")
    # parse through each student in the student list argument
    for student in students:
        # check if the student was absent
        if student[5] == "False":
            # record the student's name
            log_file.write(f"{student[0]} {student[1]}, ")
            # record the student's name
            log_file.write(f"{student[3]}, ")
            # record that they were absent
            log_file.write(f"A{DELIMITER}\n")
        # check if the student was flagged at all
        elif int(student[7]) > 0:
            # record the student's name
            log_file.write(f"{student[0]} {student[1]}, ")
            # record the student's name
            log_file.write(f"{student[3]}, ")
            # record that they were flagged
            log_file.write(f"X{DELIMITER}\n")
        # check if the student was spoken but not flagged
        elif int(student[8]) > 0:
            # record the student's name
            log_file.write(f"{student[0]} {student[1]}, ")
            # record the student's email
            log_file.write(f"{student[3]}, ")
            # record if the student spoke but was not flagged
            log_file.write(f"S{DELIMITER}\n")
    # close the file
    log_file.close()
################################################################################


def updatePerforanceFile(students:list)->None:
    """
    Parameter:
        students  -   a list of lists where each of the internal lists contain
                      data entries for the student (this argument is the return
                      value of toStrList() from Student.py)

    Called by:
        ColdCall.py - main()

    Calls:
        datetime  -   now()

    Modifies:
        N/A

    Return:
        None
        (Produces a file, see desciption for details)

    Description:
        This function takes the list of lists produced by toStrList in Student.py
        and updates/creates (on first run) a file called "PerformanceFile.csv"
        that stores cummulative data about student performance over the whole term
        This data includes, first and last names, id numbers, email addresses,
        total times called, total times flagged, absences, and a list of dates
        spoken for each student. The file is in csv format so it can be easily
        read by Microsoft Excel.
        The file is formatted as follows:

        Performance File for Cold Call Assist Program
        Date: <date>
        First Name, Last Name, UO ID, Email, Times Called, Times Flagged, Absences, List of Dates
        <student_data>,<student_data>,<student_data>,<student_data>,<student_data>,<student_data>
        <student_data>,<student_data>,<student_data>,<student_data>,<student_data>,<student_data>
        <student_data>,<student_data>,<student_data>,<student_data>,<student_data>,<student_data>
        <student_data>,<student_data>,<student_data>,<student_data>,<student_data>,<student_data>

        The purpose of this file is to track student performance throughout the term
    """

    # sort the list that is passed in so it lines up with the old performance_file order
    students_sorted = sorted(students, key=itemgetter(1))

    ##############################################################
    # This is the case when there is no current performance file #
    # This will only be trigger on initial bootup                #
    ##############################################################
    if "Performance-File.csv" not in listdir("Data"):
        # Open file
        performance_file = open("Data/Performance-File.csv", "w")
        # write header information to file
        performance_file.write("Performance File for Cold Call Assist Program\n")
        performance_file.write(f"Date:,{str(date.today()).replace('-', '/')}\n")
        performance_file.write("First Name,Last Name,UO ID,Email,")
        performance_file.write("Times Called,Times Flagged,Absences,")
        performance_file.write("List of Dates Spoken\n")
        # loop through passed in student information
        for student in students_sorted:
            # add first name
            performance_file.write(f"{student[0]},")
            # add last name
            performance_file.write(f"{student[1]},")
            # add id number
            performance_file.write(f"{student[2]},")
            # add email
            performance_file.write(f"{student[3]},") # add the email
            # add the contributions line (initial contributions)
            performance_file.write(f"{student[8]},")
            # add the number of times flagged for the first session
            performance_file.write(f"{student[7]},")
            # add 1 to absences if absent for first session
            if student[5] == "False":
                # 1 because they were absent
                performance_file.write(f"1,")
            else:
                # 0 because they were present
                performance_file.write(f"0,")
            # if the student spoke at all
            if int(student[8]) > 0:
                performance_file.write(f"{str(date.today()).replace('-', '/')}") # add the date
                # if not spoken
            else:
                # add a dash for the day
                performance_file.write("-") # add a dash
            # write a newline for formatting
            performance_file.write("\n")
        # Close file and return None
        performance_file.close()
        return None

    ###############################################################
    # This is the case  where the performance file already exists #
    # This will be the case for all sessions other than the first #
    ###############################################################
    # when the file exists but needs to be updated after the session
    performance_file = open("Data/Performance-File.csv", "r")
    # skip the head and collumns lines
    performance_file.readline()
    performance_file.readline()
    performance_file.readline()
    # Initialize a list that will hold data from the previous file
    prev_file = list()
    # loops through the student data
    for student in performance_file:
        # put each student in the old performance_file into a list and split each
        # of their fields into a a seperate element of the internal list
        prev_file.append(student.strip().split(","))
    # close the file
    performance_file.close()
    # sort the list by last name so it lines up with the data that is passed in
    prev_file_sorted = sorted(prev_file, key=itemgetter(1))

    # go through each student from the current session and check if they spoke
    # if they did add the date to the list that will be written to the performance_file
    # this includes incrementing the contributions field, as well as the flag field (when applicable)
    # j will represent the old performance_file increment location
    j = 0
    for i in range(len(students_sorted)):
        # if not a new student
        if students_sorted[i][1] == prev_file_sorted[j][1]:
            # if the student spoke
            if int(students_sorted[i][8]) > 0:
                # add the number of times the student contributed in the current session to the total
                prev_file_sorted[j][4] = str((int(students_sorted[i][9]) + int(students_sorted[i][8])))
                # add the date to the list of dates because the student spoke
                prev_file_sorted[j].append(str(date.today()).replace('-', '/'))
            # the student did not speak
            else:
                # add a dash because they did not speak
                prev_file_sorted[j].append("-")
            # if the student was flagged
            if int(students_sorted[i][7]) > 0:
                # increment flagged
                prev_file_sorted[j][5] = str(int(prev_file_sorted[j][5]) + int(students_sorted[i][7]))
            # if the student was absent
            if students_sorted[i][5] == "False":
                # increment absent
                prev_file_sorted[j][6] = str(int(prev_file_sorted[j][6]) + 1)
            # increment j because not a new student
            j += 1
        # if there is a new student
        else:
            # create a new list that will represent the student in the performance file
            new_student = [students_sorted[i][0], students_sorted[i][1],
                    students_sorted[i][2], students_sorted[i][3],
                    students_sorted[i][8], students_sorted[i][7]]
            # add 1 to absences if absent for first session
            if students_sorted[i][5] == "False":
                # 1 because they were absent
                new_student.append("1")
            else:
                # 0 because they were present
                new_student.append("0")
            # if the student spoke at all
            if int(students_sorted[i][8]) > 0:
                new_student.append(f"{str(date.today()).replace('-', '/')}") # add the date
            # the student did not speak
            else:
                # add a dash because they did not speak
                new_student.append("-")
            # add the new student to the list
            prev_file_sorted.append(new_student)

    #################################################
    # Now the system has updated data and is ready  #
    # to write to the performance file              #
    #################################################
    # create a new file, overwriting the old one
    performance_file = open("Data/Performance-File.csv", "w")
    # write header information to file
    performance_file.write("Performance File for Cold Call Assist Program\n")
    performance_file.write(f"Date:,{str(date.today()).replace('-', '/')}\n")
    performance_file.write("First Name,Last Name,UO ID,Email,")
    performance_file.write("Times Called,Times Flagged,Absences,")
    performance_file.write("List of Dates Spoken\n")
    # resort the list based on last name
    prev_file_sorted = sorted(prev_file_sorted, key=itemgetter(1))
    # loop through each student
    for student in prev_file_sorted:
        # loop through the data for each student
        for i, item in enumerate(student):
            # if the last field
            if i == len(student) - 1:
                # write to the file with no camma at the end
                performance_file.write(f"{item}")
            # when not the last field
            else:
                # write to the file with camma at the end
                performance_file.write(f"{item},")
        # write new line for Excel file formatting
        performance_file.write("\n")
    # close the file
    performance_file.close()
    # return a None value because return value not used
    return None
################################################################################



################################################################################
#                       BEGINING OF TEST CASE SECTION                          #
################################################################################

# MAKE SURE TO RUN `mkdir Data .sysData` TO BUILD DATA DIRECTORY WHEN TESTING

def _testReadRoster():
    # readRoster tests
    roster = readRoster()
    print(roster)

def _testWriteToSavedBootRoster():
    # writeToSavedBootRoster
    test_function_input = [
            # FN       LN           UO ID           EMAIL         PONETIC PRESENT SPOKEN   FC CC   PC   PF   AC
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', 'True', 'True', '4', '1', '5', '4', '0'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', 'True', 'True', '2', '1', '5', '4', '0'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', 'False', 'True', '2', '0', '5', '4', '0'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', 'True', 'False', '1', '0', '2', '1', '0'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', 'False', 'False', '2', '0', '5', '4', '0']
            ]
    writeToSavedBootRoster(test_function_input)
    # this should produce: ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu',
    #    'nook', '848fsdfhkjhe8f9', 'True', '6', '5']

def _testWriteToLogFiles():
    # writeToLogFile tests
    test_function_input = [
            # FN       LN           UO ID           EMAIL         PONETIC PRESENT SPOKEN   FC CC   PC   PF   AC
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', 'True', 'True', '4', '1', '5', '4', '0'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', 'True', 'True', '2', '1', '5', '4', '0'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', 'False', 'True', '2', '0', '5', '4', '0'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', 'True', 'False', '1', '0', '2', '1', '0'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', 'False', 'False', '2', '0', '5', '4', '0']
            ]
    writeToLogFile(test_function_input)
    # this should produce:
    # A valid LogFile

def _testUpdatePerformanceFile():
    test_function_input = [
            # FN       LN           UO ID           EMAIL         PONETIC PRESENT SPOKEN   FC CC   PC   PF   AC
            ['Nick', 'Johnstone', '951******', 'nsj@uoregon.edu', 'nook', 'True', 'True', '4', '1', '5', '4', '0'],
            ['Jaeger', 'Jochimsen', '951******', 'jaegerj@uoregon.edu', 'jeeeee', 'True', 'True', '2', '1', '5', '4', '0'],
            ['Kai', 'Xiong', '951******', 'kxiong@uoregon.edu', 'ki', 'False', 'True', '2', '0', '5', '4', '0'],
            ['Mert', 'Yapucuoglu', '951******', 'merty@uoregon.edu', 'mart', 'True', 'False', '1', '0', '2', '1', '0'],
            ['Stephen', 'Levekis', '951******', 'slevecki@uoregon.edu', 'steve', 'False', 'False', '2', '0', '5', '4', '0']
            ]
    # update performance file test
    updatePerforanceFile(test_function_input)

def _testCheckValidRoster():
    valid_bool = _checkValidRoster("initial_roster.txt")
    print(valid_bool)


if __name__ == "__main__":
    """Testing"""
    if not __debug__:
        #_testReadRoster()
        #_testWriteToSavedBootRoster()
        _testWriteToLogFiles()
        #_testUpdatePerformanceFile()
        #_testCheckValidRoster()

