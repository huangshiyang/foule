import threading
from location import Location
import math
import random
import time


class PersonThread(threading.Thread):
    def __init__(self, field, measure, display):
        threading.Thread.__init__(self)
        self.field = field
        self.measure = measure
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
            location = self.decideWhereToGo()
            if location != None:
                self.field.acquire(l)
                if self.field.getLocation(location) == 0:
                    self.field.clear(self.location)
                    self.field.place(location)
                    self.location = location
                i = i + 1
                self.field.release(l)
            time.sleep(0.001)
        if not self.measure:
            with self.field.lock:
                print(self.getName(), "#", i)
                if self.display:
                    self.field.print()
        self.field.clear(self.location)

    def run(self):
        self.timeStart = time.clock()
        self.goToDoor()
        self.timeEnd = time.clock()

    def print(self):
        self.field.print()

    def getTimeComsume(self):
        return self.timeEnd - self.timeStart
