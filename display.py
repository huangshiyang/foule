from location import Location
from tkinter import *
import threading


class DisplayThread(threading.Thread):
    def __init__(self, field):
        threading.Thread.__init__(self)
        self.field=field
        self.start()
    def run(self):
        root = Tk()
        self.display = Display(self.field, root)
        root.mainloop()

class Display(Frame):
    def __init__(self, field, root):
        Frame.__init__(self)
        self.field = field
        self.root = root
        self.setup()

    def setup(self):
        self.root.title("Foule")
        self.pack(fill=BOTH, expand=2)
        self.canvas = Canvas(self, width=self.field.width * 3 + 8, height=self.field.height * 3 + 8)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.draw()

    def draw(self):
        for row in range(self.field.height):
            for col in range(self.field.width):
                bloc = self.field.getLocation(Location(row, col))
                x1 = 5 + col * 3
                y1 = 5 + row * 3
                x2 = x1 + 3
                y2 = y1 + 3
                if bloc == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                elif bloc == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
                elif bloc == 2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
