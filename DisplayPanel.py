'''
Created on Jun 25, 2013

Copyright (c) 2013 @author: Josh Willhite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from tkinter import *
#from tkinter import ttk
import DXFReader
import DisplayTools

panel = DXFReader.getPanel("test.dxf")

#print("Max Width = " + str(DisplayTools.maxWidth(lines)))
#print("Max Height = " + str(DisplayTools.maxHeight(lines)))


root = Tk()
root.title("PANEL VIEWER")


#frame = ttk.Frame(root)
canvasWidth = 800
canvasHeight = 800
c = Canvas(root, height=canvasHeight, width=canvasWidth, bg="grey")

f = DisplayTools.scaleFactor(panel, canvasWidth, canvasHeight, .75)

for line in panel.getLines():
    if line.layer == "YELLOW":
        c.create_line(f*line.x0, f*line.y0, f*line.x1, f*line.y1, fill=line.layer, dash=(3,5))
    else:
        c.create_line(f*line.x0, f*line.y0, f*line.x1, f*line.y1, fill=line.layer)



c.pack()
root.mainloop()
