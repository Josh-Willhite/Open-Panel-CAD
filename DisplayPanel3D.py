"""
Created on JuLY 15, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import DXFReader
import Panel
import DisplayTools
import pyglet
from pyglet.gl import *

panel = Panel.Panel
window = pyglet.window.Window(width=640, height=640, resizable=True)

#fovAngle = 45
aspectRatio = float(window._width)/float(window._height)

scrollX = 0
scrollY = 0

xAngle = 0.0
yAngle = 0.0
zAngle = 0.0


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
    #gluPerspective(fovAngle, 1, .1, 100)
    #gluOrtho2D(-(window._width)/2, window._width/2, -(window._height)/2, window._height/2, -1, 1)
    #gluOrtho2D(1.25 * -(panel.maxWidth())/2, 1.25 * panel.maxWidth()/2, 1.25 * -(panel.maxHeight())/2,
     #          1.25 * panel.maxHeight()/2, -10, 10)
    glMatrixMode(GL_MODELVIEW)

    #centerPanel()

    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #gluOrtho2D(-12, 12, -12, 12, -12, 12)

    centerPanel()
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
def on_mouse_press(x, y, button, modifiers):
    print("MOUSE PRESS")



def wireFrame():
    #centerPanel()

    glBegin(GL_LINES)
    panelLines = panel.getLines()

    for line in panelLines:
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
    print("GRID")
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


def main():
    global panel
    panel = DXFReader.getPanel("test.dxf")
    setup()
    pyglet.app.run()


main()


