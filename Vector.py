"""
Created on August 5, 2013

[Copyright (c) 2013 Josh Willhite]

This program is released under the MIT license. Please see the file COPYING in this distribution for the license terms.
"""
import math


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.length = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def dotProduct(self, vector):
        return vector.x * self.x + vector.y * self.y + vector.z * self.z

    def normal(self):
        return Vector(self.x/self.length, self.y/self.length, self.z/self.length)

