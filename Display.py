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
from Vector import Vector

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
       # mousePointer()
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
    #print("MOUSE POSITION: " + str(mousePosition[0]) + " " + str(mousePosition[1]))

@window.event
def on_mouse_press(x, y, button, modifiers):
    for line in st.panel.lines:
        if line.equal(closestLine):
            if line.selected:
                line.selected = False
            else:
                line.selected = True

def mousePointer():

    #print(mousePosition)
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

    #gluUnProject() # figure out how to fill this...
    x = 2 * (float(x) / window.width) - 1
    y = 2 * (float(y) / window.height) - 1

    #print("x = " + str(x) + " y = " + str(y))

    tangent = math.tan(math.radians(st.fovAngleY) / 2)
    dx = st.aspectRatio * tangent * x
    dy = tangent * y
    dz = 0.0
    #[dx, dy, dz]/(math.sqrt(dx*dx + dy*dy + dz*dz))
    #print("dx = " + str(dx*20) + " dy = " + str(dy*20))
    #print("MOUSE POSITION: " + str(dx*40) + " " + str(dy*40))
    return [dx*math.fabs(st.zTranslatePanel), dy*math.fabs(st.zTranslatePanel), dz]


def lineSelect():
    #find the line that is closest to the current mouse position
    global closestLine
    minDistance = None

    for line in st.panel.lines:
        if line.layer.lower() == st.layer or  st.layer == 'all':
            if minDistance is None:
                minDistance = distanceFromPointToLine(line)
                closestLine = line
            else:
                if minDistance > distanceFromPointToLine(line):
                    minDistance = distanceFromPointToLine(line)
                    closestLine = line
    #print(minDistance)
    glLineWidth(8.0)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.75, 0.75)  # cyan
    glVertex3f(*closestLine.sPoint)
    glVertex3f(*closestLine.ePoint)
    glEnd()


def distanceFromPointToLine(line):
    """
    from Wikipedia: http://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    distance = |(a - p) - ((a - p) dot  n * n)|
    where a is a point on the line, p is a point in space, and n is the normal direction of the line.
    """
    a = Vector(line.x0, line.y0, line.z0)  # start point of line (this can be any point on the line)
    p = Vector(mousePosition[0], mousePosition[1], mousePosition[2])  # vector pointing to current mouse location


    n = Vector(line.x1 - line.x0, line.y1 - line.y0, line.z1 - line.z0).normal() # unit vector along direction of line

    aMinusP = a.subtract(p)

    dirNorm = aMinusP.subtract(n.multiply(aMinusP.dotProduct(n))) # this is the direction normal to the line
    disNorm = dirNorm.length # this is the distance normal to the line

    startPoint = Vector(line.x0, line.y0, line.z0)
    endPoint = Vector(line.x1, line.y1, line.z1)
    mousePoint = Vector(mousePosition[0], mousePosition[1], mousePosition[2])

    endVector = mousePoint.subtract(endPoint)
    #print("Distance End = " + str(distanceEnd))

    startVector = mousePoint.subtract(startPoint)
    #print("Distance Start = " + str(distanceStart))

    distanceEnd = endVector.length
    distanceStart = startVector.length
    
    #check to see if the normal line falls outside of the line we're measuring to
    normPoint = [dirNorm.x + mousePoint.x, dirNorm.y + mousePoint.y]
    if line.isPointOnLine(normPoint):
        short = 'norm'
        distance = disNorm
    elif distanceEnd <= distanceStart:
        short = 'end'
        distance = distanceEnd
    else:
        short = 'start'
        distance = distanceStart

    #print("NORMDIST = " + str(disNorm) + " START/END = " + str(distanceEnd) + " " + str(distanceStart))


    #print("ANGLE = " + str(angle))
    """
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)  # black

    if short == 'start':
        print("NORMSTART = " + "(" + str(dirNorm.x) + ", " + str(dirNorm.y) + ")")
        print("START = " + "(" + str(startPoint.x) + ", " + str(startPoint.y) + ")")
        print("MOUSE = " + "(" + str(mousePoint.x) + ", " + str(mousePoint.y) + ")")
        glVertex3f(mousePoint.x, mousePoint.y, 0.0)
        glVertex3f(startPoint.x, startPoint.y, 0.0)
    if short == 'end':
        print("NORMEND = " + "(" + str(dirNorm.x) + ", " + str(dirNorm.y) + ")")
        glVertex3f(mousePoint.x, mousePoint.y, 0.0)
        glVertex3f(endPoint.x, endPoint.y, 0.0)
    if short == 'norm':
        glVertex3f(mousePoint.x, mousePoint.y, 0.0)
        glVertex3f(dirNorm.x + mousePoint.x, dirNorm.y + mousePoint.y, 0.0)

    glEnd()
    """

    return distance


@window.event
def on_key_press(symbol, modifiers):
    global labelIn
    global labelOut
    #print(symbol)
    if 96 <= symbol <= 122 or 32 <= symbol <= 90:  # numbers letters or symbols
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
        if line.selected:
            glColor3f(0.0, 0.75, 0.75)

        if line.layer.lower() == st.layer or  st.layer == 'all':
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


