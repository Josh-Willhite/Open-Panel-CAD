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
import math
import Vector

window = pyglet.window.Window(width=640, height=640, resizable=True)

mousePosition = None

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
    translate()
    wireFrame()
    if mousePosition is not None:
        mousePointer()
        lineSelect()

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
def on_mouse_motion(x, y, rx, ry):
    global mousePosition
    mousePosition = unProject(x, y)


def mousePointer():

    print(mousePosition)
    glPointSize(12.0)
    glEnable(GL_POINT_SMOOTH)
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.75, 0.75)

    glVertex3f(*mousePosition)

    glEnd()

"""
This method is inspired by the example program posted here:
https://sites.google.com/site/swinesmallpygletexamples/mouse-picking
"""
def unProject(x, y):
    x = 2 * (float(x) / window.width) - 1
    y = 2 * (float(y) / window.height) - 1

    tangent = math.tan(math.radians(st.fovAngleY) / 2)
    dx = st.aspectRatio * tangent * x
    dy = tangent * y
    dz = st.zTranslatePanel
    #[dx, dy, dz]/(math.sqrt(dx*dx + dy*dy + dz*dz))
    return [dx*40, dy*40, dz]


def lineSelect():
    #find the line that is closets to the current mouse position
    minDistance = None
    for line in st.panel.lines:
        if minDistance is None:
            minDistance = distanceFromPointToLine(mousePosition, line)
            closestLine = line
        else:
            if minDistance > distanceFromPointToLine(mousePosition, line):
                minDistance = distanceFromPointToLine(mousePosition, line)
                closestLine = line

    glLineWidth(8.0)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.75, 0.75)
    glVertex3f(*closestLine.sPoint)
    glVertex3f(*closestLine.ePoint)
    glEnd()


def distanceFromPointToLine(point, line):
    """
    from Wikipedia: http://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    distance = |(a - p) - ((a - p) dot  n * n)|
    where a is a point on the line, p is a point in space, and n is the normal direction of the line.
    """
    a = Vector.Vector(line.x0, line.y0, line.z0)  # start point of line
    p = Vector.Vector(point[0], point[1], st.zTranslatePanel)  # mousePointer

    lineVector = Vector.Vector(line.x1 - line.x0, line.y1 - line.y0, line.z1 - line.z0) # vector of line

    aMinusP = a.subtract(p)

    distance = aMinusP.dotProduct(lineVector.normal().multiply(aMinusP.dotProduct(lineVector.normal())))

    return distance


@window.event
def on_key_press(symbol, modifiers):
    global labelIn
    global labelOut
    #print(symbol)
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

def translate():
    glTranslatef(st.xTrans, st.yTrans, st.zTrans)
    #glRotate()


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


