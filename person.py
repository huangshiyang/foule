from location import Location
import random
import math

class Person:
    def __init__(self, field):
        self.field = field
        while True:
            location = Location(random.randint(0, self.field.getHeight() - 1),
                                random.randint(0, self.field.getWidth() - 1))
            if self.field.getLocation(location) == 0:
                self.location = location
                self.field.placePerson(self)
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