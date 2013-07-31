"""
Created on JuLY 15, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import DXFReader
import Panel
import pyglet
from pyglet.gl import *


panel = Panel.Panel
window = pyglet.window.Window(width=640, height=640, resizable=True)

fovAngle = 65
aspectRatio = float(window.width)/float(window.height)

scrollX = 0
scrollY = 0

xAngle = 0.0
yAngle = 0.0
zAngle = 0.0

textSize = -400
zTranslate = -20


"""
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=8,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
"""

text = "->"

html = '''
<font size=+1 color=#FF3030>
<b>Pyglet Basic OpenGL Demo</b>
</font><br/>
<font size=+2 color=#00FF60>
R = Reset<br/>
</font>
'''
"""
label = pyglet.text.HTMLLabel(html, #location,
                              width=window.width//200,
                              multiline=True, anchor_x='right', anchor_y='top')
                              """

label = pyglet.text.Label(text ,
                          font_name='Verdana',
                          font_size=14,
                          x=-window.width//2.75, y=-window.height//2.75)

def setup():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.2, 0.2, 0.2, 0.2)  #background color
    #glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    #glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


"""
on_resize is based on the example in the pyglet documentation here:
http://pyglet.org/doc/programming_guide/resizing_the_window.html
"""

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovAngle, width/float(height), .1, 2000)
    glMatrixMode(GL_MODELVIEW)

    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0,0.0, textSize) #set size of text
    label.draw() #draw the text

    glTranslatef(0.0, 0.0, -textSize + zTranslate)

    rotatePerspective()
    grid()
    wireFrame()


    return pyglet.event.EVENT_HANDLED

#@window.event
#def on_mouse_motion(x, y, dx, dy):
    #print("X = " + str(x) + " Y = " + str(y))

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    print("scroll = (" + str(scroll_x) + ", " + str(scroll_y) + ")")
    #glScalef(1.25, 1.25, 0.0)
    global xAngle, yAngle, zAngle
    if scroll_y > 0:
        xAngle += 2.0
        yAngle += 1.6
        zAngle += 1.2
    else:
        xAngle += -2.0
        yAngle += -1.6
        zAngle += -1.2

@window.event
def on_key_press(symbol, modifiers):
    global label
    global text
    print chr(symbol),
    text += chr(symbol)
    label = pyglet.text.Label(text,
                          font_name='Verdana',
                          font_size=14,
                          x=-window.width//2.75, y=-window.height//2.75)

@window.event
def on_mouse_press(x, y, button, modifiers):
    print("button pressed")


def wireFrame():
    glBegin(GL_LINES)

    for line in panel.lines:
        if line.layer == 'YELLOW':
            glColor3f(1.0, 1.0, 0.0)
        else:
            glColor3f(0.0, 0.0, 1.0)

        glVertex3f(*line.sPoint)
        glVertex3f(*line.ePoint)

    glEnd()

def grid():
    glBegin(GL_LINES)

    sizeX = 12
    sizeY = 12
    sizeZ = 12
    #print("GRID")
    #x-line
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-sizeX, 0.0, 0.0)
    glVertex3f(sizeX, 0.0, 0.0)
    #draw the x grid marks
    for mark in range(-sizeX, sizeX):
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(mark, -.25, 0.0)
        glVertex3f(mark, .25, 0.0)


    #y-line
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, sizeY, 0.0)
    glVertex3f(0.0, -sizeY, 0.0)
    #draw the y grid marks
    for mark in range(-sizeY, sizeY):
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(-.25, mark, 0.0)
        glVertex3f(.25, mark, 0.0)

    #z-line
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, sizeZ)
    glVertex3f(0.0, 0.0, -sizeZ)
    #draw the z grid marks
    for mark in range(-sizeZ, sizeZ):
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, -.25, mark)
        glVertex3f(0.0, .25, mark)

    glEnd()

def rotatePerspective():
    glRotatef(xAngle, 1.0, 0.0, 0.0)  #X-vector
    glRotatef(yAngle, 0.0, 1.0, 0.0)  #Y-vector
    glRotatef(zAngle, 0.0, 0.0, 1.0)  #Z-vector

"""
def centerPanel():
    gluOrtho2D(1.25 * -(panel.maxWidth())/2, 1.25 * panel.maxWidth()/2, 1.25 * -(panel.maxHeight())/2,
               1.25 * panel.maxHeight()/2, -10, 10)
    #glMatrixMode(GL_MODELVIEW)
    t = DisplayTools.center3D(panel, window._width, window._height)

    #print("X translate = " + str(t[0]))
    #print("Y translate = " + str(t[1]))
    #print("Panel Width = " + str(panel.maxWidth()) + " Panel Height = " + str(panel.maxHeight()))
    #print("Viewport Width = " + str(window._width) + " Viewport Height = " + str(window._height))

    glTranslatef(t[0], t[1], 0.0)
"""

def main():

    global panel
    panel = DXFReader.getPanel("test.dxf")
    #setup()
    pyglet.app.run()

main()


