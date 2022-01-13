import sys
from os import listdir


def checkInitialBootStatus()->bool:
    if ".saved_boot.txt" in listdir():
        return False
    return True

def readRoster()->list:
    """This function will return a list of lists"""
    if checkInitialBootStatus():
        roster = open("initial_roster.txt", "r")
    else:
        roster = open(".saved_boot.txt", "r")

    result = list()
    for line in roster:
        result.append(line.strip().split('\t'))

    roster.close()
    return result


def writeToSavedBootRoster(students:list)->None:
    new_roster = open(".saved_boot.txt", "w")
    for student in students:
        for i, attribute in enumerate(student):
            if i == 6:
                new_roster.write(attribute)
            else:
                new_roster.write(f"{attribute}\t")
        new_roster.write("\n")
    new_roster.close()

rosty = readRoster()

writeToSavedBootRoster(rosty)
