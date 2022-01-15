from tkinter import *
import tkinter as tk
from tkinter import filedialog
import random
from threading import Thread
import time


class InstructorInterface():
    def __init__(self, given, callback):
        self.root = Tk()
        if not given:
            self.rosterFile = filedialog.askopenfilename(initialdir="", title="Please choose your roster file")
            return

        # self.frame = Frame(self.root, padding=50)
        # self.frame.grid()
        self.root.grid()
        self.root.geometry("+1000+0")
        self.roster = given
        self.index = 0
        self.callback = callback
        self.deckSize = 4
        self.nameLabels = []

        y = 15
        for i in range(self.deckSize):
            if (i==self.index):
                label = Label(self.root,text=f"{self.roster[i]}",bg = "red")
            else:
                label = Label(self.root,text=f"{self.roster[i]}",bg = "green")
            label.pack(padx=5, pady=y, side=tk.LEFT)
            y+=10
            self.nameLabels.append(label)

        button = Button(self.root, text="click", command=self.buttonHit)
        button.pack(padx=5, pady=30, side=tk.LEFT)


    def startGUI(self):
        self.root.wm_attributes("-topmost", "true")
        self.root.lift()
        self.root.mainloop()

    def kill(self):
        self.root.destroy()

    def updateGUI(self):
        """Will be called by keybind callback functions to update the GUI after
        the changes. It stops the mainloop and takes care of the waiting functions.
         It recolorizes the labels and updates the name with the new deck"""
        self.root.update_idletasks()
        for index,label in enumerate(self.nameLabels):
            if (index == self.index):
                label.config(text=f"{self.roster[index]}", bg="red")
            else:
                label.config(text=f"{self.roster[index]}", bg="green")
            label.update()

        time.sleep(0.1)

    def getRosterFileInput(self):
        return self.rosterFile
