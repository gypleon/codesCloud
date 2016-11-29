#!/usr/bin/python

import redis
from ctypes import cdll

def main():
    slotlib = cdll.LoadLibrary('./libslot.so')
    nodes_file = "/data/opt/course/1155081867/Twitter-dataset/data/nodes.csv"
    edges_file = "/data/opt/course/1155081867/Twitter-dataset/data/edges.csv"
    redis_hosts = [ "proj5", "proj6", "proj7" ]
    redis_port = 6379
    cons = []
    for i in range(len(redis_hosts)):
        cons.append(redis.StrictRedis(redis_hosts[i], redis_port))

    ef = open(edges_file, 'r')
    print "ef loading..."
    eflines = ef.readlines()
    eflen = len(eflines)
    print "ef len", eflen
    cur_efline_i = 0
    with open(nodes_file, 'r') as nf:
        for nfline in nf.readlines():
            node = nfline.strip('\r\n')
#            if int(node) > 100:
#                break;
#            print "node", node
            followees = []
            while cur_efline_i < eflen:
                edge = eflines[cur_efline_i].strip('\r\n')
                follower = edge.split(',')[0]
                followee = edge.split(',')[1]
                if follower == node:
#                     print "  |-followee", followee
                    cur_efline_i += 1
                    followees.append(int(followee))
                else:
                    break;
            slot = slotlib.slot(node, len(node))
#            print slot
            if slot >= 10923:
                which = 1
            elif slot >= 5461:
                which = 0
            else:
                which = 2
            print "deleting", node, redis_hosts[which]
            cons[which].delete(int(node))
            if len(followees) > 0:
                print "creating", node, followees
                cons[which].rpush(int(node), *followees)
    print "closing ef"
    ef.close()
    print "end"

if __name__ == "__main__":
    main()
