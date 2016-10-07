#!/usr/bin/python

import sys

def main():
    usramount = 0
    for line in sys.stdin:
        usramount += 1
    key = 0
    for usr1 in range(1, usramount):
        for usr2 in range(usr1+1, usramount+1):
            key += 1
            key = key % 17
            print "%d\t%d:%d" % (key, usr1, usr2)

if __name__ == "__main__":
    main()   
