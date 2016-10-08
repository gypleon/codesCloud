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
def findFrequentItemsets( plist, cur, thrd ):
    filist = list()
    if cur <= thrd:
        fimat = list()
        nplist = list()
        ncplist = list()
        for pset in plist:
            # print(pset, cur)
            lenpset = len(pset)
            if lenpset >= cur:
                if lenpset == cur:
                    if len(fimat) == 0:
                        fimat.append([pset, 1])
                    else:
                        existed = False
                        for row in fimat:
                            if row[0] == pset:
                                row[1] += 1
                                existed = True
                                break
                        if not existed:
                            fimat.append([pset, 1])
                else:
                    ncplist.append(pset)
                    for row in fimat:
                        if row[0].issubset(pset):
                            row[1] += 1
                            break
        # print(fimat, cur)
        for row in fimat:
            if row[1] >= thrd:
                filist.append(row[0])
        for npset in ncplist:
            for fis in filist:
                if fis.issubset(npset):
                    nplist.append(npset)
                    break
        # print(filist)
        fimat.clear()
        ncplist.clear()
        filist.extend( findFrequentItemsets(nplist, cur+1, thrd))
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
    with open('./B.txt', 'w') as f:
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
    outputfile = './A.txt'
    plist = getPrimesLists(start, end)
    # print(plist)
    sortFISandOutput( findFrequentItemsets(plist, dimstart, threshold), outputfile)
