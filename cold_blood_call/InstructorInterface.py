"""
    Created by Stephen Leveckis, 1/12/2022
    Creates self.window GUI for cold calling program

    Installs Requried:
        Tkinter: sudo apt-get install python3.6-tk
"""
"""
Create and allow interaction with a GUI window using tkinter.

Used By:
    main.py

Members:
    Member Name:        : Type          : Default Val           -> Description
    ------------------------------------------------------------------------------------------------------------------------------------------
    self.win            : tkinter       : Tk()                  -> the main tkinter window that will hold the names and accept input

    self.text_colors    : list[string]  : ["white", "white",    -> The color array defining the color of text for each student name on the window
                                           "white", "white"]

    self.deck           : list[Student] : deck(parameter)       -> a list of Student objects that show who are currently on deck

    self.moveToPost     : method        : moveToPost(parameter) -> a method given to the class on initialization, used to modify deck upon user input

    self.highlight_list : list[bool]    : [True, False,         -> A list of bools showing which label is indexed on the GUI.
                                           False, False]

Methods:

    Private:                                                                     Return:
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._buildRoster(self, roster : list[list[str]] )          |   ->  list[Student]
                                                                                |
    Usage:          self._buildRoster(roster)                                   |   ->  [Student(), Student(), ...]
                                                                                |
    Description:    Create a list of Student objects from the lists of lists of |
                    string representing student data                            |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._buildPrePostDeck(self, roster : list[list[Student]])  |   ->  list[Student] , list[Student]
                                                                                |
    Usage:          self._buildPrePostDeck(roster)                              |   ->  preDeck:[Student()] , postDeck:[Student()]
                                                                                |
    Description:    Create a tuple of Student lists, sorting the input roster   |
                    of Students based on their spoken fields. The first         |
                    list is the preDeck (all Student objects with spoken=False),|
                    the second is the postDeck (all Student objects with        |
                    spoken=True)                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self.createDeck(self)                                       |   ->  list[Student]
                                                                                |
    Usage:          self._createDeck(self)                                      |   ->  deck:list[Student]
                                                                                |
                                                                                |
    Description:    Create the deck of size self.deckSize by adding random      |
                    Student objects from self.preDeck to self.deck              |
    ----------------------------------------------------------------------------|-------------------------------------------------

    Public:                                                                      Return:
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self.moveToDeck(self)                                       |   ->  None
                                                                                |
    Usage:          instance.moveToDeck()                                       |
                                                                                |
    Description:    Move a random Student object from self.preDeck to           |
                    self.deck                                                   |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self.moveToPost(self, index:int, flag:bool = False)         |   ->  list[Student]
                                                                                |
    Usage:          instance.moveToPost(1, False)                               |   ->  updated deck:list[Student]
                                                                                |
    Description:    Move the Student object at index to the self.postDeck,      |
                    setting that Student's flagged field to flag                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self.getDeck(self)                                          |   ->  list[Student]
                                                                                |
    Usage:          instance.getDeck()                                          |   ->  deck:list[Student]
                                                                                |
    Description:    Return the current deck (self.deck)                         |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self.refresh(self)                                          |   ->  None
                                                                                |
    Usage:          self.refresh()                                              |   ->  None
                                                                                |
    Description:    Move all Students in the postDeck to the preDeck, resetting |
                    their spoken fields to be False.                            |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self.mergeDecksToList(self)                                 |   -> list[list[str]]
                                                                                |
    Usage:          instance.mergeDecksToList()                                 |   -> list[list[str]]
                                                                                |
    Description:    Add string representation of each Student object to a list, |
                    this is the current state of the class                      |
    ----------------------------------------------------------------------------|-------------------------------------------------
"""
import tkinter as tk
from tkinter import *
from tkinter import filedialog

