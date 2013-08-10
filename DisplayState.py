"""
Created on August 2, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import Panel


class State:

    panel = Panel
    backGroundColor = [.2, .2, .2, .2]

    #gluperspective arguments
    fovAngleY = 0
    aspectRatio = 0
    zNear = 0
    zFar = 0

    xRotAngle = 0.0
    yRotAngle = 0.0
    zRotAngle = 0.0

    xTrans = 0.0
    yTrans = 0.0
    zTrans = 0.0

    viewVector = [0.0, 0.0, 0.0, 0.0]  # [angle, x, y, z]

    layer = "all"
    
    axisOfRotation = "z"

    zTranslateCommandPrompt = -400
    zTranslatePanel = -20

    commandIn = "<-"
    commandOut = "->"

    def __init__(self, panel, fovAngleY, aspectRatio, zNear, zFar):
        self.panel = panel
        self.fovAngleY = fovAngleY
        self.aspectRatio = aspectRatio
        self.zNear = zNear
        self.zFar = zFar


