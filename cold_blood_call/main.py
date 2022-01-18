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

    # rosterStringList = "This is an error please choose a roster file"

    ourGUI = InstructorInterface(rosterStringList, None)    # setting the input roster into GUI module

    exitProgram = 0
    trial = 0
    while not isinstance(rosterStringList,list):                      # if rosterStringList is a string and not a list, it is an error
        newRosterFile = ourGUI.getRosterFileInput(rosterStringList)   # asking the user for a roster file path

        if newRosterFile == "" or trial > 2:                    # if the path given is empty or the user tried 3 times, exit program
            ourGUI.kill()
            exitProgram = 1
            break

        rosterStringList = readRoster(newRosterFile)            # Check and try to read the new given roster file path

        trial += 1


    if exitProgram or trial > 2:                                #quit the program if no roster is given
        return

    ourClassroom = Classroom(rosterStringList, 4)
    print(ourClassroom.getDeck())
    ourGUI.insertDeck(ourClassroom.getDeck(), ourClassroom.moveToPost)                # call Classroom module to create students on-deck/predeck/postdeck with roster
    
    save = ourClassroom.mergeDecksToList()  # save the current student info on the post-deck/pre-deck/on-deck
    writeToSavedBootRoster(save)            # Write the Saved/Boot roster file
    writeToLogFile(save)                    # Write the log file
    updatePerforanceFile(save)              # Upadte the Performance file

if __name__ == "__main__":
    main()
