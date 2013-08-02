"""
Created on July 31, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import math


def parseCommand(command):
    args = command.split(' ')

    commands = {'view': view, 'fold': fold, 'help': help}
    return commands.get(args[0], default)(args)


def view(args):
    if len(args) != 2:
        return "too many arguments try \"<-help\""
    return "scroll mouse to rotate around " + args[1] + " axis"


def fold(args):

    return "fold angle"


def help(args):
    return "sorry no help yet:)"


def default(args):
    return "\"" + args[0] + "\" is not a command try: \"<-help\""
