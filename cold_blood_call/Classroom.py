import random
from Student import Student

class Classroom():
    """Classroom data structure class. Contains 3 lists that organize the cold
    call order of the classroom, and functions that manipulate these lists"""

    def __init__(self, roster, deckSize):
        """Takes in:
        roster: a list of lists of string that represent attributes of a student
        for the class roster
        deckSize: integer, to decide the size of deck.

        Initializes an empty postDeck, and calls the createDeck() method from
        itself to create the deck. The remaining students stay in preDeck."""

        # build the roster of Student objects from list of 
        self.roster = self._buildRoster(roster)

        # build the pre and post deck structures
        self.preDeck, self.postDeck = self._buildPrePostDeck(self.roster)

        

        self.deckSize = deckSize

        # create deck with respect to self.preDeck
        self.deck = self.createDeck()

    def _buildPrePostDeck(self, roster):
        preDeck = []
        postDeck = []
        for student in roster:
            # new student without spoken field
            # set spoken field, default is to set it to False (in the case of the initial roster)
            if student.getSpoken():
                postDeck.append(student)
            else:
                preDeck.append(student)

        return preDeck, postDeck


    def _buildRoster(self, studentList):
        roster = list()
        for student in studentList:
            spoken = False
            if student[6] == "True": spoken = True

            roster.append(Student(student[0], student[1], student[2],
                student[3], student[4], student[5], spoken, int(student[7]), int(student[8])))

        return roster


    def createDeck(self):
        """Uses random library to choose random students from preDeck and
        creates a temporary list for the deck.

        Returns: list[Student], deck that will
        be initialized as the self.deck"""

        gonnaBeDeck = []
        for i in range(self.deckSize):
            chosen = random.randint(0,len(self.preDeck)-1)
            gonnaBeDeck.append(self.preDeck[chosen])
            self.preDeck.remove(self.preDeck[chosen])
        # print("Deck Created")
        #print(gonnaBeDeck, self.preDeck)
        return gonnaBeDeck


    def moveToDeck(self):
        """Called by: moveToPost() from the same class

        Uses random to choose a student from preDeck and moves it to deck.
        If the preDeck is empty, calls the refresh method from the class to
        re-occupy it."""

        if (len(self.preDeck) == 0):
            self.refresh()
        nextIndex = random.randint(0,len(self.preDeck)-1)
        self.deck.append(self.preDeck[nextIndex])
        self.preDeck.remove(self.preDeck[nextIndex])


    def moveToPost(self,index,flag=0):
        """Takes in:
        index: integer, to know which student is chosen and will be moved to
        postDeck
        flag: boolean, will be true if the instructor set the flag.

        Called by: InstructorInterface, to communicate user choice and request
        new deck data.

        Moves the student from deck to postDeck, and calls the moveToDeck() from
        the class to fill the spot

        Returns: list[Student], which will be used by InstructorInterface"""

        self.postDeck.append(self.deck[index])
        self.deck[index].setSpoken(True)    # student has spoken, set that field
        self.deck[index].incrementContributions()

        self.deck.remove(self.deck[index])
        self.moveToDeck()

        #print("Modified")
        #print(self.deck,self.preDeck,self.postDeck)
        return self.deck


    def getDeck(self):
        """Returns the current deck: list[Student]."""
        return self.deck


    def refresh(self):
        """Called by: moveToDeck from the same class

        When a student is needed from preDeck but it is empty, this function is
        called. Moves every student in postDeck to preDeck and resets the spoken field."""

        for student in self.postDeck:
            # remove student from postDeck
            self.postDeck.remove(student)

            # preDeck students have a False val for spoken
            student.setSpoken(False)
            self.preDeck.append(student)


