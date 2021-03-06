import threading
from location import Location
import math
import random
import time


class PersonThread(threading.Thread):
    def __init__(self, field, measure, barrier):
        threading.Thread.__init__(self)
        self.field = field
        self.measure = measure
        self.barrier = barrier
        while True:
            location = Location(random.randint(0, self.field.height - 1),
                                random.randint(0, self.field.width - 1))
            if self.field.getLocation(location) == 0:
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
        while self.location.row > 1 or self.location.col > 1 or (self.location.row == 1 and self.location.col == 1):
            l = self.location
            location = self.decideWhereToGo()
            if location is not None:
                self.field.acquire(l)
                if self.field.getLocation(location) == 0:
                    self.field.clear(self.location)
                    self.field.place(location)
                    self.location = location
                self.field.release(l)
        self.field.clear(self.location)

    def run(self):
        self.barrier.wait()
        if self.measure:
            self.timeStart = time.clock()
            self.goToDoor()
            self.timeEnd = time.clock()
        else:
            self.goToDoor()

    def getTimeComsume(self):
        return self.timeEnd - self.timeStart
