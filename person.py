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
            for i in range(len(distance)):
                if sortedDist[0] == distance[i]:
                    return freeLocations[i]
        return None

        # def goToDoor(self):
        # while location.row != 0:
        #    print()
        # todo

        # def run(self):
        # self.goToDoor()
