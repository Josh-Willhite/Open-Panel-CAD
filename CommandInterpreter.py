"""
Created on July 31, 2013

[Copyright (c) 2013 Josh Willhite]
Repository: https://github.com/Josh-Willhite/Open-Panel-CAD Email: jwillhite@gmail.com

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import math
import DisplayState
import DXFReader



class Interpreter:

    def __init__(self, state):
        self.state = state

    def parseCommand(self, command):
        args = command.split(' ')

        commands = {'open': self.open, 'layer': self.layer, 'rotateview': self.rotateview, 'view': self.view, 'translate': self.translate,'fold': self.fold, 'help': self.help}
        return commands.get(args[0], self.default)(args)

    def open(self, args):

        self.state.openedPanel = args[1]
        self.state.panel = DXFReader.getPanel(args[1])

        return "opened " + args[1]


    def translate(self, args):
        self.state.xTrans = float(args[1])
        self.state.yTrans = float(args[2])
        self.state.zTrans = float(args[3])
        return "translated"

    def view(self, args):
        if len(args) == 4:
            self.state.xRotAngle = float(args[1])
            self.state.yRotAngle = float(args[2])
            self.state.zRotAngle = float(args[3])
        elif len(args) == 2:
            if args[1] == 'top':
                self.state.xRotAngle = 0.0
                self.state.yRotAngle = 0.0
                self.state.zRotAngle = 0.0
            if args[1] == 'bottom':
                self.state.xRotAngle = 180.0
                self.state.yRotAngle = 0.0
                self.state.zRotAngle = 0.0
            if args[1] == 'front':
                self.state.xRotAngle = -90.0
                self.state.yRotAngle = 0.0
                self.state.zRotAngle = 0.0
            if args[1] == 'back':
                self.state.xRotAngle = -90.0
                self.state.yRotAngle = 0.0
                self.state.zRotAngle = 180.0
            if args[1] == 'right':
                self.state.xRotAngle = -90.0
                self.state.yRotAngle = 0.0
                self.state.zRotAngle = -90.0
            if args[1] == 'left':
                self.state.xRotAngle = -90.0
                self.state.yRotAngle = 0.0
                self.state.zRotAngle = 90.0
        else:
            return "usage:view xangle yangle zangle"

        return "(X angle, Y angle, Z angle) = (" + str(self.state.xRotAngle) + ", " + str(self.state.yRotAngle) + ", " + str(self.state.zRotAngle) + ")"

    # not using this method at the moment
    def rotateview(self, args):
        if len(args) != 2:
            return "too many arguments try \"<-help\""

        if args[1] == "z":
            self.state.axisOfRotation = "z"
        elif args[1] == "x":
            self.state.axisOfRotation = "x"
        elif args[1] == "y":
            self.state.axisOfRotation = "y"

        return "scroll mouse to rotate around " + args[1] + " axis"

    def layer(self, args):
        self.state.layer = args[1]
        return "showing " + args[1] + " layer"

    def fold(self, args):
        #need to modify this code to take into account selecting multiple route lines, need to somehow identify line
        #that is to be rotated about.
        foldLine = None
        #  find the route line to rotate other lines about
        for line in self.state.panel.lines:
            if line.selected and line.layer == 'YELLOW':
                if foldLine is None:
                    foldLine = line
                else:
                    return "Please select only ONE route line"

        if foldLine is None:
            return "Please select route line to fold"

        for line in self.state.panel.lines:
            if line.selected and line.layer == 'BLUE':
                line.rotate(foldLine, args[1])

        return "folded to " + args[1] + " degree angle"


    def help(self, args):

        return "commands: view, rotateview"

    def default(self, args):
        return "\"" + args[0] + "\" is not a command try: \"<-help\""