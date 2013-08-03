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

        commands = {'view': self.view, 'fold': self.fold, 'help': self.help}
        return commands.get(args[0], self.default)(args)


    def view(self, args):
        if len(args) != 2:
            return "too many arguments try \"<-help\""

        #if args[1] == "z":

        return "scroll mouse to rotate around " + args[1] + " axis"


    def fold(self, args):
        """
        Iterate through route lines prompting the user to enter an angle for each line.
        """
        # DisplayPanel3D.foldPanel("no angle yet")
        return "fold angle"


    def help(self, args):

        return "sorry no help yet:)"


    def default(self, args):
        return "\"" + args[0] + "\" is not a command try: \"<-help\""
