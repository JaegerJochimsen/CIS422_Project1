from Classroom import Classroom
from InstructorInterface import InstructorInterface
from FileIO import *

data = [
"Jaeger",
"Mert",
"Nick",
"Kai",
"Steven",
"Atlas",
"Yavuz",
"Kerim"
]

def main():
    rosterStringList = readRoster()

    rosterStringList = False

    if not rosterStringList:

        rosterFileInputGUI = InstructorInterface(rosterStringList, None)
        newRosterFile = rosterFileInputGUI.getRosterFileInput()
        print(newRosterFile)
        return False

    ourClassroom = Classroom(rosterStringList, 4)

    ourGUI = InstructorInterface(ourClassroom.getDeck(), ourClassroom.moveToPost)
    ourGUI.startGUI()

    save = ourClassroom.mergeDecksToList()
    writeToSavedBootRoster(save)
    writeToLogFile(save)

main()
