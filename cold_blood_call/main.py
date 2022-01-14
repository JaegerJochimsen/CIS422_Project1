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
    #print(len(rosterStringList))
    #print(rosterStringList[0])
    ourClassroom = Classroom(rosterStringList, 4)
    #for student in test:
    #    print(student.getFirst())

    ourGUI = InstructorInterface(ourClassroom.getDeck(), ourClassroom.moveToPost)
    ourGUI.startGUI()

    save = ourClassroom.mergeDecksToList()
    writeToSavedBootRoster(save)

main()
