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


        # label1 = Label(self.root, text=f"{self.roster[0]}")
        # label1.pack(padx=5, pady=15, side=tk.LEFT)
        #
        # label2 = Label(self.root, text="asd2")
        # label2.pack(padx=5, pady=20, side=tk.LEFT)
        #
        # label3 = Label(self.root, text="asd2")
        # label3.pack(padx=5, pady=25, side=tk.LEFT)

        button = Button(self.root, text="click", command=self.buttonHit)
        button.pack(padx=5, pady=30, side=tk.LEFT)

        # self.nameLabels.append(button)

        # for index,name in enumerate(self.roster):
        #     self.nameLabels.append(Label(self.root, text=f"{name}").grid(row=0,column=index))
        #     print(self.nameLabels[index])

        # self.button = Button(self.root, text="click", command=self.buttonHit).grid(row=0, column=4)
        # for index,name in enumerate(self.roster):
        #     self.nameLabels.append(tk.Label(self.frame, text=f"{name}").grid(column=index, row=0))
        #
        # self.btn = tk.Button(self.frame, text="asd", command=self.buttonHit ).grid(column=5, row=0)


    def startGUI(self):
        # self.root.after(1000, self.checkUpdate)
        self.root.mainloop()

    def kill(self):
        self.running = 0
        # self.addRandom()
        # self.root.destroy()

    def chooseStudent(self):
        print("set")
        self.index = 1

    def checkUpdate(self):
        print("s")
        # while (1):

        if(self.index != -1):
            self.roster = self.callback(self.index)
            self.index =-1
        self.root.update_idletasks()
        self.root.after(1000,self.checkUpdate)

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
