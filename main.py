import argparse
import sys
def checkArg(args=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('-p',default=0, type=int,help='nombre de personnes présentent sur le terrain')
    parser.add_argument('-t',default=0, type=int,help='scénario de créations des threads')
    parser.add_argument('-m',help='mesure du temps d’exécution')
    results=parser.parse_args(args)

if __name__ == "__main__":
    checkArg(sys.argv[1:])
