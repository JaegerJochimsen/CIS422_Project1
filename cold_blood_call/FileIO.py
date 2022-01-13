import sys
from os import listdir


def _checkInitialBootStatus()->bool:
    if ".saved_boot.txt" in listdir():
        return False
    return True

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


if __name__ == "__main__":
    """Testing"""
    """
    rosty = readRoster()
    print(rosty)
    print("\n")
    test_roster = rosty.copy()
    test_roster[2][6] = "True"
    test_roster[1][6] = "True"
    print(test_roster)

    writeToSavedBootRoster(test_roster)
    """

