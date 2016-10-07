#!/usr/bin/python

import logging
import sys

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main():
    data = read_mapper_output(sys.stdin)
    for line in data:
        k = line[0].split(':')
        setsstr = line[1].split(':')
        ratelist = list()
        for setstr in setsstr:
            ratelist.append(eval(setstr))
        # compute the Jaccard similarity
        logging.debug("%d:%d ratelist: %d", int(k[0]), int(k[1]), len(ratelist))
        print k[0], k[1], round(float(len(ratelist[0].intersection(ratelist[1].union(ratelist[2].intersection(ratelist[3]))))) / len(ratelist[0].union(ratelist[1]).union(ratelist[2]).union(ratelist[3])), 2)

if __name__ == "__main__":
    logging.basicConfig(filename='reducer.log', filemode='w', level=logging.DEBUG)
    main()
