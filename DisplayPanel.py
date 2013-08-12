"""
Created on Jun 25, 2013

[Copyright (c) 2013 Josh Willhite]
Repository: https://github.com/Josh-Willhite/Open-Panel-CAD Email: jwillhite@gmail.com

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
from Tkinter import *
#from tkinter import ttk
#from tkinter import filedialog


import DXFReader
import DisplayTools

fileName = ""

class MenuBar:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        mainMenu = Menu(root)
        self.fileMenu(mainMenu)
        root.config(menu=mainMenu)

    def fileMenu(self, mainMenu):
        fMenu = Menu(mainMenu, tearoff=0)
        mainMenu.add_cascade(menu=fMenu, label='File')
        fMenu.add_command(label='Open', command=self.openFile)
        fMenu.add_command(label='Quit', command=self.quit)

    def openFile(self):
        fileName = filedialog.askopenfilename(filetypes=[("Drawing Exchange Format", "*.dxf"),
                                                         ("Drawing Exchange Format", "*.DXF"), ("All Files", "*.*")])

        self.canvas.drawPanel(DXFReader.getPanel(fileName))

    def quit(self):
        self.root.destroy()


class CanvasWindow:
    height = 800
    width = 800
    bgColor = '#333333'

    def __init__(self, root):
        self.canvas = Canvas(root, height=self.height, width=self.width, bg=self.bgColor)
        self.canvas.pack()

    def drawPanel(self, panel):
        t = DisplayTools.scaleAndCenter(panel, self.width, self.height, .85)

        for line in panel.getLines():
            if line.layer == "YELLOW":
                self.canvas.create_line(t[0]*line.x0 + t[1], t[0]*line.y0 + t[2], t[0]*line.x1 + t[1], t[0]*line.y1 +
                                        t[2],fill=line.layer, dash=(18, 20), width='.5m')
            else:
                self.canvas.create_line(t[0]*line.x0 + t[1], t[0]*line.y0 + t[2], t[0]*line.x1 + t[1], t[0]*line.y1 +
                                        t[2], fill=line.layer, width='.25m')


def main():
    root = Tk()
    root.title("Open Panel CAD")
    canvas = CanvasWindow(root)
#    MenuBar(root, canvas)

    root.mainloop()

main()