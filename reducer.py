#!/usr/bin/python

import sys
import json
import bisect as bs
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
    # top100 = []
    top100 = {}
    for line in mapout:
        key = int(line[0])
        if not top100.has_key(key):
            top100[key] = []
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
            toplen = len(top100[key])
            # optimization: maintain local top 100
            if 0 == toplen:
                top100[key].append(js)
            else:
                top100[key].reverse()
                bs.insort_right(top100[key], js)
                top100[key].reverse()
            if toplen > 10:
                top100[key].pop()
                
    # print "%d\t%s" % (key, ",".join(str(l) for l in top100))
    for k, v in top100.iteritems():
        print "%d\t%s" % (k, ",".join(str(l) for l in v))


if __name__ == "__main__":
    main()
