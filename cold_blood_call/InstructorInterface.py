from tkinter import *
import tkinter as tk
import random
from threading import Thread
import time


class InstructorInterface():
    def __init__(self, given, callback):
        self.root = Tk()
        # self.frame = Frame(self.root, padding=50)
        # self.frame.grid()
        self.root.grid()
        self.root.geometry("+1000+0")
        self.roster = given
        self.index = -1
        self.callback = callback
        self.deckSize = 4
        self.nameLabels = []

        y = 15
        for i in range(self.deckSize):
            label = Label(self.root,text=f"{self.roster[i]}")
            label.pack(padx=5, pady=y, side=tk.LEFT)
            y+=10
            self.nameLabels.append(label)

        button = Button(self.root, text="click", command=self.buttonHit)
        button.pack(padx=5, pady=30, side=tk.LEFT)



    def startGUI(self):
        self.root.mainloop()

    def kill(self):
        self.root.destroy()

    def buttonHit(self):

        print("asd")
        self.callback(1)
        # Wait for two seconds
        self.root.update_idletasks()
        for index,label in enumerate(self.nameLabels):
            label.config(text=f"{self.roster[index]}")
            label.update()

        print("roster")
        print(self.roster)
        time.sleep(0.1)
