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
    rosterModified = checkRosterChange()
    (rosterStringList, isInitialBoot) = readRoster()

    exitProgram = 0
    # rosterStringList = "This is an error please choose a roster file"
    if not isinstance(rosterStringList,list):
        rosterGUI = InstructorInterface(rosterStringList)                   # Creating a GUI for roster file input

        while not isinstance(rosterStringList,list):                        # if rosterStringList is a string and not a list, it is an error
            newRosterFile = rosterGUI.getRosterFileInput(rosterStringList)  # asking the user for a roster file path

            if newRosterFile == "":                            # if the path given is empty or the user tried 3 times, exit program
                rosterGUI.killMain()
                exitProgram = 1
                break
            else:
                # save the file name and most recent time for it
                saveRosterInfo(newRosterFile)

            (rosterStringList, isInitialBoot) = readRoster(newRosterFile)   # Check and try to read the new given roster file path

            if isinstance(rosterStringList,list):                           #if the read is successful
                rosterGUI.changeMessage("Please Confirm the Student Roster, cancel to re-enter roster file")
                rosterGUI.createRosterConfirmWindow(rosterStringList)       #Show the roster window and ask the user to confirm or cancel
                rosterConfirmed = rosterGUI.getRosterConfirmationResult()   #if confirmed, 1 will be returned. Regardless of choice the GUI will be destroyed
                if rosterConfirmed:                                         #break roster input loop if confirmed
                    break
                else:                                                       #else reset the roster file
                    rosterStringList = "Please choose your roster file"
                    rosterGUI = InstructorInterface(rosterStringList)       #since the GUI was destroyed, make a new one and repeat the loop


    if exitProgram:                                #quit the program if no roster is given
        return

    # HERE IS WHERE THE ROSTER CHANGE GUI MESSAGE SHOULD GO TO AVOID VARIABLE UNDEFINED ERRORS

    ourClassroom = Classroom(rosterStringList, 4)   # call Classroom module to create students on-deck/predeck/postdeck with roster
    ourGUI = InstructorInterface(rosterStringList)  #Create the cold-call GUI
    ourGUI.insertDeck(ourClassroom.getDeck(),       #feed the GUI with the deck and needed classroom methods and start the program
                      ourClassroom.moveToPost,
                      ourClassroom.markAbsent)


    save = ourClassroom.mergeDecksToList()  # save the current student info on the post-deck/pre-deck/on-deck
    writeToSavedBootRoster(save)            # Write the Saved/Boot roster file
    writeToLogFile(save)                    # Write the log file
    updatePerforanceFile(save)              # Upadte the Performance file

if __name__ == "__main__":
    main()
