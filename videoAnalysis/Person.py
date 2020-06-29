from random import randint
import time

class Person:
    def __init__(self, id, xi, yi, maxAge):
        self.id = id
        self.x = xi
        self.y = yi
        self.age = 0
        self.maxAge = maxAge

    def getId(self):
        return self.id
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getMaxAge(self):
        return self.maxAge
    def updateCoords(self, xn, yn):
        self.age = 0
        self.x = xn
        self.y = yn
    def ageOneFrame(self):
        self.age += 1
        
