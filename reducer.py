#!/usr/bin/python

import logging
import sys

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main():
    data = read_mapper_output(sys.stdin)
    for line in data:
        k = line[0]
        setsstr = line[1].split(':')
        ratelist = list()
        for setstr in setsstr:
            ratelist.append(eval(setstr))
        # compute the Jaccard similarity
        # print ratelist
        u1itu2l = ratelist[0].intersection(ratelist[1])
        u1itu2u = ratelist[2].intersection(ratelist[3])
        u1unu2l = ratelist[0].union(ratelist[1])
        u1unu2u = ratelist[2].union(ratelist[3])
        result = round(float(len(u1itu2l.union(u1itu2u))) / len(u1unu2l.union(u1unu2u)), 4)
        print k, result

if __name__ == "__main__":
    main()
