import argparse
import sys
from personThread import PersonThread
from person import Person
from field import Field
from fieldThread import FieldThread
import time
import threading
from display import DisplayData
from display import Display


def checkArg(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], default=0, type=int,
                        help='nombre de personnes présentent sur le terrain')
    parser.add_argument('-t', choices=[0, 1], default=0, type=int, help='scénario de créations des threads')
    parser.add_argument('-m', action='store_true', help='mesure du temps d’exécution')
    parser.add_argument('-d', action='store_true', help='display')
    results = parser.parse_args(args)
    return results


def stop():
    for row in range(0, field.height):
        for col in range(0, field.height):
            if field.grid[row][col] is 1:
                return False
    return True


if __name__ == "__main__":
    args = checkArg(sys.argv[1:])

    n = pow(2, args.p)
    if args.m:
        print("Mesuring...Run 5 times. Please be patient.")
        cpuTimeList = [0, 0, 0, 0, 0]
        responseTimeList = [0, 0, 0, 0, 0]
        responseTimeSum = 0
        cpuTimeSum = 0
        for index in range(len(responseTimeList)):
            number = n
            cpuTime = 0
            if args.t == 0:
                field = Field(512, 128)
                field.obstruct()
                barrier = threading.Barrier(n)
                print("#", index + 1, "run.")
                personList = []
                while number > 0:
                    personList.append(PersonThread(field, args.m, barrier))
                    number = number - 1
                responseTimeStart = time.time()
                for person in personList:
                    person.start()
                for person in personList:
                    person.join()
                responseTimeEnd = time.time()
                for person in personList:
                    cpuTime += person.getTimeComsume()
            elif args.t == 1:
                field = Field(512, 128)
                field.obstruct()
                barrier = threading.Barrier(4)
                print("#", index + 1, "run.")
                while number > 0:
                    Person(field)
                    number = number - 1
                stopEvent = threading.Event()
                field1 = FieldThread(field, 0, 0, int(field.width / 2), int(field.height / 2), stopEvent, args.m,
                                     barrier)
                field2 = FieldThread(field, int(field.width / 2), 0, field.width, int(field.height / 2), stopEvent,
                                     args.m, barrier)
                field3 = FieldThread(field, 0, int(field.height / 2), int(field.width / 2), field.height,
                                     stopEvent, args.m, barrier)
                field4 = FieldThread(field, int(field.width / 2), int(field.height / 2), field.width, field.height,
                                     stopEvent, args.m, barrier)

                responseTimeStart = time.time()
                field1.start()
                field2.start()
                field3.start()
                field4.start()

                flag = True
                while flag:
                    personSet = set()
                    for row in range(0, field.height):
                        for col in range(0, field.height):
                            if field.gridPerson[row][col] is not None:
                                personSet.add(field.gridPerson[row][col])
                    flag = personSet
                stopEvent.set()
                field1.join()
                field2.join()
                field3.join()
                field4.join()
                responseTimeEnd = time.time()

                cpuTime = field1.getTimeComsume() + field2.getTimeComsume() + field3.getTimeComsume() + field4.getTimeComsume()
            responseTime = responseTimeEnd - responseTimeStart
            print("response time :", responseTime, "second(s)")
            print("CPU time :", cpuTime, "second(s)")
            print("")
            responseTimeList[index] = responseTime
            cpuTimeList[index] = cpuTime
            responseTimeSum += responseTimeList[index]
            cpuTimeSum += cpuTimeList[index]
        responseTimeSum -= min(responseTimeList) + max(responseTimeList)
        cpuTimeSum -= min(cpuTimeList) + max(cpuTimeList)
        print("average response time :", responseTimeSum / 3, "second(s)")
        print("average CPU time :", cpuTimeSum / 3, "second(s)")

    else:
        if args.t == 0:
            print("running")
            field = Field(512, 128)
            field.obstruct()
            print("")
            personList = []
            if args.d:
                barrier = threading.Barrier(n + 1)
            else:
                barrier = threading.Barrier(n)
            while (n > 0):
                personList.append(PersonThread(field, args.m, barrier))
                n = n - 1
            if args.d:
                displayData = DisplayData(field)
            for person in personList:
                person.start()
            if args.d:
                barrier.wait()
                displayData.start()
            for person in personList:
                person.join()
            if args.d:
                displayData.endRecord()
            print("done")
            if args.d:
                display = Display(displayData)
                display.root.mainloop()
        elif args.t == 1:
            print("running")
            field = Field(512, 128)
            field.obstruct()
            if args.d:
                barrier = threading.Barrier(5)
            else:
                barrier = threading.Barrier(4)
            while n > 0:
                Person(field)
                n = n - 1
            stopEvent = threading.Event()
            field1 = FieldThread(field, 0, 0, int(field.width / 2), int(field.height / 2), stopEvent, args.m, barrier)
            field2 = FieldThread(field, int(field.width / 2), 0, field.width, int(field.height / 2), stopEvent, args.m,
                                 barrier)
            field3 = FieldThread(field, 0, int(field.height / 2), int(field.width / 2), field.height,
                                 stopEvent, args.m, barrier)
            field4 = FieldThread(field, int(field.width / 2), int(field.height / 2), field.width, field.height,
                                 stopEvent, args.m, barrier)
            if args.d:
                displayData = DisplayData(field)
            field1.start()
            field2.start()
            field3.start()
            field4.start()

            if args.d:
                barrier.wait()
                displayData.start()
            flag = False
            while not flag:
                flag = stop()
            stopEvent.set()
            field1.join()
            field2.join()
            field3.join()
            field4.join()
            if args.d:
                displayData.endRecord()
            print("done")
            if args.d:
                display = Display(displayData)
                display.root.mainloop()
