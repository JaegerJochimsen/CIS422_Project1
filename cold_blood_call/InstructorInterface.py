"""
    Created by Stephen Leveckis, Mert Yapucuoglu 1/12/2022
    Creates self.window GUI for cold calling program

    Installs Requried:
        Tkinter: sudo apt-get install python3.6-tk

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

    self.roster         : list[Student] : None                  -> a list of Student that will be shown on initial file load for review

    self.moveToPost     : method        : moveToPost(parameter) -> a method given to the class on initialization, used to modify deck upon user input

    self.highlight_list : list[bool]    : [True, False,         -> A list of bools showing which label is indexed on the GUI.
                                           False, False]


Methods:

    Private:                                                                     Return:
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._displayText(self)                                     |   ->  None
                                                                                |
    Usage:          self.<direction>ArrowKey(self,event)                        |
                                                                                |
    Description:    Delete all the name labels on the current window and        |
                    recreate them with the updated colors and names             |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._increaseCounter(self)                                 |   ->  None
                                                                                |
    Usage:          self._leftArrowKey(self, event)                             |
                                                                                |
    Description:    Increases the highlight counter that indicates which name   |
                    is being currently selected                                 |
                                                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._decreaseCounter(self)                                 |   ->  None
                                                                                |
    Usage:          self._rightArrowKey(self, event)                            |
                                                                                |
    Description:    Decreases the highlight counter that indicates which name   |
                    is being currently selected                                 |
                                                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._leftArrowKey(self, event)                             |   ->  None
                                                                                |
    Usage:          self.win.bind(<Left>)                                       |
                                                                                |
    Description:    Upon user left arrow input, calls self._decreaseCounter()   |
                    to change the highlighted index, changes the highlight_list |
                    with the new index and calls self._displayText() to refresh |
                    the GUI window.                                             |
                                                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._rightArrowKey(self, event)                            |   ->  None
                                                                                |
    Usage:          self.win.bind(<Right>)                                      |
                                                                                |
    Description:    Upon user right arrow input, calls self._increaseCounter()  |
                    to change the highlighted index, changes the highlight_list |
                    with the new index and calls self._displayText() to refresh |
                    the GUI window.                                             |
                                                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._UpArrowKey(self, event)                               |   ->  None
                                                                                |
    Usage:          self.win.bind(<r>)                                          |
                                                                                |
    Description:    Upon user r key input, finds the highlighed index and calls |
                    self.moveToPost(index) which is a method passed on by init  |
                    from the main, which also imported it from the Classroom.py |
                    in order to move the selected student from deck to postdeck |
                    because he/she has been cold called. Also sets up the flag. |
                    for the selected student.                                   |
                                                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._DownArrowKey(self, event)                             |   ->  None
                                                                                |
    Usage:          self.win.bind(<e>)                                          |
                                                                                |
    Description:    Upon user e key input, finds the highlighed index and calls |
                    self.moveToPost(index) which is a method passed on by init  |
                    from the main, which also imported it from the Classroom.py |
                    in order to move the selected student from deck to postdeck |
                    because  he/she has been cold called.                       |
                                                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------

    Public:                                                                      Return:
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self._startGUI(self)                                        |   ->  None
                                                                                |
    Usage:          main() in main.py                                           |
                                                                                |
    Description:    Called by self.insertDeck() when a valid roster is found.   |
                    Sets the GUI window to the top and foreground, and starts   |
                    the tkinter mainloop for the GUI to function.               |
                                                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self.getRosterFileInput(self, errorMessage)                 |   ->  string  - An absolute file path given by
                                                                                |                 the user
    Usage:          main() in main.py                                           |
                                                                                |
    Description:    This is called by main when there is no valid roster file.  |
                    Takes an errorMessage and shows it on the GUI. Pops up a    |
                    file input screen and lets the user choose a roster file.   |
                    Sets the GUI window to the top and foreground, and starts   |
                    the tkinter mainloop for the GUI to function.               |
                                                                                |
    ----------------------------------------------------------------------------|-------------------------------------------------
    Declaration:    self.insertDeck(self,deck, moveToPost)                      |   ->  None
                                                                                |
    Usage:          main() in main.py                                           |
                                                                                |
    Description:    This is called by main to feed the GUI with the student     |
                    deck. It also takes in the moveToPost function of the       |
                    classroom class and saves it for future use for cold call.  |
                    It then calls self._displayText() to update the window with |
                    the student names, and then calls self._startGUI() to start |
                    the GUI mainloop.                                           |
                                                                                |
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
        self.roster = None
        self.moveToPost = moveToPost

        # Leftmost value is True (highlighted) by default
        self.highlight_list = [True, False, False, False]
        self.highlight_counter = 0

        # Key listeners as part of the Tkinter library, waits for key press
        self.win.bind('<Right>', self._rightArrowKey)
        self.win.bind('<Left>', self._leftArrowKey)
        self.win.bind('<r>', self._UpArrowKey)
        self.win.bind('<e>', self._DownArrowKey)

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

        if not isinstance(self.deck,list):
            self.canvas.create_text(5,15, text=self.deck, fill = "white", font = ('Helvetica 18 bold'), anchor='w')
            self.canvas.pack(fill=BOTH, expand=True)
        else:
            self.canvas.create_text(5,15, text=self.deck[0], fill = self.text_colors[0], font = ('Helvetica 15 bold'), anchor='w')
            self.canvas.create_text(self.win_w/4, 15, text=self.deck[1], fill = self.text_colors[1], font = ('Helvetica 15 bold'), anchor='w')
            self.canvas.create_text(self.win_w/2, 15, text=self.deck[2], fill = self.text_colors[2], font = ('Helvetica 15 bold'), anchor='w')
            self.canvas.create_text(((self.win_w*3) /4), 15, text=self.deck[3], fill = self.text_colors[3], font = ('Helvetica 15 bold'), anchor='w')
            self.canvas.pack(fill=BOTH, expand=True)


    """
    Deletes all old text objects and replaces them with updated ones based on the
    text_colors list. This is called after every key press event to reflect which name should be highlighted.
    """
    def _displayText(self):
        self.canvas.delete("all")
        self.canvas.create_text(5,15, text=self.deck[0], fill = self.text_colors[0], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/4, 15, text=self.deck[1], fill = self.text_colors[1], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/2, 15, text=self.deck[2], fill = self.text_colors[2], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(((self.win_w*3) /4), 15, text=self.deck[3], fill = self.text_colors[3], font = ('Helvetica 15 bold'), anchor='w')

    """
    Increases highlight_counter with a bound that prevents it from
    increasing past 3, the rightmost name on our Deck.
    """
    def _increaseCounter(self):
        if ((self.highlight_counter +1) > 3):
            self.highlight_counter = 3
        else:
            self.highlight_counter = self.highlight_counter + 1

    """
    Decreases highlight_counter with a bound that prevents it from
    decreasing past zero, the leftmost name on our Deck.
    """
    def _decreaseCounter(self):
        if((self.highlight_counter -1) < 0):
            self.highlight_counter = 0
        else:
            self.highlight_counter = self.highlight_counter - 1


    """
    Upon a <Left> Arrow Key press, updates highlight_counter and the corresponding data
    structures to represent highligting the name to the left of the current highlighted name.
    """
    def _leftArrowKey(self, event):
        # Set the boolean list to reflect which index
        # in the list we want to be highlighted
        self._decreaseCounter()
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
        self._displayText()

    """
    Upon a <Right> Arrow Key press, updates highlight_counter and the corresponding data
    structures to represent highligting the name to the left of the current highlighted name.
    """
    def _rightArrowKey(self, event):
        # Set the boolean list to reflect which index
        # in the list we want to be highlighted
        self._increaseCounter()
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
        self._displayText()


    """
    Removes the currently highlighted student from the Deck
    """
    def _UpArrowKey(self, event):
        # Moves the highlighted student to the post-deck,
        # which moves them off the Deck.
        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.moveToPost(i,True)
                break
        # Displays the text after modifying relevant data structures
        # (the removed student will no longer be shown on the Deck.
        # print("yeah")
        self._displayText()

    """
    Removes the currently highlighted student from the Deck,
    and "flags" them (reflected in the output log file)
    for user purposes.
    """
    def _DownArrowKey(self, event):
        # Moves the highlighted student to the post-Deck,
        # which moves them off the Deck.
        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.moveToPost(i)
                break
        # Displays the text after modifying relevant data structures
        # (the removed student will no longer be shown on the Deck.
        self._displayText()

    """
    Start the GUI itself (nothing is displayed without mainloop()),
    and set window properties.
    The win.lift() function ensures our window is always displayed
    above other application GUIs on the user screen.
    """
    def _startGUI(self):
        self.win.wm_attributes("-topmost", "true")
        self.win.lift()
        self.win.mainloop()

    """
    Opens a file explorer to input a roster file if one
    has not been supplied yet by the user. Shows the error message
    provided by errorMessage parameter on the screen.
    """
    def getRosterFileInput(self, errorMessage):
        self.canvas.delete("all")                                                                                  #Clear the canvas GUI
        self.canvas.create_text(5,15, text=errorMessage, fill = "white", font = ('Helvetica 18 bold'), anchor='w') #create a text with the errorMessage
        self.canvas.pack(fill=BOTH, expand=True)                                                                   #add the errormessage to the window
        rosterFile = filedialog.askopenfilename(initialdir = "", title="Please choose your roster file")           #Take file path input from a pop-up window
        return rosterFile                                                                                          #return the path

    """
    Takes a deck parameter and saves  it to the self.deck to be used as a roster.
    Tkaes a moveToPost parameters method that will be called to move students
    out of the deck. Refreshes the GUI window with the provided deck names with
    self._displayText(). And starts the GUI functionality with self._startGUI()
    """
    def insertDeck(self, deck, moveToPost, roster):
        self.deck = deck
        self.moveToPost = moveToPost
        self.roster = roster
        self._displayText()
        self._startGUI()

    """
    Closes the GUI.
    """
    def kill(self):
        self.win.destroy()
