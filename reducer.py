#!/usr/bin/python

import sys
import json
import pydoop.hdfs as hdfs

def read_mapper(mapout):
    for line in mapout:
        yield line.split('\t')

def load_usrinfos(jsonf):
    usrinfos = list()
    # with hdfs.open(jsonf, 'r') as f:
    with open(jsonf, 'r') as f:
        for line in f:
            usrinfos.append(json.loads(line))
    return usrinfos

def main():
    usrinfos = load_usrinfos("usrlist.test")
    mapout = read_mapper(sys.stdin)
    top100 = []
    for line in mapout:
        key = line[0]
        usrpair = line[1].split(':')
        usr1 = int(usrpair[0])
        usr2 = int(usrpair[1])
        u1inf = usrinfos[usr1-1]
        u2inf = usrinfos[usr2-1]
        # optimization: filter out some unlikely data
        estupper = float(len(u1inf['l'])+len(u1inf['u'])) / (len(u2inf['l'])+len(u2inf['u']))
        if estupper < 0.9 or estupper > 1.1:
            continue
        elif 0 == len(u1inf['l'] & u2inf['l']) and 0 == len(u1inf['u'] & u2inf['u']):
            continue
        else:
            # compute Jaccard Similarity
            js = float(len(u1inf['l'] & u2inf['l'] | (u1inf['u'] & u2inf['u']))) / len(u1inf['l'] | u2inf['l'] | u1inf['u'] | u2inf['u'])
            top100.append(js)
        # optimization: maintain local top 100
        print "%d\t%s" % (key, ",".join(str(l) for l in top100))


if __name__ == "__main__":
    main()
