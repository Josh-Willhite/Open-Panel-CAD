"""
Created on JuLY 15, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import DXFReader
import CommandInterpreter
import DisplayState
import pyglet
from pyglet.gl import *

window = pyglet.window.Window(width=640, height=640, resizable=True)


def setup():
    glShadeModel(GL_SMOOTH)
    glClearColor(*st.backGroundColor)  # background color
    #glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    #glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


"""
#on_resize is based on the example in the pyglet documentation here:
#http://pyglet.org/doc/programming_guide/resizing_the_window.html
"""
@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(st.fovAngleY, st.aspectRatio, st.zNear, st.zFar)

    glMatrixMode(GL_MODELVIEW)

    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    commandPrompt()

    glTranslatef(0.0, 0.0, st.zTranslatePanel-st.zTranslateCommandPrompt)

    rotatePerspective()
    grid()
    wireFrame()

    return pyglet.event.EVENT_HANDLED


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    #print("scroll = (" + str(scroll_x) + ", " + str(scroll_y) + ")")

    if scroll_y > 0:
        if st.axisOfRotation == "z":
            st.xRotAngle = -45
            st.yRotAngle = 0
            st.zRotAngle += 1
        elif st.axisOfRotation == "x":
            st.xRotAngle += 1
            st.yRotAngle = -45
            st.zRotAngle = 0
        elif st.axisOfRotation == "y":
            st.xRotAngle = -45
            st.yRotAngle += 1
            st.zRotAngle = 0
    else:
        if st.axisOfRotation == "z":
            st.xRotAngle = -45
            st.yRotAngle = 0
            st.zRotAngle += -1
        elif st.axisOfRotation == "x":
            st.xRotAngle += -1
            st.yRotAngle = -45
            st.zRotAngle = 0
        elif st.axisOfRotation == "y":
            st.xRotAngle = -45
            st.yRotAngle += -1
            st.zRotAngle = 0

@window.event
def on_key_press(symbol, modifiers):
    global labelIn
    global labelOut
    print(symbol)
    if 96 <= symbol <= 122 or 32 <= symbol <= 63:  # numbers letters or symbols
        st.commandIn += chr(symbol)

    if symbol == 65293:  # enter
        st.commandOut = "->"
        st.commandOut += cL.parseCommand(st.commandIn[2:])
        st.commandIn = "<-"

    if symbol == 65288 and len(st.commandIn) > 2:  # backspace
        st.commandIn = st.commandIn[:-1]

    labelIn = pyglet.text.Label(st.commandIn, font_name='Verdana', font_size=14, x=-window.width//2.75,
                                y=-window.height//2.75 + 20)
    labelOut = pyglet.text.Label(st.commandOut, font_name='Verdana', font_size=14, x=-window.width//2.75,
                                y=-window.height//2.75)


def commandPrompt():
    glTranslatef(0.0,0.0, st.zTranslateCommandPrompt)  # set size of text
    labelIn.draw()  # command prompt
    labelOut.draw()

def wireFrame():
    glLineWidth(1.0)
    glBegin(GL_LINES)

    for line in st.panel.lines:
        if line.layer == 'YELLOW':
            glColor3f(1.0, 1.0, 0.0)
        else:
            glColor3f(0.0, 0.0, 1.0)

        glVertex3f(*line.sPoint)
        glVertex3f(*line.ePoint)

    glEnd()


def grid():
    glLineWidth(4.0)
    glBegin(GL_LINES)


    sizeX = 12
    sizeY = 12
    sizeZ = 12

    #print("GRID")
    #x-line
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(sizeX, 0.0, 0.0)
    #draw the x grid marks
    for mark in range(sizeX):
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(mark, -.25, 0.0)
        glVertex3f(mark, .25, 0.0)

    #y-line
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, sizeY, 0.0)
    #draw the y grid marks
    for mark in range(sizeY):
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(-.25, mark, 0.0)
        glVertex3f(.25, mark, 0.0)

    #z-line
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, sizeZ)
    #draw the z grid marks
    for mark in range(sizeZ):
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, -.25, mark)
        glVertex3f(0.0, .25, mark)

    glEnd()


def rotatePerspective():
    #glRotatef(st.xRotAngle, 1.0, 0.0, 0.0)  # X-vector
    #glRotatef(st.yRotAngle, 0.0, 1.0, 0.0)  # Y-vector
    #glRotatef(st.zRotAngle, 0.0, 0.0, 1.0)  # Z-vector
    glRotatef(*st.viewVector)



def main():
    global st
    global cL
    global labelIn
    global labelOut

    panel = DXFReader.getPanel("test.dxf")
    st = DisplayState.State(panel, 65, float(window.width)/float(window.height), .1, 2000)
    cL = CommandInterpreter.Interpreter(st)

    labelIn = pyglet.text.Label(st.commandIn, font_name='Verdana', font_size=14, x=-window.width//2.75,
                                y=-window.height//2.75 + 20)
    labelOut = pyglet.text.Label(st.commandOut, font_name='Verdana', font_size=14, x=-window.width//2.75,
                                y=-window.height//2.75)
    setup()
    pyglet.app.run()

main()


