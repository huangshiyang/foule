import argparse
import sys
from person import Person
from location import Location
from field import Field


def checkArg(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', metavar='0123456789', default=0, type=int,
                        help='nombre de personnes présentent sur le terrain')
    parser.add_argument('-t', metavar='01', default=0, type=int, help='scénario de créations des threads')
    parser.add_argument('-m', metavar='', help='mesure du temps d’exécution')
    results = parser.parse_args(args)


if __name__ == "__main__":
    checkArg(sys.argv[1:])
