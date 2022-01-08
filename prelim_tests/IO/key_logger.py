import tkinter as tkr


def char(event):
    print(f'pressed: {repr(event.char)}')
    Log.append(event.char)
    print(Log)

def arrowL(event):
    print("left")
    Log.append("<-")
    print(Log)

def click(event):
    frame.focus_set()
    print(f'clicked at: {event.x}, {event.y}')
    Log.append((event.x, event.y))
    print(Log)

Log = []
master = tkr.Tk()
frame = tkr.Frame(master, height=500, width=500)
frame.bind("<Key>", char)
frame.bind('<Left>', arrowL)
frame.bind("<Button-1>", click)

frame.pack()

master.mainloop()



