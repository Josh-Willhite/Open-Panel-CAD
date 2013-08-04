"""
Created on Jun 29, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import math


class Panel:
    def __init__(self):
        self.lines = []

    def addLine(self, line):
        self.lines.append(line)

    def getLines(self):
        return self.lines

    def maxWidth(self):
        max = 0.0
        for line in self.lines:
            curr = math.fabs(line.x0 - line.x1)
            if curr > max:
                max = curr
        return max

    def maxHeight(self):
        max = 0.0
        for line in self.lines:
            curr = math.fabs(line.y0 - line.y1)
            if curr > max:
                max = curr
        return max

    def xMin(self):
        min = self.lines[0].x0  #set the default min
        for line in self.lines:
            if min > line.x0:
                min = line.x0
            if min > line.x1:
                min = line.x1
        return min

    def yMin(self):
        min = self.lines[0].y0  #set the default min
        for line in self.lines:
            if min > line.y0:
                min = line.y0
            if min > line.y1:
                min = line.y1
        return min

    def zMax(self):
        max = self.lines[0].z0  #set the default min
        for line in self.lines:
            if max < line.z0:
                max = line.z0
            if max < line.z1:
                max = line.z1
        return max

    def centerXY(self):
        if self.xMin() == 0:
            xTranslate = -(self.maxWidth()/2)

        if self.xMin() > 0:
            xTranslate = -(self.xMin() + self.maxWidth()/2)

        if self.xMin() < 0:
            xTranslate = self.xMin() - self.maxWidth()/2

        if self.yMin() == 0:
            yTranslate = -(self.maxHeight()/2)

        if self.yMin() > 0:
            yTranslate = -(self.yMin() + self.maxHeight()/2)

        if self.yMin() < 0:
            yTranslate = self.yMin() - self.maxHeight()/2

        #print("X TRANSLATE = " + str(xTranslate))
        #print("Y TRANSLATE = " + str(yTranslate))

        for line in self.lines:
            line.x0 += xTranslate
            line.x1 += xTranslate
            line.y0 += yTranslate
            line.y1 += yTranslate
            line.sPoint = [line.x0, line.y0, line.z0]
            line.ePoint = [line.x1, line.y1, line.z1]
            #print("(" + str(line.x0) + ", " + str(line.y0) + ") (" + str(line.x1) + ", " + str(line.y1) + ")")


class Line:

    x0 = y0 = z0 = x1 = y1 = z1 = 0.0
    sPoint = [x0, y0, z0]
    ePoint = [x1, y1, z1]
    folded = False

    def __init__(self, layer, x0, y0, z0, x1, y1, z1):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.layer = layer
        self.sPoint = [x0, y0, z0]
        self.ePoint = [x1, y1, z1]

    def __str__(self):
        return ("\nLayer:%s (%.3f, %.3f, %.3f) (%.3f, %.3f, %.3f)\n"
                % (self.layer, self.x0, self.y0, self.z0, self.x1, self.y1,
                self.z1))

