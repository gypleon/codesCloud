#!/usr/local/bin/python3

import numpy as np

# Shingling
def Shingling( sen, co ):
    ret = set()
    for i in range(0, len(sen)-co+1):
        ret.add(sen[i:i+co])
    return ret

# print matrix
def prinmat( mat):
    row = len(mat)
    col = len(mat[0])
    for i in range(row):
        for j in range(col):
            print("%s\t" % str(mat[i][j]), end='')
        print('\n')

# Matrix representation
def Matriculating( sens, shingles):
    uset = set()
    for sh in shingles:
        uset |= sh
    uset = sorted(list(uset))
    print(uset)
    nrow = len(uset)
    ncol = len(sens)
    mat = list([[0 for i in range(ncol + 1)] for j in range(nrow + 1)])
    for i in range(1, nrow+1):
        mat[i][0] = uset[i-1]
    for i in range(1, ncol+1):
        mat[0][i] = sens[i-1]
    for i in range(1, nrow+1):
        currow = mat[i][0]
        for j in range(1, ncol+1):
            cursen = mat[0][j]
            if currow in cursen:
                mat[i][j] = 1
    return mat

# h1 = 7x+1 mod 10
def hashFunc1(x):
    return (x * 7 + 1) % 10

# h2 = 8x+2 mod 10
def hashFunc2(x):
    return (x * 8 + 2) % 10

# h3 = 6x+2 mod 10
def hashFunc3(x):
    return (x * 6 + 2) % 10

# MinHash signature
def minHash( mat, hfunc):
    signatures = list()
    hvalues = list()
    for i in range(1, len(mat)):
        hvalues.append( hfunc(i))
    print("hash values: %s" % str(hvalues))
    for j in range(1, len(mat[0])):
        minv = len(mat)-1
        for i in range(1, len(mat)):
            if mat[i][j] == 1 and minv > hvalues[i-1]:
                minv = hvalues[i-1]
        signatures.append(minv)
    return signatures

def minHashMatrix(sigs):
    mat = list()
    for sig in sigs:
        mat.append(sig)
    return mat

# Estimated Jaccard similarity
def estimatedJaccard(mat):
    nrow = len(mat)
    ncol = len(mat[0])
    js = dict()
    for j in range(ncol-1):
        for k in range(j+1, ncol):
            s1 = list([mat[i][j] for i in range(nrow)])
            s2 = list([mat[i][k] for i in range(nrow)])
            sim = 0
            for x in range(nrow):
                if s1[x] == s2[x]:
                    sim += 1
            js["s%d-s%d" % (j+1, k+1)] = float(sim) / nrow
    return js


# True Jaccard similarity
def trueJaccard(mat):
    nrow = len(mat)
    ncol = len(mat[0])
    nmat = []
    js = dict()
    for j in range(1, ncol-1):
        for k in range(j+1, ncol):
            s1 = list([mat[i][j] for i in range(1, nrow)])
            s2 = list([mat[i][k] for i in range(1, nrow)])
            sim = 0
            tol = 0
            for x in range(len(s1)):
                if 1 == s1[x] or 1 == s2[x]:
                    tol += 1
                if 1 == s1[x] and 1 == s2[x]:
                    sim += 1
            js["s%d-s%d" % (j, k)] = float(sim) / tol
    return js
    

# E-T close
def closeMeasure(e, t):
    devs = list()
    for k, v in e.items():
        # devs.append((e[k] - t[k])/t[k])
        devs.append(e[k]/t[k])
    sumd = 0
    for i in devs:
        sumd += i
    return (sumd / len(devs))


if __name__ == '__main__':
    sentences = ( 'acbcbd', 'adbcad', 'cdbdad', 'bcacbd', 'bdadca' )
    shingles = list()
    print("=== ORIGINAL DOCUMENTS(Sentences) ===")
    print(sentences)
    for s in sentences:
        shingles.append( Shingling(s, 2))
    print("=== a. 2=SHINGLES ===")
    for i in range(0, len(shingles)):
        print(shingles[i])
    mat = Matriculating( sentences, shingles)
    print("=== a. SHINGLE MATRIX ===")
    prinmat(mat)
    print("=== b. MINHASH ===")
    mat2 = minHashMatrix([minHash(mat, hashFunc1), minHash(mat, hashFunc2), minHash(mat, hashFunc3)])
    prinmat(mat2)
    print("=== d. ESTIMATED JACCARD SIMILARITY ===")
    eJ = estimatedJaccard(mat2)
    for k, v in eJ.items():
        print("%s\t%.2f\n" % (k, v), end='')
    print("=== d. TRUE JACCARD SIMILARITY ===")
    tJ = trueJaccard(mat)
    for k, v in tJ.items():
        print("%s\t%.2f\n" % (k, v), end='')
    print("=== d. HOW CLOSE ===")
    avg_dev = closeMeasure(eJ, tJ)
    print("%.2f" % avg_dev)
