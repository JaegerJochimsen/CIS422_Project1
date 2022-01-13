import sys
from os import listdir, getcwd, mkdir
from datetime import date


def _checkInitialBootStatus()->bool:
    if ".saved_boot.txt" in listdir():
        return False
    return True

def _checkIfFileDir()->bool:
    if "MetaData" in listdir():
        return True
    return False

def readRoster()->list:
    """This function will return a list of lists"""
    initial = _checkInitialBootStatus()
    if initial:
        roster = open("initial_roster.txt", "r")
    else:
        roster = open(".saved_boot.txt", "r")
        print("READING THIS")

    student_list = list()
    for line in roster:
        student_list.append(line.strip().split('\t'))

    if initial:
        for student in student_list:
            student.append("False")

    roster.close()
    return student_list


def writeToSavedBootRoster(students:list)->None:
    new_roster = open(".saved_boot.txt", "w")
    for student in students:
        for i in range(7):
            if i == 6:
                new_roster.write(student[i])
            else:
                new_roster.write(f"{student[i]}\t")
        new_roster.write("\n")
    new_roster.close()


def _strBoolToPrint(bl:str)->str:
    if bl == "True":
        return "Yes"
    elif bl == "False":
        return "No"
    else:
        return None


def writeToLogFile(students:list)->None:
    dir_exists = _checkIfFileDir()
    if not dir_exists:
        cwd = getcwd()
        new_dir = cwd + "/MetaData"
        mkdir(new_dir)

    log_name = "LogFile-" + str(date.today())
    log_file = open(f"MetaData/{log_name}", "w")
    log_file.write(f"Log File for {str(date.today())}:\n")

    log_file.write(f"-----------------------------------------------------\n")

    for student in students:
        for i, attribute in enumerate(student):
            if i == 0:
                log_file.write(f"First Name: {attribute}\n")

            elif i == 1:
                log_file.write(f"Last Name: {attribute}\n")

            elif i == 2:
                log_file.write(f"UO ID: {attribute}\n")

            elif i == 3:
                log_file.write(f"Email: {attribute}\n")

            elif i == 4:
                log_file.write(f"Phonetic: {attribute}\n")

            elif i == 5:
                log_file.write(f"Reveal Code: {attribute}\n")

            elif i == 6:
                log_file.write(f"Spoke This Session: {_strBoolToPrint(attribute)}\n")

            elif i == 7:
                log_file.write(f"Flagged: {_strBoolToPrint(attribute)}\n")

            elif i == 8:
                log_file.write(f"Number of Contributions: {attribute}\n")

        log_file.write("----------------------------------------------------\n")

    log_file.close()




if __name__ == "__main__":
    """Testing"""

    """
    # readRoster tests
    rosty = readRoster()
    print(rosty)
    print("\n")
    test_roster = rosty.copy()
    test_roster[2][6] = "True"
    test_roster[1][6] = "True"
    print(test_roster)

    writeToSavedBootRoster(test_roster)
    """

    """
    # writeToLogFile tests
    log_test_input = [["Nick", "Johnstone", "951******", "nsj@gmail.com", "nook",
            "848fsdfhkjhe8f9", "False", "False", "0"]]
    writeToLogFile(log_test_input)
    """
