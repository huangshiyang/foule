import argparse
import sys
from person import Person
from field import Field
import math
import psutil
import time


def checkArg(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], default=0, type=int,
                        help='nombre de personnes présentent sur le terrain')
    parser.add_argument('-t', choices=[0, 1], default=0, type=int, help='scénario de créations des threads')
    parser.add_argument('-m', action='store_true', help='mesure du temps d’exécution')
    results = parser.parse_args(args)
    return results

def getCPUstate(interval=1):
    return (" CPU:"+str(psutil.cpu_percent(interval))+"%")

if __name__ == "__main__":
    args = checkArg(sys.argv[1:])

    n = pow(2, args.p)
    if args.m:
        list=[0, 0, 0, 0, 0]
        sum=0
        for index in range(len(list)):
            if args.t == 0:
                field = Field(12, 8)
                field.obstruct()
                start = time.clock()
                if args.t == 0:
                    listP = []
                    while (n > 0):
                        listP.append(Person(field))
                        n = n - 1
                    for p in listP:
                        p.start()
                end = time.clock()
                list[index] = end - start
                sum += list[index]
#            elif args.t == 1:
        sum -= min(list) + max(list)
        print("average time : "+ str(sum/3))
        print(getCPUstate())
    else:
        if args.t == 0:
            field = Field(12, 8)
            field.obstruct()
            field.print()
            print("")
            if args.t == 0:
                listP=[]
                while (n > 0):
                    listP.append(Person(field, 0))
                    n = n - 1
                field.print()
                for p in listP:
                    p.start()
        elif args.t == 1:
            print("not done")



