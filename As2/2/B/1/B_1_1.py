#!/usr/bin/python

from __future__ import print_function
import sys
import math

def parsePoint(str_point):
    point = str_point.rstrip(')').split("(")[1].split(',')
    point = [int(point[0]), int(point[1])]
    return point

def distance2(p1, p2):
    dist = math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2)
    return dist

def restorePoint(point, points):
    for i in range(len(points)):
        if point == points[i]:
            str_point = "A%d" % (i+1)
            break
    return str_point

def main():
    with open("points.txt") as f:
        rawpoints = f.readline().rstrip('\n').split('|')
    points = list()
    for point in rawpoints:
        points.append(parsePoint(point))
    clusters = list([[([1,1],0)], [([5,12],0)], [([7,2],0)], [([15,8],0)]])
    for cluster in clusters:
        points.remove(cluster[0][0])
    # print(points)
    for point in points:
        mind = 10000
        mini = 0
        for i in range(len(clusters)):
            cur = distance2(point, clusters[i][0][0])
            if cur < mind:
                mind = cur
                mini = i
        clusters[mini].append((point, int(mind)))
    centers = list()
    for cluster in clusters:
        # print(cluster)
        centerx = 0
        centery = 0
        for point in cluster:
            centerx += point[0][0]
            centery += point[0][1]
        centerx = round(float(centerx) / len(cluster), 2)
        centery = round(float(centery) / len(cluster), 2)
        centers.append([cluster, (centerx, centery)])
    for center in centers:
        print(center)

if __name__ == "__main__":
    main()
