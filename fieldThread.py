import threading


class FieldThread(threading.Thread):
    def __init__(self, field, x1, y1, x2, y2, stopEvent):
        threading.Thread.__init__(self)
        self.stopEvent = stopEvent
        self.col1 = x1
        self.row1 = y1
        self.col2 = x2
        self.row2 = y2
        self.field = field
        self.personList = []


    def run(self):
        # print("not done")
        while not self.stopEvent.is_set():
            for row in range(self.row1, self.row2):
                for col in range(self.col1, self.col2):
                    if self.field.gridPerson[row][col] is not None:
                        self.personList.append(self.field.gridPerson[row][col])
            for person in self.personList[:]:
                if person.location.row > 1 or person.location.col > 1 or (
                                person.location.row == 1 and person.location.col == 1):
                    location = person.decideWhereToGo()
                    if not self.inBound(location):
                        self.field.acquire(location)
                        if self.field.getLocation(location) == 0:
                            self.field.clearPerson(person)
                            self.field.placePerson(person)
                            person.location = location
                            self.personList.remove(person)
                        self.field.release(location)
                    else:
                        self.field.clearPerson(person)
                        self.field.placePerson(person)
                        person.location = location
                else:
                    self.field.clearPerson(person)
                    self.personList.remove(person)
            with self.field.lock:
                print("")
                self.field.print()

    def inBound(self, location):
        return location.col < self.col2 and location.col >= self.col1 and location.row < self.row2 and location.row >= self.row1

    def havePerson(self):
        return self.personList
