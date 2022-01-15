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

    while not rosterStringList:

        rosterFileInputGUI = InstructorInterface(rosterStringList, None)
        newRosterFile = rosterFileInputGUI.getRosterFileInput()
        rosterStringList = readRoster(newRosterFile)
        if rosterStringList:
            rosterFileInputGUI.kill()

    ourClassroom = Classroom(rosterStringList, 4)

    ourGUI = InstructorInterface(ourClassroom.getDeck(), ourClassroom.moveToPost)
    ourGUI.startGUI()

    save = ourClassroom.mergeDecksToList()
    writeToSavedBootRoster(save)
    writeToLogFile(save)

main()
