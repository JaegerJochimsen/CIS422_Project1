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
    if not rosterStringList:
        print("CANNOT FIND ROSTER")
        return False
    ourClassroom = Classroom(rosterStringList, 4)

    ourGUI = InstructorInterface(ourClassroom.getDeck(), ourClassroom.moveToPost)
    ourGUI.startGUI()

    save = ourClassroom.mergeDecksToList()
    writeToSavedBootRoster(save)
    writeToLogFile(save)

main()