class InstructorInterface():
    def __init__(self, deck, moveToPost):

        # The main GUI window object 
        self.win = tk.Tk()

        # All text starts as white by default
        self.text_colors = ["white", "white", "white", "white"]
        self.deck = deck
        self.moveToPost = moveToPost

        # Leftmost value is True (highlighted) by default
        self.highlight_list = [True, False, False, False]
        self.highlight_counter = 0

        # Key listeners as part of the Tkinter library, waits for key press
        self.win.bind('<Right>', self.rightArrowKey)
        self.win.bind('<Left>', self.leftArrowKey)
        self.win.bind('<r>', self.UpArrowKey)
        self.win.bind('<e>', self.DownArrowKey)

        # Gets native screen resolution width and height
        screen_w = self.win.winfo_screenwidth()
        screen_h = self.win.winfo_screenheight()

        # 19 is a scalar modifier that happens to create a decent
        # screen height for our self.win based on original native screen height
        self.win_h = screen_h/22
        self.win_w = screen_w

        # Make a string "widthxheight" to pass to geometry function
        dimensions = "%dx%d" % (self.win_w, self.win_h)
        # Sets the self.window size to these dimensions
        self.win.geometry(dimensions)

        # Canvas object
        self.canvas = Canvas(self.win, width = self.win_w, height = self.win_h, bg = "black")

        """
        Create 4 widgets, one for each displayed name.

        This process, creating 4 widgets must be done once initially, here,
        and then once for every keypress to display the updated text
        (done in the arrow key functions)
        """
        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.text_colors[i] = "red"

        self.canvas.create_text(5,15, text=self.deck[0], fill = self.text_colors[0], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/4, 15, text=self.deck[1], fill = self.text_colors[1], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/2, 15, text=self.deck[2], fill = self.text_colors[2], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(((self.win_w*3) /4), 15, text=self.deck[3], fill = self.text_colors[3], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.pack(fill=BOTH, expand=True)


    """
    Deletes all old text objects and replaces them with updated ones based on the
    text_colors list. This is called after every key press event to reflect which name should be highlighted.
    """
    def displayText(self):
        self.canvas.delete("all")
        self.canvas.create_text(5,15, text=self.deck[0], fill = self.text_colors[0], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/4, 15, text=self.deck[1], fill = self.text_colors[1], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/2, 15, text=self.deck[2], fill = self.text_colors[2], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(((self.win_w*3) /4), 15, text=self.deck[3], fill = self.text_colors[3], font = ('Helvetica 15 bold'), anchor='w')

    """
    Increases highlight_counter with a bound that prevents it from
    increasing past 3, the rightmost name on our Deck.
    """
    def increaseCounter(self):
        if ((self.highlight_counter +1) > 3):
            self.highlight_counter = 3
        else:
            self.highlight_counter = self.highlight_counter + 1

    """
    Decreases highlight_counter with a bound that prevents it from
    decreasing past zero, the leftmost name on our Deck.
    """
    def decreaseCounter(self):
        if((self.highlight_counter -1) < 0):
            self.highlight_counter = 0
        else:
            self.highlight_counter = self.highlight_counter - 1


    """
    Upon a <Left> Arrow Key press, updates highlight_counter and the corresponding data 
    structures to represent highligting the name to the left of the current highlighted name.
    """
    def leftArrowKey(self, event):
        # Set the boolean list to reflect which index
        # in the list we want to be highlighted
        self.decreaseCounter()
        self.highlight_list[self.highlight_counter+1] = False
        self.highlight_list[self.highlight_counter] = True

        # Update the text_colors list to reflect which name on Deck
        # should be red/highlighted
        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.text_colors[i] = "red"
            else:
                self.text_colors[i] = "white"

        # After updating the data structures, call the function
        # that will display the text accordingly
        self.displayText()

    """
    Upon a <Right> Arrow Key press, updates highlight_counter and the corresponding data 
    structures to represent highligting the name to the left of the current highlighted name.
    """
    def rightArrowKey(self, event):
        # Set the boolean list to reflect which index
        # in the list we want to be highlighted
        self.increaseCounter()
        self.highlight_list[self.highlight_counter-1] = False
        self.highlight_list[self.highlight_counter] = True

        # Update the text_colors list to reflect which name on Deck
        # should be red/highlighted
        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.text_colors[i] = "red"
            else:
                self.text_colors[i] = "white"

        # After updating the data structures, call the function
        # that will display the text accordingly
        self.displayText()


    """
    Removes the currently highlighted student from the Deck 
    """
    def UpArrowKey(self, event):
        # Moves the highlighted student to the post-deck,
        # which moves them off the Deck.
        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.moveToPost(i,True)
                break
        # Displays the text after modifying relevant data structures
        # (the removed student will no longer be shown on the Deck.
        self.displayText()

    """
    Removes the currently highlighted student from the Deck,
    and "flags" them (reflected in the output log file)
    for user purposes.
    """
    def DownArrowKey(self, event):
        # Moves the highlighted student to the post-Deck,
        # which moves them off the Deck.
        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.moveToPost(i)
                break
        # Displays the text after modifying relevant data structures
        # (the removed student will no longer be shown on the Deck.
        self.displayText()

    """
    Start the GUI itself (nothing is displayed without mainloop()), 
    and set window properties.
    The win.lift() function ensures our window is always displayed
    above other application GUIs on the user screen.
    """
    def startGUI(self):
        self.win.wm_attributes("-topmost", "true")
        self.win.lift()
        self.win.mainloop()

    """
    Opens a file explorer to input a roster of students if one
    has not been supplied yet by the user.
    """
    def getRosterFileInput(self):
        rosterFile = filedialog.askopenfilename(initialdir = "", title="Please choose your roster file")
        return rosterFile
