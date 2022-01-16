"""
    Created by Stephen Leveckis, 1/12/2022
    Creates self.window GUI for cold calling program

    Installs Requried:
        Tkinter: sudo apt-get install python3.6-tk
"""
import tkinter as tk
from tkinter import *

class InstructorInterface():
    def __init__(self, given, callback):
        self.win = tk.Tk()
        # All text starts as white by default
        self.text_colors = ["white", "white", "white", "white"]

        # Leftmost value is True (highlighted) by default
        self.highlight_list = [True, False, False, False]

        self.highlight_counter = 0

        # Key listeners as part of the Tkinter library, waits for key press
        self.win.bind('<Right>', self.rightArrowKey)
        self.win.bind('<Left>', self.leftArrowKey)

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

        # Instantiate name variables to read in from the "deck" data structure
        self.name1 = "Thomas Python"
        self.name2 = "Johnny Hammersticks"
        self.name3 = "Susan Walkway"
        self.name4 = "Theodore Crumpet"

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

        self.canvas.create_text(5,15, text=self.name1, fill = self.text_colors[0], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/4, 15, text=self.name2, fill = self.text_colors[1], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/2, 15, text=self.name3, fill = self.text_colors[2], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(((self.win_w*3) /4), 15, text=self.name4, fill = self.text_colors[3], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.pack(fill=BOTH, expand=True)
    

    """
        Deletes all old text objects and replaces them with updated ones based on the 
        text_colors list.
    """
    def displayText(self):
        self.canvas.delete("all")
        self.canvas.create_text(5,15, text=self.name1, fill = self.text_colors[0], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/4, 15, text=self.name2, fill = self.text_colors[1], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(self.win_w/2, 15, text=self.name3, fill = self.text_colors[2], font = ('Helvetica 15 bold'), anchor='w')
        self.canvas.create_text(((self.win_w*3) /4), 15, text=self.name4, fill = self.text_colors[3], font = ('Helvetica 15 bold'), anchor='w')

    """
    Increases highlight_counter with a bound that prevents it from
    increasing past 3.
    """
    def increaseCounter(self):
        #global highlight_counter
        if ((self.highlight_counter +1) > 3):
            self.highlight_counter = 3
        else:
            self.highlight_counter = self.highlight_counter + 1

    """
    Decreases highlight_counter with a bound that prevents it from
    decreasing past zero.
    """
    def decreaseCounter(self):
        #global highlight_counter
        if((self.highlight_counter -1) < 0):
            self.highlight_counter = 0 
        else:
            self.highlight_counter = self.highlight_counter - 1


    """

    """
    def leftArrowKey(self, event):
        #global highlight_counter
        # Set the boolean list to reflect which index
        # in the list we want to be highlighted 
        self.decreaseCounter()
        self.highlight_list[self.highlight_counter+1] = False
        self.highlight_list[self.highlight_counter] = True

        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.text_colors[i] = "red"
            else:
                self.text_colors[i] = "white"

        self.displayText()    

    """
        Current index starts at 0, the furthest left displayed name.
        Right arrow key press should highlight a name to the right of the current index.
        Appropriately, modify the highlight_list to be false at the current index, and
        True one index to the right.

        Also set the text_colors list in the same manner.

        Finally, create text objects to display the desired behavior:
        the initial index going from red to white, and the index to the right
        going from white to red

    """
    def rightArrowKey(self, event):
        #global highlight_counter
        self.increaseCounter()

        self.highlight_list[self.highlight_counter-1] = False
        self.highlight_list[self.highlight_counter] = True

        for i in range(len(self.highlight_list)):
            if (self.highlight_list[i] is True):
                self.text_colors[i] = "red"
            else:
                self.text_colors[i] = "white"

        self.displayText()

    # Let it rip
    def startGUI(self):
        self.win.mainloop()

