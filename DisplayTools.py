"""
Created on Jun 29, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import math


def scaleAndCenter(panel, canvasWidth, canvasHeight, size):
    #assumes panel is always going to be much smaller then canvas, check this later
    xDelta = math.fabs(panel.maxWidth() - canvasWidth)
    yDelta = math.fabs(panel.maxHeight() - canvasHeight)

    if xDelta > yDelta:
        scale =  size*canvasWidth/panel.maxWidth()
    else:
        scale =  size*canvasHeight/panel.maxHeight()

    xTranslate = (canvasWidth - scale * panel.maxWidth())/2
    yTranslate = (canvasHeight - scale * panel.maxHeight())/2

    return [scale, xTranslate, yTranslate]


# add tools for navigating "model space"

