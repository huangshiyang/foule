import threading
from field import Field
from location import Location
import math
import random
import time


class Person(threading.Thread):
    def __init__(self, field, display):
        threading.Thread.__init__(self)
        self.field = field
        self.display = display
        while True:
            location = Location(random.randint(0, self.field.getHeight() - 1),
                                random.randint(0, self.field.getWidth() - 1))
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
        i = 0
        while self.location.row > 1 or self.location.col > 1 or (self.location.row == 1 and self.location.col == 1):
            l = self.location
            self.field.acquire(l)
            location = self.decideWhereToGo()
            if location != None:
                self.field.clear(self.location)
                self.field.place(location)
                self.location = location
            i = i + 1
            self.field.release(l)
            time.sleep(0.001)
        with self.field.lock:
            if self.display:
                print(self.getName(), "#", i)
                self.field.print()
                print("")
        self.field.clear(self.location)

    def run(self):
        self.goToDoor()

    def print(self):
        self.field.print()
