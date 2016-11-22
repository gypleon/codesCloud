#!/usr/local/bin/python3

import numpy as np

def load_data(data_path):
    points = list()
    with open(data_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            point_str = line.strip("\n").split("\t")
            points.append([float(point_str[0]), float(point_str[1])])
        points = np.array(points)
    return points

def ssei(cluster):
    # print(cluster)
    c = np.average(cluster, axis=0)
    # print(c)
    sse = 0
    for x in cluster:
        sse += np.square(np.linalg.norm(x-c))
    return sse

def sse(clusters):
    sse = 0
    for cluster in clusters:
        sse += ssei(cluster)
    return sse

def ssb(clusters, points):
    c = np.average(points, axis=0)
    ssb = 0
    for cluster in clusters:
        ci = np.average(cluster, axis=0)
        ssb += len(cluster) * np.square(np.linalg.norm(c-ci))
    return ssb

def tss(clusters, points):
    c = np.average(points, axis=0)
    tss = 0
    for point in points:
        tss += np.square(np.linalg.norm(point-c))
    return tss

def main():
    points = load_data("./6_points")
    print("================ a. ================")
    print("Cluster 1:")
    print(points[:3])
    print("Cluster 2:")
    print(points[3:])
    se1 = ssei(points[:3])
    print("SSE1 =",se1)
    se2 = ssei(points[3:])
    print("SSE2 =",se2)
    se = sse([points[:3], points[3:]])
    print("SSE =",se)
    sb = ssb([points[:3], points[3:]], points)
    print("SSB =",sb)
    ts = tss([points[:3], points[3:]], points)
    print("TSS =",ts)
    # print(se+sb)
    print("================ b. ================")
    cluster1 = np.array([points[0],points[5]])
    cluster2 = np.array([points[1],points[3]])
    cluster3 = np.array([points[2],points[4]])
    print("Cluster 1:")
    print(cluster1)
    print("Cluster 2:")
    print(cluster2)
    print("Cluster 3:")
    print(cluster3)
    se1 = ssei(cluster1)
    print("SSE1 =",se1)
    se2 = ssei(cluster2)
    print("SSE2 =",se2)
    se3 = ssei(cluster3)
    print("SSE3 =",se3)
    se = sse([cluster1,cluster2,cluster3])
    print("SSE =",se)
    sb = ssb([cluster1,cluster2,cluster3], points)
    print("SSB =",sb)
    ts = tss([cluster1,cluster2,cluster3], points)
    print("TSS =",ts)
    # print(se+sb)

if __name__ == "__main__":
    main()
