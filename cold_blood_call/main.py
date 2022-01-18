"""
    File: main.py
    Description: The main function is a driver to start the software system
    with three modules. The sofeware system will read the roster from
    initial_roster.txt file or Saved/boot roster file to load student infomation.
    The system will output three files when program exit. (Log file, Saved/Boot file
    and perfermance file)
    Last update time: 1/17/2022
    Dependencies: Classroom, InstructorInterface, FileIO
    Credit: n/a
"""

# Import module
from Classroom import Classroom
from InstructorInterface import InstructorInterface
from FileIO import *

"""
    main(): the driver to control modules for the system
"""
def main():
    # loading Saved/Boot Roster, return a list of lists
    # readRoster() failed then return False
    rosterStringList = readRoster()

    # rosterStringList = "tits"

    while not isinstance(rosterStringList,list):                            # if rosterStringList is false, trying get roster from File Input
        rosterFileInputGUI = InstructorInterface(rosterStringList, None)    # setting the input roster into GUI module
        newRosterFile = rosterFileInputGUI.getRosterFileInput()             # getting the updated roster from GUI module
        rosterStringList = readRoster(newRosterFile)                        # renewing the roster in system
        # turn off the file input part
        rosterFileInputGUI.kill()

    ourClassroom = Classroom(rosterStringList, 4)                                   # call Classroom module to create students on-deck/predeck/postdeck with roster
    ourGUI = InstructorInterface(ourClassroom.getDeck(), ourClassroom.moveToPost)   # setting GUI with current roster and method for move student to post deck
    ourGUI.startGUI()                                                               # start the GUI module

    save = ourClassroom.mergeDecksToList()  # save the current student info on the post-deck/pre-deck/on-deck
    writeToSavedBootRoster(save)            # Write the Saved/Boot roster file
    writeToLogFile(save)                    # Write the log file
    updatePerforanceFile(save)              # Upadte the Performance file

if __name__ == "__main__":
    main()
