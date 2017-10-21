import threading
from field import Field
from location import Location
import math
import random
import os


# threading.Thread
class Person:
    def __init__(self, field):
        # threading.Thread.__init__(self)
        self.field = field
        while True:
            location = Location(random.randint(1, self.field.getHeight()), random.randint(1, self.field.getWidth()))
            if (self.field.getLocation(location) == 0):
                self.field.place(location)
                self.location = location
                break

    def decideWhereToGo(self):
        freeLocations = self.field.getFreeAdjacentLocations(self.location)
        if freeLocations:
            distance = []
            for l in freeLocations:
                distance.append(math.sqrt(l.row * l.row + l.col * l.col))
            sortedDist = sorted(distance)
            normDist = math.sqrt(self.location.row * self.location.row + self.location.col * self.location.col)
            if normDist > sortedDist[0]:
                for i in range(len(distance)):
                    if sortedDist[0] == distance[i]:
                        return freeLocations[i]
        return None

    def goToDoor(self):
        while self.location.row > 1 or self.location.col > 1:
            location = self.decideWhereToGo()
            if location != None:
                self.field.clear(self.location)
                self.field.place(location)
                self.location = location

            # def run(self):
            # self.goToDoor()

    def print(self):
        self.field.print()
