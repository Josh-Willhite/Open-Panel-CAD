'''
Created on Jun 25, 2013

@author: Josh Willhite
'''
from tkinter import *
from tkinter import ttk
import DXFReader

lines = DXFReader.getLines("test.dxf")

for line in lines:
    print(line)

root = Tk()
root.title("PANEL VIEWER")


#frame = ttk.Frame(root)

c = Canvas(root, height=800, width=800, bg="black")

for line in lines:
    if line.layer == "YELLOW":
        c.create_line(line.x0, line.y0, line.x1, line.y1, fill=line.layer, dash=(3,5))
    else:
        c.create_line(line.x0, line.y0, line.x1, line.y1, fill=line.layer)


c.pack()
root.mainloop()
