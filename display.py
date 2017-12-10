from tkinter import *
from copy import deepcopy
import time
import threading


class Display():
    def __init__(self, data):
        self.root = Tk()
        self.frame = Frame(self.root)
        self.data = data
        self.setup()

    def setup(self):
        self.root.title("Foule")
        self.frame.pack(fill=BOTH, expand=2)
        self.canvas = Canvas(self.frame, width=self.data.field.width * 3 + 8, height=self.data.field.height * 3 + 8)
        self.canvas.pack(fill=BOTH, side=TOP)
        last = Button(self.frame, text="Last", command=self.lastGrid)
        next = Button(self.frame, text="Next", command=self.nextGrid)
        back = Button(self.frame, text="Back", command=self.back)
        last.pack(side=LEFT)
        next.pack(side=LEFT)
        back.pack(side=LEFT)
        self.indexLabel = Label(self.frame, text=str(self.data.index + 1) + "/" + str(len(self.data.grid)))
        self.indexLabel.pack(side=LEFT)
        self.draw(self.data.grid[self.data.index])

    def draw(self, grid):
        for row in range(self.data.field.height):
            for col in range(self.data.field.width):
                bloc = grid[row][col]
                x1 = 5 + col * 3
                y1 = 5 + row * 3
                x2 = x1 + 3
                y2 = y1 + 3
                if bloc == 0:
                    self.data.rects[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray",
                                                                             outline="gray")
                elif bloc == 1:
                    self.data.rects[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="red")
                elif bloc == 2:
                    self.data.rects[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

    def updateGrid(self, grid):
        for row in range(self.data.field.height):
            for col in range(self.data.field.width):
                bloc = grid[row][col]
                id = self.data.rects[row][col]
                if bloc == 0:
                    self.canvas.itemconfig(id, fill="gray", outline="gray")
                elif bloc == 1:
                    self.canvas.itemconfig(id, fill="red", outline="red")
                elif bloc == 2:
                    self.canvas.itemconfig(id, fill="black")

    def lastGrid(self):
        if self.data.index is not 0:
            self.data.index = self.data.index - 1
            self.updateGrid(self.data.grid[self.data.index])
            self.indexLabel.config(text=str(self.data.index + 1) + "/" + str(len(self.data.grid)))

    def nextGrid(self):
        if self.data.index is not len(self.data.grid) - 1:
            self.data.index = self.data.index + 1
            self.updateGrid(self.data.grid[self.data.index])
            self.indexLabel.config(text=str(self.data.index + 1) + "/" + str(len(self.data.grid)))

    def back(self):
        self.data.index = 0
        self.updateGrid(self.data.grid[self.data.index])
        self.indexLabel.config(text=str(self.data.index + 1) + "/" + str(len(self.data.grid)))


class DisplayData(threading.Thread):
    def __init__(self, field):
        threading.Thread.__init__(self)
        self.field = field
        self.rects = [[0 for i in range(field.width)] for j in range(field.height)]
        self.grid = []
        self.grid.append(deepcopy(self.field.grid))
        self.flag = True
        self.index = 0

    def run(self):
        self.store()

    def store(self):
        while self.flag:
            matrix = deepcopy(self.field.grid)
            self.grid.append(matrix)

    def endRecord(self):
        self.flag = False
