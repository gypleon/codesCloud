#!/usr/local/bin/python3

import math
import numpy as np

# get prime factors unduplicatedly, optimized
def getPrimes( num ):
    pset = set()
    if 0 == num % 2:
        pset.add(2)
    for i in range(3, num+1, 2):
        if 0 == num % i:
            isprime = True
            for j in range(3, int(math.sqrt(i))+1, 2):
                if 0 == i % j and i != j:
                    isprime = False
                    break
            if isprime:
                pset.add(i)
    if len(pset) == 0:
        pset.add(num)
    return pset

# get prime factor lists, optimized: sorted by set length
def getPrimesLists( start, end ):
    plist = list()
    for i in range(start, end+1):
        plist.append(getPrimes(i))
    plist.sort(key=lambda ps:len(ps))
    return plist

# find frequent itemsets, to be optimized: implemented in multi-round map-reduce
def findFrequentItemsets( buckets, candset, cursize, thrd ):
    # print(len(buckets), len(candset), cursize, thrd)
    filist = list()
    newcandset = list()
    # count frequent item sets in current loop
    for itemset in buckets:
        if len(itemset) == cursize:
            maybe = False
            if len(candset) == 0:
                maybe = True
            else:
                for cand in candset:
                    if set(cand).issubset(set(itemset)):
                        maybe = True
            if maybe:
                count = 0
                for bucket in buckets:
                    if set(itemset).issubset(set(bucket)):
                        count += 1
                        if count >= thrd:
                            existed = False
                            for check in filist:
                                if itemset == check:
                                    existed = True
                                    break
                            if not existed:
                                filist.append(itemset)
                            break
    # construct candidate item sets for next loop
    # print(filist)
    for i in range(len(filist)-1):
        for j in range(i+1, len(filist)):
            cand = list(set(filist[i]).union(set(filist[j])))
            if len(cand) == cursize+1:
                existed = False
                for check in newcandset:
                    if cand == check:
                        existed = True
                        break
                if not existed:
                    newcandset.append(cand)
    if len(newcandset) == 0:
        return filist
    # next loop
    filist.extend(findFrequentItemsets( buckets, newcandset, cursize+1, thrd ))
    # return current result
    return filist

# sort frequent itemsets list & output
def sortFISandOutput( filist, outputfile ):
    outlist = list()
    dtype = list()
    order = list()
    for i in filist:
        outlist.append(tuple(sorted(list(i))))
    print(outlist)
    maxfield = len(outlist[len(outlist)-1])
    for i in range(1, maxfield+1):
        dtype.append((str(i), int))
        order.append(str(i))
    # print(dtype, order)
    outlist = np.array(outlist, dtype = dtype)
    outlist.sort(order = order)
    with open(outputfile, 'w') as f:
        for out in outlist:
            # print(out)
            for i in out:
                f.write("%2d\t" % i)
            f.write("\n")
    return 0

if __name__ == "__main__":
    start = 2
    end = 10000
    dimstart = 3
    threshold = 50
    outputfile = './B.txt'
    buckets = getPrimesLists(start, end)
    sortFISandOutput( findFrequentItemsets(buckets, [], dimstart, threshold), outputfile)
    # print( findFrequentItemsets(buckets, set([]), dimstart, threshold))
