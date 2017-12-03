import argparse
import sys
from personThread import PersonThread
from person import Person
from field import Field
from fieldThread import FieldThread
from location import Location
import time
import threading


def checkArg(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], default=0, type=int,
                        help='nombre de personnes présentent sur le terrain')
    parser.add_argument('-t', choices=[0, 1], default=0, type=int, help='scénario de créations des threads')
    parser.add_argument('-m', action='store_true', help='mesure du temps d’exécution')
    parser.add_argument('-d', action='store_true', help='display')
    results = parser.parse_args(args)
    return results


if __name__ == "__main__":
    args = checkArg(sys.argv[1:])

    n = pow(2, args.p)
    if args.m:
        print("I'm mesuring...Please be patient=)")
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
                print(".")
                personList = []
                while (number > 0):
                    personList.append(PersonThread(field, args.m, args.d))
                    number = number - 1
                responseTimeStart = time.time()
                for person in personList:
                    person.start()
                for person in personList:
                    person.join()
                    cpuTime += person.getTimeComsume()
                responseTimeEnd = time.time()
            else:  # args.t == 1
                responseTimeStart = time.time()
                print("not done")
                responseTimeEnd = time.time()

            responseTimeList[index] = responseTimeEnd - responseTimeStart
            cpuTimeList[index] = cpuTime
            responseTimeSum += responseTimeList[index]
            cpuTimeSum += cpuTimeList[index]
        responseTimeSum -= min(responseTimeList) + max(responseTimeList)
        cpuTimeSum -= min(cpuTimeList) + max(cpuTimeList)
        print("average response time :", responseTimeSum / 3, "second(s)")
        print("average CPU time :", cpuTimeSum / 3, "second(s)")

    else:
        if args.t == 0:
            field = Field(512, 128)
            field.obstruct()
            if args.d:
                field.print()
            print("")
            personList = []
            while (n > 0):
                personList.append(PersonThread(field, args.m, args.d))
                n = n - 1
            if args.d:
                field.print()
            for person in personList:
                person.start()
            for person in personList:
                person.join()
            print("")
        elif args.t == 1:
            # print("not done")
            field = Field(10, 10)
            field.obstruct()
            while (n > 0):
                Person(field)
                n = n - 1
            field.print()
            stopEvent = threading.Event()
            field1 = FieldThread(field, 0, 0, int(field.width / 2), int(field.height / 2), stopEvent)
            field2 = FieldThread(field, int(field.width / 2), 0, field.width, int(field.height / 2), stopEvent)
            field3 = FieldThread(field, 0, int(field.height / 2), int(field.width / 2), field.height,
                                 stopEvent)
            field4 = FieldThread(field, int(field.width / 2), int(field.height / 2), field.width, field.height,
                                 stopEvent)
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
            print("done")
