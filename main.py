import argparse
import sys
from person import Person
from field import Field
import math
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
    t = args.t
    if args.m:
        print("I'm mesuring...Please be patient=)")
        list = [0, 0, 0, 0, 0]
        listR = [0, 0, 0, 0, 0]
        sum = 0
        sumR = 0
        for index in range(len(list)):
            number = n
            if t == 0:
                field = Field(512, 128)
                field.obstruct()
                print(".")
                listP = []
                while (number > 0):
                    listP.append(Person(field, 0))
                    number = number - 1
                if args.d:
                    field.print()
                for p in listP:
                    p.start()
                for p in listP:
                    p.join()
            elif t == 1:
                    print("not done")
            list[index] = resource.getrusage(resource.RUSAGE_SELF).ru_utime
            listR[index] = resource.getrusage(resource.RUSAGE_SELF).ru_stime
            sum += list[index]
            sumR += listR[index]
        sum -= min(list) + max(list)
        sumR -= min(listR) + max(listR)
        print("average response time : "+ str(sum/3))
        print("average CPU time : " + str(sumR / 3))
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print ("Memory usage is: {0} KB".format(mem))
    else:
        if args.t == 0:
            field = Field(512, 128)
            field.obstruct()
            if args.d:
                field.print()
            print("")
            if args.t == 0:
                listP = []
                while (n > 0):
                    listP.append(Person(field, args.d))
                    n = n - 1
#                if args.d:
 #                   field.print()
                for p in listP:
                    p.start()
        elif args.t == 1:
            print("not done")