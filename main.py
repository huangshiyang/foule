import argparse
import sys
from personThread import PersonThread
from person import Person
from field import Field
from fieldThread import FieldThread
import resource
import time


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
        userTimeList = [0, 0, 0, 0, 0]
        systemTimeList = [0, 0, 0, 0, 0]
        responseTimeList = [0, 0, 0, 0, 0]
        userTimeSum = 0
        systemTimeSum = 0
        responseTimeSum = 0
        for index in range(len(userTimeList)):
            number = n
            if args.t == 0:
                field = Field(512, 128)
                field.obstruct()
                print(".")
                personList = []
                while (number > 0):
                    personList.append(PersonThread(field, args.m, args.d))
                    number = number - 1
                responseTimeStart = time.time()
                userTimeStart = resource.getrusage(resource.RUSAGE_SELF).ru_utime
                systemTimeStart = resource.getrusage(resource.RUSAGE_SELF).ru_stime
                for person in personList:
                    person.start()
                for person in personList:
                    person.join()
                responseTimeEnd = time.time()
                userTimeEnd = resource.getrusage(resource.RUSAGE_SELF).ru_utime
                systemTimeEnd = resource.getrusage(resource.RUSAGE_SELF).ru_stime
            else:  # args.t == 1
                responseTimeStart = time.time()
                userTimeStart = resource.getrusage(resource.RUSAGE_SELF).ru_utime
                systemTimeStart = resource.getrusage(resource.RUSAGE_SELF).ru_stime
                print("not done")
                responseTimeEnd = time.time()
                userTimeEnd = resource.getrusage(resource.RUSAGE_SELF).ru_utime
                systemTimeEnd = resource.getrusage(resource.RUSAGE_SELF).ru_stime

            userTimeList[index] = userTimeEnd - userTimeStart
            systemTimeList[index] = systemTimeEnd - systemTimeStart
            responseTimeList[index] = responseTimeEnd - responseTimeStart
            userTimeSum += userTimeList[index]
            systemTimeSum += systemTimeList[index]
            responseTimeSum += responseTimeList[index]
        userTimeSum -= min(userTimeList) + max(userTimeList)
        systemTimeSum -= min(systemTimeList) + max(systemTimeList)
        responseTimeSum -= min(responseTimeList) + max(responseTimeList)
        print("average response time :", responseTimeSum / 3, "second(s)")
        print("average CPU time :", (userTimeSum / 3) + (systemTimeSum / 3), "second(s)")
        rusage_denom = 1024.
        if sys.platform == 'darwin':
            rusage_denom = rusage_denom * rusage_denom
        memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / rusage_denom
        print("Memory usage :", memory, "MB")

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
            fieldList = []
            fieldList.append(FieldThread(field, 0, 0, int(field.width / 2), int(field.height / 2)))
            fieldList.append(FieldThread(field, int(field.width / 2), 0, field.width, int(field.height / 2)))
            fieldList.append(FieldThread(field, 0, int(field.height / 2), int(field.width / 2), field.height))
            fieldList.append(FieldThread(field, int(field.width / 2), int(field.height / 2), field.width, field.height))
            for fieldThread in fieldList:
                fieldThread.start()
            for fieldThread in fieldList:
                fieldThread.join()
