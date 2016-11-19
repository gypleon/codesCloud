#!/usr/local/bin/python3

import numpy as np
import matplotlib.pyplot as plt


class Clusterers:
    def __init__(self, data_path):
        self._data_path = data_path
        self._points = list()
        self._clusters = list()
        self.load_data()

    def load_data(self):
        with open(self._data_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                point_str = line.strip("\n").split("\t")
                self._points.append([float(point_str[0]), float(point_str[1])])
            self._points = np.array(self._points)

    ''' Following is implementation for K-means clustering '''
    def k_means(self, init_centroids):
        cent = init_centroids
        print(self.mink_dist(cent[0], cent[1], 3))
        return

    def k_means_train(self, init_cents, dist_m):
        self._clusters = list()
        for cent in init_cents:
            self._clusters.append(cent)
        # num_clusters = len(init_cents)
        pre_obj = self.k_means_obj_func(dist_m)
        self.k_means_assign(init_cents, dist_m)
        self.k_means_update(dist_m)
        obj = self.k_means_obj_func(dist_m)
        loss = abs(pre_obj - obj)
        print(self.obj)
        print(self._clusters)
        return self._clusters

    def k_means_assign(self, cents, dist_m):
        for 
        return self._clusters

    def k_means_update(self, dist_m):
        return self._clusters

    def k_means_obj_func(self, dist_m):
        # res = 0
        # for clst_i in range(len(self._clusters)):
        #     cent = self._clusters[clst_i][0]
        #     res += sum(dist_m(cent, self._clusters[clst_i][i]) for i in range(1, len(self._clusters[clst_i])))
        # return res
        return sum( sum(dist_m(self._clusters[clst_i][0], self._clusters[clst_i][i]) for i in range(1, len(self._clusters[clst_i]))) for clst_i in range(len(self._clusters)))

    ''' Following is implementation for Hierarchical clustering '''
    def hierarchical(self):
        return 

    ''' Following is implementation for SOM clustering '''
    def som(self, init_centroids, a = 0.3, a_nb = 0.2, size_nb = 3, loss_threshold = 1e-16, learning_rate_threshold = 1e-10):
        # self.display_points(init_centroids)

        centroids = init_centroids
        print("[b] before training:\n", centroids)
        epoch = 0
        while True:
            epoch += 1
            pre_centroids = np.array(centroids)
            centroids = self.som_train(self._points, centroids, a, a_nb, size_nb, epoch)
            loss = np.linalg.norm(pre_centroids - centroids)
            print("loss: ", loss)
            if loss <= loss_threshold:
                break
        print("after training:\n", centroids, "\nround: ", epoch)
        self._clusters = self.som_assign(self._points, centroids)

        print("======================================")

        centroids = init_centroids
        print("[c] before training:\n", centroids)
        epoch = 0
        pre_loss = 0
        while True:
            epoch += 1
            pre_centroids = np.array(centroids)
            # TODO: epoch from 0 or 1?
            a -= 0.02
            a_nb -= 0.02
            centroids = self.som_train(self._points, centroids, a, a_nb, size_nb, epoch)
            loss = np.linalg.norm(pre_centroids - centroids)
            pre_loss = loss
            print("loss: ", loss)
            if loss <= loss_threshold or a <= learning_rate_threshold or a_nb <= learning_rate_threshold:
                break
        print("after training:\n", centroids, "\nround: ", epoch, ", a=", a, ", a_nb=", a_nb)
        self._clusters = self.som_assign(self._points, centroids)

        return self._clusters

    def som_train(self, examples, centroids, a, a_nb, size_nb, cur_round):
        # print("round: ", cur_round)
        for example in examples:
            # select winner centroid
            min_dist = 1000
            closest_cent = 0
            for ind in range(len(centroids)):
                dist = self.eucl_dist(centroids[ind], example)
                if dist < min_dist:
                    min_dist = dist
                    closest_cent = ind
            # print(closest_cent, centroids[closest_cent], min_dist) 
            # look for winner's neighbours
            nb_inds = list()
            for nb_i in range(len(centroids)):
                if nb_i != closest_cent:
                    nb_inds.append(nb_i)
            # update winner
            centroids[closest_cent] += a * ( example - centroids[closest_cent] )
            # update winner's neighbours
            for i in range(size_nb):
                centroids[nb_inds[i]] += a_nb * (example - centroids[nb_inds[i]])
        return centroids

    def som_assign(self, examples, centroids):
        self._clusters = list()
        # create clusters
        for ind in range(len(centroids)):
            self._clusters.append(np.array([centroids[ind]]))
        for example in examples:
            min_dist = 1000
            closest_cent = 0
            for ind in range(len(centroids)):
                dist = self.eucl_dist(centroids[ind], example)
                if dist < min_dist:
                    min_dist = dist
                    closest_cent = ind
            # print(closest_cent, min_dist)
            self._clusters[closest_cent] = np.append(self._clusters[closest_cent], np.array([example]), axis=0)
        cluster_num = 0
        for cluster in self._clusters:
            cluster_num += 1
            print("cluster", cluster_num)
            print(cluster)
        return self._clusters

    # a special case of minkovski-distance with 2 as lambda 
    def eucl_dist(self, vec1, vec2):
        # return self.mink_dist(vec1, vec2, 2)
        return np.linalg.norm(vec1 - vec2)

    # a special case of minkovski-distance with 1 as lambda 
    def city_dist(self, vec1, vec2):
        # return self.mink_dist(vec1, vec2, 1)
        return sum(abs(vec1[dim] - vec2[dim]) for dim in range(len(vec1)))

    def mink_dist(self, vec1, vec2, lmd = 3):
        return (sum((abs(vec1[dim] - vec2[dim]) ** lmd) for dim in range(len(vec1))) ** (1 / lmd))

    def display_points(self, points):
        plt.plot(points)
        plt.show()

    def display_clusters(self):
        # plot self._clusters
        return self._clusters

    def print_clusters(self):
        print(self._clusters)

def main():
    # configuration
    data_path = "./data_points"
    init_centroids_som = np.array([[1, 3.1], [2, 2.2], [1.5, 2.1], [3.1, 1.1]])
    init_centroids_kmeans = np.array([[1.8, 2.3], [2.3, 1.4]])
    lambda_kmeans_mink = 3
    # create my clusterers
    my_clusterers = Clusterers(data_path)
    # run k-means
    my_clusterers.k_means(init_centroids_kmeans)

    # run hierarchical

    # run som
    # my_clusterers.som(init_centroids_som)

if __name__ == "__main__":
    main()
