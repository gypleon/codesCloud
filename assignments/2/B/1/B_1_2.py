#!/usr/local/bin/python3

import tensorflow as tf
import numpy as np
import sys, getopt

def parsePoint(str_point):
    point = str_point.rstrip(')').split("(")[1].split(',')
    point = [int(point[0]), int(point[1])]
    return point

def eucDistances(points, centroids):
    exp_points = tf.expand_dims(points, 0)
    exp_centroids = tf.expand_dims(centroids, 1)
    distances = tf.reduce_sum(tf.square(tf.sub(exp_points, exp_centroids)), 2)
    return distances

def assignPoints(points, distances, n_clusters):
    clusters_inds = tf.to_int32(tf.argmin(distances, 0))
    clusters = tf.dynamic_partition(points, clusters_inds, n_clusters)
    return clusters

def newCentroids(clusters):
    new_centroids = tf.concat(0, [tf.expand_dims(tf.reduce_mean(cluster, 0), 0) for cluster in clusters])
    return new_centroids

def main(argv):
    print('you can input initial CENTROIDS in format like:\npython3 B-1-2.py \"A7(6,2)|A8(6,4)|A10(7,2)|A11(7,5)\"\n')
    # load raw data
    with open("points.txt") as f:
        rawpoints = f.readline().rstrip('\n').split('|')
    points = np.ndarray([0,2])
    for point in rawpoints:
        points = np.append(points, [parsePoint(point)], axis = 0)
    centroids = np.ndarray([0,2])
    # if command-line arguments
    if len(argv) > 0:
        try:
            opts, args = getopt.getopt(argv, '')
            rawcentroids = args[0].rstrip('\n').split('|')
            for c in rawcentroids:
                centroids = np.append(centroids, [parsePoint(c)], axis = 0)
        except:
            print('please input initial CENTROIDS in format like \"A7(1,1)|A8(1,2)|A10(7,2)|A11(7,5)\"')
            sys.exit()
    else:
        centroids = np.append(centroids, [[1,1], [5,12], [7,2], [15,8]], axis = 0)
    print("Initial Centroids:\n", centroids)
    n_clusters = len(centroids)
    threshold = 0
    # apply tensorflow 
    graph = tf.Graph()
    with graph.as_default():
        points = tf.Variable(points, name = 'points')
        centroids = tf.Variable(centroids, name = 'centroids')
        model = tf.initialize_all_variables()
        clusters = assignPoints(points, eucDistances(points, centroids), n_clusters)
        new_centroids = newCentroids(clusters)
        update_centroids = tf.assign(centroids, new_centroids)
        # new_centroids = tf.placeholder(tf.float64, shape = tf.shape(centroids), name = 'new_centroids')
        # k-means begin
        with tf.Session() as session:
            session.run(model)
            i = 1
            while session.run(tf.greater(tf.reduce_max(tf.reduce_sum(tf.square(tf.sub(new_centroids, centroids)), 1)), threshold)):
                print("Tensorflow Round[%d]:" % i)
                i += 1
                res = session.run(new_centroids)
                session.run(update_centroids)
                print(res)

if __name__ == "__main__":
    main(sys.argv[1:])
