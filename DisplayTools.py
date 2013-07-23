"""
Created on Jun 29, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import math


def scaleAndCenter(panel, canvasWidth, canvasHeight, size):
    #assumes panel is always going to be much smaller then canvas, check this later
    assert panel.maxWidth() < canvasWidth , "panel is larger then canvas"
    assert panel.maxHeight() < canvasHeight, "panel is larger then canvas"

    xDelta = math.fabs(panel.maxWidth() - canvasWidth)
    yDelta = math.fabs(panel.maxHeight() - canvasHeight)

    if xDelta > yDelta:
        scale =  size*canvasWidth/panel.maxWidth()
    else:
        scale =  size*canvasHeight/panel.maxHeight()

    xTranslate = (canvasWidth - scale * panel.maxWidth())/2
    yTranslate = (canvasHeight - scale * panel.maxHeight())/2

    return [scale, xTranslate, yTranslate]

def center3D(panel, width, height):
    if panel.xMin() == 0:
        xTranslate = -(panel.maxWidth()/2)

    if panel.xMin() > 0:
        xTranslate = -(panel.xMin() + panel.maxWidth()/2)

    if panel.xMin() < 0:
        xTranslate = panel.xMin() - panel.maxWidth()/2

    if panel.yMin() == 0:
        yTranslate = -(panel.maxHeight()/2)

    if panel.yMin() > 0:
        yTranslate = -(panel.yMin() + panel.maxHeight()/2)

    if panel.yMin() < 0:
        yTranslate = panel.yMin() - panel.maxHeight()/2

    return [xTranslate, yTranslate]

# add tools for navigating "model space"

