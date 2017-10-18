import threading
import location

class Person(threading.Thread):

    def __init__(self, field, location):
        threading.Thread.__init__(self)
        self.field = field
        self.location = location

    def goToDoor(self):
        while location.row != 0:
            print()
            #todo

    def run(self):
        self.goToDoor()