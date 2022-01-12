import random

class Classroom():
    def __init__(self,roster, deckSize):
        self.roster = roster
        self.preDeck = roster
        self.postDeck = []
        self.deckSize = deckSize
        self.deck = self.createDeck()

    def createDeck(self):
        gonnaBeDeck = []
        for i in range(self.deckSize):
            chosen = random.randint(0,len(self.preDeck)-1)
            gonnaBeDeck.append(self.preDeck[chosen])
            self.preDeck.remove(self.preDeck[chosen])
        print("Deck Created")
        print(gonnaBeDeck, self.preDeck)
        return gonnaBeDeck


    def moveToDeck(self):
        if (len(self.preDeck) == 0):
            self.refresh()
        nextIndex = random.randint(0,len(self.preDeck)-1)
        self.deck.append(self.preDeck[nextIndex])
        self.preDeck.remove(self.preDeck[nextIndex])

    def moveToPost(self,index): #may change the name to something better
        self.postDeck.append(self.deck[index])
        self.deck.remove(self.deck[index])
        self.moveToDeck()
        print("Modified")
        print(self.deck,self.preDeck,self.postDeck)
        return self.deck

    def getDeck(self):
        return self.deck

    def refresh(self):
        for student in self.postDeck:
            self.preDeck.append(student)
            self.postDeck.remove(student)
