import argparse
def main(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument('-p',default=0, type=int,help='nombre de personnes présentent sur le terrain')
    parser.add_argument('-t',default=0, type=int,help='scénario de créations des threads')
    parser.add_argument('-m',help='mesure du temps d’exécution')

if __name__ == "__main__":
    main()
