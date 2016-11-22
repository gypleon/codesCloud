#!/usr/local/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance as sd


class Clusterers:
    def __init__(self, data_path):
        self._data_path = data_path
        self._points = list()
        self._clusters = list()
        self._centroids = list()
        self.load_data()

    def load_data(self):
        with open(self._data_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                point_str = line.strip("\n").split("\t")
                self._points.append([float(point_str[0]), float(point_str[1])])
            self._points = np.array(self._points)
        # print(np.average(self._points, axis=0))

    ''' ################# Following is implementation for K-means clustering ################# '''
    def k_means(self, init_centroids):
        cent = init_centroids
        # print(self.mink_dist(cent[0], cent[1], 3))
        print("=============  (a) Euclidean  ==============")
        self.k_means_train(init_centroids, self.eucl_dist)
        print("=============  (b) Cityblock  ==============")
        self.k_means_train(init_centroids, self.city_dist)
        print("=============  (c) Minkovski  ==============")
        self.k_means_train(init_centroids, self.mink_dist)
        return

    def k_means_train(self, init_cents, dist_m):
        # num_clusters = len(init_cents)
        self._centroids = list(init_cents)
        self._clusters.clear()

        loss = 1000
        epoch = 0
        while loss > 0:
            epoch += 1
            print("=============  epoch", epoch, "==============")
            pre_obj = self.k_means_obj_func(dist_m)
            # assign points
            self.print_centroids()
            self.k_means_assign(dist_m)
            # update centroids
            self.k_means_update()
            self.print_clusters()
            obj = self.k_means_obj_func(dist_m)
            print("result of pre_obj func:", pre_obj)
            print("result of obj func:", obj)
            loss = abs(pre_obj - obj)
            print("loss:", loss)
        print("amount of epoch:", epoch)

        return self._clusters

    def k_means_assign(self, dist_m):
        cents = self._centroids
        self._clusters = [np.zeros([0,2]) for i in range(len(cents))]
        # for cent in cents:
        #     self._clusters.append(np.array([cent]))
        for point in self._points:
            min_dist = 1000
            min_ind = 0
            for cent_ind in range(len(cents)):
                dist = dist_m(point, cents[cent_ind])
                if dist < min_dist:
                    min_dist = dist
                    min_ind = cent_ind
            # print(point, self._clusters[min_ind][0], min_dist)
            self._clusters[min_ind] = np.append(self._clusters[min_ind], np.array([point]), axis=0)
        return self._clusters

    def k_means_update(self):
        self._centroids.clear()
        for clst in self._clusters:
            # print(clst[1:])
            self._centroids.append(np.average(clst[:], axis = 0))
            # print(self._centroids)
        return self._centroids

    def k_means_obj_func(self, dist_m):
        # res = 0
        # for clst_i in range(len(self._clusters)):
        #     cent = self._clusters[clst_i][0]
        #     res += sum(dist_m(cent, self._clusters[clst_i][i]) for i in range(1, len(self._clusters[clst_i])))
        # return res
        return sum( sum(dist_m(self._clusters[clst_i][0], self._clusters[clst_i][i]) for i in range(1, len(self._clusters[clst_i]))) for clst_i in range(len(self._clusters)))

    ''' ################# Following is implementation for Hierarchical clustering ################# '''
    def hierarchical(self):
        self._clusters.clear()
        # print pair-wise proximity matrix for original points
        print("======================= a. initial proximity matrix & clusters =======================")
        pdist = self.hier_pdist()
        self.hier_show_prox_mat(self._points, pdist, "[Point-Point Proximities]", True, "p")
        dists = self.hier_init_clusters()
        self.print_clusters()
        self._clusters.clear()

        # complete linkage
        print("======================= b. complete linkage  =======================")
        dists = self.hier_init_clusters(self.hier_dist_complete)
        self.hier_show_prox_mat(self._clusters, dists, "[Cluster-Cluster Proximities]", True)
        while len(self._clusters)>1:
            dists = self.hier_update(dists, self.hier_dist_complete)
            self.hier_show_prox_mat(self._clusters, dists, "[Cluster-Cluster Proximities]", True)
        self._clusters.clear()

        # single linkage
        print("======================= c. single linkage  =======================")
        dists = self.hier_init_clusters(self.hier_dist_single)
        self.hier_show_prox_mat(self._clusters, dists, "[Cluster-Cluster Proximities]", True)
        while len(self._clusters)>1:
            dists = self.hier_update(dists, self.hier_dist_single)
            self.hier_show_prox_mat(self._clusters, dists, "[Cluster-Cluster Proximities]", True)
        self._clusters.clear()

        # group average
        print("======================= d. group average =======================")
        dists = self.hier_init_clusters(self.hier_dist_group)
        self.hier_show_prox_mat(self._clusters, dists, "[Cluster-Cluster Proximities]", True)
        while len(self._clusters)>1:
            dists = self.hier_update(dists, self.hier_dist_group)
            self.hier_show_prox_mat(self._clusters, dists, "[Cluster-Cluster Proximities]", True)
        self._clusters.clear()

        return 

    def hier_init_clusters(self, dist_m = None):
        # initialize 5 separations (0-3, 4-7, 8-11, 12-15, 16-19)
        # self._clusters = [np.zeros([0,2]) for i in range(5)]
        # for clst_i in range(len(self._clusters)):
        #     for p_i in range(clst_i * 4, clst_i * 4 + 4):
        #         self._clusters[clst_i] = np.append(self._clusters[clst_i], np.array([self._points[p_i]]), axis=0)
        #         # print(np.array([self._points[p_i]]))

        # initialize 5 separations using single-linkage
        for point in self._points:
            self._clusters.append(np.array([point]))
        pdist = self.hier_pdist()
        dists = self.hier_update(pdist, self.hier_dist_single)
        while len(self._clusters) != 5:
            dists = self.hier_update(dists, self.hier_dist_single)
        if dist_m:
            # dists = dist_m(pdist)
            dists = dist_m()
            return dists
        return

    def hier_update(self, dists, merge_m):
        self.hier_merge(dists)
        # return merge_m(dists)
        return merge_m()

    def hier_merge(self, dists):
        # merge clusters based on a certain linkage method
        min_ind = np.argmin(dists)
        # self.print_clusters()
        num_clst = len(self._clusters)
        for clst_1 in range(num_clst-1):
            for clst_2 in range(clst_1+1, num_clst):
                if min_ind == self.hier_rcl(clst_1, clst_2, num_clst):
                    print("[Notes] 'c%02d'" % clst_2, "will be merged into 'c%02d'" % clst_1)
                    # found the closest cluster pair
                    # print(clst_1, clst_2)
                    clusters = list() 
                    for clst_i in range(num_clst):
                        if clst_i == clst_2:
                            clusters[clst_1] = np.append(clusters[clst_1], self._clusters[clst_2], axis=0)
                            continue
                        clusters.append(self._clusters[clst_i])
                    self._clusters = clusters
                    break
        # self.print_clusters()
        return self._clusters

    def hier_pdist(self):
        return sd.pdist(self._points)

    # def hier_dist_single(self, pdist):
    def hier_dist_single(self):
        clusters = self._clusters
        dists = np.zeros([0])
        for clst_1 in range(len(clusters)-1):
            for clst_2 in range(clst_1 + 1, len(clusters)):
                min_dist = np.min(sd.cdist(clusters[clst_1], clusters[clst_2]))
                dists = np.append(dists, np.array([min_dist]))
                # print(clst_1, clst_2, min_dist)
        return dists

    # def hier_dist_complete(self, pdist):
    def hier_dist_complete(self):
        clusters = self._clusters
        dists = np.zeros([0])
        for clst_1 in range(len(clusters)-1):
            for clst_2 in range(clst_1 + 1, len(clusters)):
                max_dist = np.max(sd.cdist(clusters[clst_1], clusters[clst_2]))
                dists = np.append(dists, np.array([max_dist]))
        return dists

    # def hier_dist_group(self, pdist):
    def hier_dist_group(self):
        clusters = self._clusters
        dists = np.zeros([0])
        for clst_1 in range(len(clusters)-1):
            for clst_2 in range(clst_1 + 1, len(clusters)):
                avg_dist = np.average(sd.cdist(clusters[clst_1], clusters[clst_2]))
                dists = np.append(dists, np.array([avg_dist]))
        return dists

    def hier_show_prox_mat(self, clusters, pdist, title, if_print = False, label = 'c'):
        if if_print:
            num_p = len(clusters)
            # print table header
            print(title)
            if label == "p":
                print("             ", end="")
            else:
                print("    ", end="")
            for i in range(num_p):
                print(" %s%02d " % (label, i), end="")
            print()
            # print matrix
            row = 0
            for i in sd.squareform(pdist):
                col = 0
                if label == "p":
                    print("%s%02d[%.1f,%.1f] " % (label, row, clusters[row][0], clusters[row][1]), end="")
                else:
                    print("%s%02d " % (label, row), end="")
                for j in i:
                    if row == col:
                        print("0.00 ", end="")
                    else: 
                        print("%.2f " % pdist[self.hier_rcl(row,col,num_p)], end="")
                        # if j == pdist[self.hier_rcl(row,col,num_p)]:
                        #     print('true ', end="")
                    col += 1
                row += 1
                print()
        return pdist

    # get dist from condensed pdist, based on #row, #col and len
    def hier_rcl(self, i, j, l):
        if i < j:
            res = (i*(l-2)+j-i*(i-1)/2-1) 
        elif i > j:
            res = (j*(l-2)+i-j*(j-1)/2-1) 
        # print(res)
        return int(res)

    ''' ################# Following is implementation for SOM clustering ################# '''
    def som(self, init_centroids, a = 0.3, a_nb = 0.2, size_nb = 3, loss_threshold = 1e-16, learning_rate_threshold = 1e-10):
        # self.display_points(init_centroids)

        self._clusters.clear()
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
        self.print_clusters()

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
        self.print_clusters()

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
        cluster_num = 0
        for cluster in self._clusters:
            cluster_num += 1
            print("cluster", cluster_num)
            print(cluster)

    def print_centroids(self):
        cent_num = 0
        for cent in self._centroids:
            cent_num += 1
            print("centroid", cent_num, ":", cent)

def main():
    # configuration
    data_path = "./data_points"
    # create my clusterers
    my_clusterers = Clusterers(data_path)

    # run k-means
    init_centroids_kmeans = np.array([[1.8, 2.3], [2.3, 1.4]])
    lambda_kmeans_mink = 3
    my_clusterers.k_means(init_centroids_kmeans)

    # run hierarchical
    my_clusterers.hierarchical()

    # run som
    init_centroids_som = np.array([[1, 3.1], [2, 2.2], [1.5, 2.1], [3.1, 1.1]])
    my_clusterers.som(init_centroids_som)

if __name__ == "__main__":
    main()
