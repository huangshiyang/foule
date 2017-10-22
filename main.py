import argparse
import sys
from person import Person
from field import Field
import math


def checkArg(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], default=0, type=int,
                        help='nombre de personnes présentent sur le terrain')
    parser.add_argument('-t', choices=[0, 1], default=0, type=int, help='scénario de créations des threads')
    parser.add_argument('-m', action='store_true', help='mesure du temps d’exécution')
    results = parser.parse_args(args)
    return results


if __name__ == "__main__":
    args = checkArg(sys.argv[1:])

    n = pow(2, args.p)
    if args.t == 0:
        field = Field(512, 128)
        field.obstruct()
        if args.t == 0:
            listP=[]
            while (n > 0):
                listP.append(Person(field))
                n = n - 1
            for p in listP:
                p.start()
    elif args.t == 1:
        print("not done")
