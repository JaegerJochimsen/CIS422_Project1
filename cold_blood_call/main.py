
from Classroom import Classroom
from InstructorInterface import InstructorInterface

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

    ourClassroom = Classroom(data,4)
    ourGUI = InstructorInterface(ourClassroom.getDeck(), ourClassroom.moveToPost)
    ourGUI.startGUI()

main()
