from location import Location



class Field:
    def __init__(self, row, col):
        self.grid = [[0 for x in range(col)] for y in range(row)]

    def getFreeAdjacentLocations(self, location):
        locations = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0) and self.inBound(location.row + i, location.col + j) and \
                                self.grid[location.row + i][location.col + j] == 0:
                    locations.append(Location(location.row + i, location.col + j))
        return  locations

    def inBound(self, row, col):
        return ((row >= 0 and row < len(self.grid)) and (col >= 0 and col < len(self.grid[0])))
