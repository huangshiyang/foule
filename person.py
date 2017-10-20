import threading
from field import Field
from location import Location
import math


# threading.Thread
class Person:
    def __init__(self, field, location):
        # threading.Thread.__init__(self)
        self.field = field
        self.location = location

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
        location = self.decideWhereToGo()
        self.field.clear(location)
        self.field.place(location)

        # def run(self):
        # self.goToDoor()
