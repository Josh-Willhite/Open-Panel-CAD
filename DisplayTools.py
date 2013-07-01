'''
Created on Jun 29, 2013

Copyright (c) 2013 @author: Josh Willhite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import math

def scaleAndCenter(panel, canvasWidth, canvasHeight, size):
    #assumes panel is always going to be much smaller then canvas, add checking later
    xDelta = math.fabs(panel.maxWidth() - canvasWidth)
    yDelta = math.fabs(panel.maxHeight() - canvasHeight)

    if xDelta > yDelta:
        scale =  size*canvasWidth/panel.maxWidth()
    else:
        scale =  size*canvasHeight/panel.maxHeight()

    xTranslate = (canvasWidth - scale * panel.maxWidth())/2
    yTranslate = (canvasHeight - scale * panel.maxHeight())/2

    return [scale, xTranslate, yTranslate]


