#!/usr/bin/python

import sys
import json
# import pydoop.hdfs as hdfs

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
    usrinfos = load_usrinfos("usrlist")
    mapout = read_mapper(sys.stdin)
    top100 = []
    for line in mapout:
        usrpair = line[1].split(':')
        usr1 = int(usrpair[0])
        usr2 = int(usrpair[1])
        u1inf = usrinfos[usr1-1]
        u2inf = usrinfos[usr2-1]
        u1inf['l'] = set(u1inf['l'])
        u1inf['u'] = set(u1inf['u'])
        u2inf['l'] = set(u2inf['l'])
        u2inf['u'] = set(u2inf['u'])
        # optimization: filter out some unlikely data
        estupper = float(len(u1inf['l'])+len(u1inf['u'])) / (len(u2inf['l'])+len(u2inf['u']))
        if estupper < 0.9 or estupper > 1.1:
            continue
        elif 0 == len(u1inf['l'] & u2inf['l']) and 0 == len(u1inf['u'] & u2inf['u']):
            continue
        else:
            # compute Jaccard Similarity
            js = round(float(len(u1inf['l'] & u2inf['l'] | (u1inf['u'] & u2inf['u']))) / len(u1inf['l'] | u2inf['l'] | u1inf['u'] | u2inf['u']), 2)
            toplen = len(top100)
            # optimization: maintain local top 100 jaccards
            if 0 == toplen:
                top100.append([usr1, usr2, js])
            else:
                top100.append([usr1, usr2, js])
                top100 = sorted(top100, cmp = lambda x, y: int(y[2]*1000-x[2]*1000))
            if toplen > 100:
                top100.pop()
            # print "%6d\t%6d\t%.2f" % (usr1, usr2, js)
    for u1u2 in top100:
        print "%s\t%s\t%.2f" % (u1u2[0], u1u2[1], u1u2[2])

if __name__ == "__main__":
    main()
