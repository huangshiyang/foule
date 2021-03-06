from location import Location
import random
import threading


class Field:
    def __init__(self, x, y):
        self.grid = [[0 for i in range(x)] for j in range(y)]
        self.gridPerson = [[None for i in range(x)] for j in range(y)]
        self.gridLock = [[threading.Lock() for i in range(x)] for j in range(y)]
        self.width = x
        self.height = y

    def acquire(self, location):
        self.gridLock[location.row][location.col].acquire()

    def release(self, location):
        self.gridLock[location.row][location.col].release()

    def getFreeAdjacentLocations(self, location):
        locations = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0) and self.inBound(location.row + i, location.col + j) and \
                        self.grid[location.row + i][location.col + j] == 0:
                    locations.append(Location(location.row + i, location.col + j))
        return locations

    def clear(self, location):
        self.grid[location.row][location.col] = 0

    def clearPerson(self, location):
        self.clear(location)
        self.gridPerson[location.row][location.col] = None

    def place(self, location):
        self.grid[location.row][location.col] = 1

    def placePerson(self, person):
        self.place(person.location)
        self.gridPerson[person.location.row][person.location.col] = person

    def obstruct(self):
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 0 and not self.isUpperLeftAdjacent(x, y):
                    width = self.width - 1
                    height = self.height - 1
                    if random.uniform(0, 1000) < 5:
                        while width > self.width - x - 1 or height > self.height - y - 1 or self.isCovered(x, y, height,
                                                                                                           width) or self.isUnder(
                                x, y, width):
                            width = random.randint(0, min(100, self.width - x, self.underX(x, y, width)))
                            height = random.randint(0, min(20, self.height - y))
                        for x2 in range(x, width + x):
                            for y2 in range(y, height + y):
                                self.grid[y2][x2] = 2

    def inBound(self, row, col):
        return (0 <= row < self.height) and (0 <= col < self.width)

    def isUpperLeftAdjacent(self, x, y):
        return not (self.grid[y - 1][x - 1] == 0 and self.grid[y][x - 1] == 0 and self.grid[y + 1][x - 1] == 0 and
                    self.grid[y - 1][x] == 0 and self.grid[y - 1][x + 1] == 0)

    def isCovered(self, x, y, height, width):
        if y + height > self.height - 1:
            return True
        if x + width > self.width - 1:
            return True
        for i in range(y, height + y):
            for j in range(x, width + x):
                if self.grid[i][j] != 0:
                    return True
        return False

    def isUnder(self, x, y, width):
        if x + width > self.width - 1:
            width = self.width - x - 1
        for i in range(x + 1, width + x + 1):
            if self.grid[y - 1][i] != 0:
                return True
        return False

    def underX(self, x, y, width):
        if x + width > self.width - 1:
            width = self.width - x - 1
        for i in range(x + 1, width + x + 1):
            if not self.grid[y - 1][i] == 0:
                return i
        return self.width - 1

    def getLocation(self, location):
        return self.grid[location.row][location.col]
