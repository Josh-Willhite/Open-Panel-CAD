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

class Panel:

    def __init__(self):
        self.lines = []

    def addLine(self, line):
        self.lines.append(line)

    def getLines(self):
        return self.lines

    def maxWidth(self):
        max = 0
        for line in self.lines:
            curr = math.fabs(line.x0 - line.x1)
            if curr > max:
                max = curr
        return max

    def maxHeight(self):
        max = 0
        for line in self.lines:
            curr = math.fabs(line.y0 - line.y1)
            if curr > max:
                max = curr
        return max

class Line:
    def __init__(self, layer, x0, y0, z0, x1, y1, z1):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.layer = layer

    def __str__(self):
        return ("\nLayer:%s (%.3f, %.3f, %.3f) (%.3f, %.3f, %.3f)\n"
                % (self.layer, self.x0, self.y0, self.z0, self.x1, self.y1,
                self.z1))

