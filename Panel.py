"""
Created on Jun 29, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import math
from Vector import Vector


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

"""
    def fold(self, startPt, endPt, angle):
        for line in self.lines:
            #if this line starts or ends at the hinge line [check to see if lines intersect]
            #and it's between 90 and 270 degrees
                #move
"""


class Line:

    x0 = y0 = z0 = x1 = y1 = z1 = 0.0
    sPoint = [x0, y0, z0]
    ePoint = [x1, y1, z1]
    selected = False

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

    def isPointOnLine(self, pt):
        xInRange = False
        yInRange = False
        # check to make sure x is between x0 and x1
        if self.x0 < self.x1:
            if self.x0 <= pt[0] <= self.x1:
                xInRange = True
        else:
            if self.x1 <= pt[0] <= self.x0:
                xInRange = True

        # check to make sure y is between y0 and y1
        if self.y0 < self.y1:
            if self.y0 <= pt[1] <= self.y1:
                yInRange = True
        else:
            if self.y1 <= pt[1] <= self.y0:
                yInRange = True

        if xInRange and yInRange:
            return True
        else:
            return False

    def equal(self, line):
        if self.x0 == line.x0 and self.x1 == line.x1 and self.y0 == line.y0 and self.y1 == line.y1 and self.z0 == line.z0 and self.z1 == line.z1:
            return True

        return False

    def rotate(self, routeLine, angle):
        # (1) translate/rotate route line to align with z-axis(perform same manipulations to line that is being rotated
        # (2) perform the rotation
        # (3) un-translate/rotate the point

        # get vector normal to route line

        #xAxisNormal = Vector(1, 0, 0)
        #yAxisNormal = Vector(0, 1, 0)
        zAxisNormal = Vector(0, 0, 1)

        pointA = Vector(self.x0, self.y0, self.z0)  # point to be rotated
        pointB = Vector(self.x1, self.y1, self.z1)  # point to be rotated

        routeA = Vector(routeLine.x0, routeLine.y0, routeLine.z0)
        routeB = Vector(routeLine.x1, routeLine.y1, routeLine.z1)

        routeDirection = routeB.subtract(routeA).normal()  # direction of line to be rotated about

        #xAngle = routeDirection.angle(xAxisNormal)
        #yAngle = routeDirection.angle(yAxisNormal)
        zAngle = routeDirection.angle(zAxisNormal)  # angle of line to be rotated about w/respect to z-axis


 #       if zAngle != 0:


        pointA = pointA.subtract(routeA)  # translate to origin
        pointAx = pointA.x * math.cos(zAngle) - pointA.y * math.sin(zAngle)  # rotate to align w/z-axis
        pointAy = pointA.y * math.cos(zAngle) - pointA.x * math.sin(zAngle)






    def __str__(self):
        return ("\nLayer:%s (%.3f, %.3f, %.3f) (%.3f, %.3f, %.3f)\n"
                % (self.layer, self.x0, self.y0, self.z0, self.x1, self.y1,
                self.z1))

