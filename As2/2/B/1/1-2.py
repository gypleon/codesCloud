#/usr/local/bin/python3

import tensorflow as tf
import numpy as np
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
    

if __name__ == "__main__":
    main()
