"""
    Created by Stephen Leveckis, 1/12/2022
    Creates window GUI for cold calling program

    Installs Requried:
        Tkinter: sudo apt-get install python3.6-tk
"""

# TODO: red text goes OVER white text such that it peeks out
# a little at the border of the red text. Looks a little gross. Fix!

import tkinter as tk
from tkinter import *

win = tk.Tk()
# All text starts as white by default
text_colors = ["white", "white", "white", "white"]

# Leftmost value is True (highlighted) by default
highlight_list = [True, False, False, False]

highlight_counter = 0

"""
    Deletes all old text objects and replaces them with updated ones based on the 
    text_colors list.
"""
def displayText():
    canvas.delete("all")
    canvas.create_text(5,15, text=name1, fill = text_colors[0], font = ('Helvetica 15 bold'), anchor='w')
    canvas.create_text(win_w/4, 15, text=name2, fill = text_colors[1], font = ('Helvetica 15 bold'), anchor='w')
    canvas.create_text(win_w/2, 15, text=name3, fill = text_colors[2], font = ('Helvetica 15 bold'), anchor='w')
    canvas.create_text(((win_w*3) /4), 15, text=name4, fill = text_colors[3], font = ('Helvetica 15 bold'), anchor='w')

"""
Increases highlight_counter with a bound that prevents it from
increasing past 3.
"""
def increaseCounter():
    global highlight_counter
    if ((highlight_counter +1) > 3):
        highlight_counter = 3
    else:
        highlight_counter = highlight_counter + 1

"""
Decreases highlight_counter with a bound that prevents it from
decreasing past zero.
"""
def decreaseCounter():
    global highlight_counter
    if((highlight_counter -1) < 0):
        highlight_counter = 0 
    else:
        highlight_counter = highlight_counter - 1


"""

"""
def leftArrowKey(event):
    global highlight_counter
    # Set the boolean list to reflect which index
    # in the list we want to be highlighted 
    decreaseCounter()
    highlight_list[highlight_counter+1] = False
    highlight_list[highlight_counter] = True

    for i in range(len(highlight_list)):
        if (highlight_list[i] is True):
            text_colors[i] = "red"
        else:
            text_colors[i] = "white"

    displayText()    
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
def rightArrowKey(event):
    global highlight_counter
    increaseCounter()

    highlight_list[highlight_counter-1] = False
    highlight_list[highlight_counter] = True

    for i in range(len(highlight_list)):
        if (highlight_list[i] is True):
            text_colors[i] = "red"
        else:
            text_colors[i] = "white"

    displayText()

    # Key listeners as part of the Tkinter library, waits for key press
win.bind('<Right>', rightArrowKey)
win.bind('<Left>', leftArrowKey)

# Gets native screen resolution width and height
screen_w = win.winfo_screenwidth()
screen_h = win.winfo_screenheight()

# 19 is a scalar modifier that happens to create a decent
# screen height for our win based on original native screen height
win_h = screen_h/22
win_w = screen_w 

# Make a string "widthxheight" to pass to geometry function
dimensions = "%dx%d" % (win_w, win_h)
# Sets the window size to these dimensions
win.geometry(dimensions)

# Instantiate name variables to read in from the "deck" data structure
name1 = "Thomas Python"
name2 = "Johnny Hammersticks"
name3 = "Susan Walkway"
name4 = "Theodore Crumpet"

# Canvas object
canvas = Canvas(win, width = win_w, height = win_h, bg = "black")

# Image object creation
myimg = PhotoImage(file='texture2.gif')
canvas.create_image(0, 0, image = myimg, anchor='nw')

"""
    Create 4 widgets, one for each displayed name.

    This process, creating 4 widgets must be done once initially, here,
    and then once for every keypress to display the updated text
    ie, which name is red now to show highlight)
"""

for i in range(len(highlight_list)):
    if (highlight_list[i] is True):
        text_colors[i] = "red"

canvas.create_text(5,15, text=name1, fill = text_colors[0], font = ('Helvetica 15 bold'), anchor='w')
canvas.create_text(win_w/4, 15, text=name2, fill = text_colors[1], font = ('Helvetica 15 bold'), anchor='w')
canvas.create_text(win_w/2, 15, text=name3, fill = text_colors[2], font = ('Helvetica 15 bold'), anchor='w')
canvas.create_text(((win_w*3) /4), 15, text=name4, fill = text_colors[3], font = ('Helvetica 15 bold'), anchor='w')

# No idea what fill and expand parameters are, look it up!
canvas.pack(fill=BOTH, expand=True)

"""
    win.mainloop() loops the tkinter functions,
    to create a constantly-updated graphics display
"""
win.mainloop()

