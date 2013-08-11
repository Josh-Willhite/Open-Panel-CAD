"""
Created on July 31, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import math
import DisplayState


class Interpreter:

    def __init__(self, state):
        self.state = state

    def parseCommand(self, command):
        args = command.split(' ')

        commands = {'layer': self.layer, 'rotateview': self.rotateview, 'view': self.view, 'translate': self.translate,'fold': self.fold, 'help': self.help}
        return commands.get(args[0], self.default)(args)

    def translate(self, args):
        self.state.xTrans = float(args[1])
        self.state.yTrans = float(args[2])
        self.state.zTrans = float(args[3])
        return "translated"

    def view(self, args):
        print(args[1], args[2], args[3], args[4])
        self.state.viewVector = [float(args[1]), float(args[2]), float(args[3]), float(args[4])]
        return "new view!"

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