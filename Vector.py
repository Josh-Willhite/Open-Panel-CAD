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

    def subtract(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def multiply(self, value):
        return Vector(self.x * value, self.y * value, self.z * value)

    def normal(self):  # normal direction of vector
        return Vector(self.x/self.length, self.y/self.length, self.z/self.length)

    def angle(self, vector):  # angle between two vectors
        return math.acos((self.dotProduct(vector))/(self.length * vector.length))



