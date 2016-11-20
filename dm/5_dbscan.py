#!/usr/local/bin/python3

import numpy as np
from scipy.spatial import distance as sd

def load_data(data_path):
    points = list()
    with open(data_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            point_str = line.strip("\n").split("\t")
            points.append([float(point_str[0]), float(point_str[1])])
        points = np.array(points)
    return points

def label_cores(points, eps, minpts):
    cores = list()
    num_ps = len(points)
    pdist = sd.pdist(points)
    for i in range(num_ps):
        count = 0
        for j in range(num_ps):
            if i == j:
                continue
            # edist = np.linalg.norm(np.abs(points[i] - points[j]))
            dist = get_dist(pdist, i, j, num_ps)
            if dist <= eps:
                count += 1
                if count > minpts:
                    cores.append(points[i])
                    break
    return np.array(cores)

def label_borders(points, cores, eps):
    borders = list()
    remain = list()
    for p_i in range(len(points)):
        is_core = False
        for core_i in range(len(cores)):
            if np.array_equal(cores[core_i], points[p_i]):
                is_core = True
                break
        if not is_core:
            remain.append(points[p_i])
    remain = np.array(remain)
    for r_i in range(len(remain)):
        for c_i in range(len(cores)):
            dist = np.linalg.norm(np.abs(remain[r_i] - cores[c_i]))
            if dist <= eps:
                borders.append(remain[r_i])
                break
    return np.array(borders)

def label_noises(points, cores, borders):
    noises = list()
    for p_i in range(len(points)):
        is_core = False
        for core_i in range(len(cores)):
            if np.array_equal(cores[core_i], points[p_i]):
                is_core = True
                break
        is_border = False
        for bord_i in range(len(borders)):
            if np.array_equal(borders[bord_i], points[p_i]):
                is_border = True
                break
        if not is_core and not is_border:
            noises.append(points[p_i])
    return np.array(noises)

def direct_reach(r, points, eps):
    r_nbs = list()
    for point in points:
        if not np.array_equal(point, r) and np.linalg.norm(np.abs(point - r)) <= eps:
            r_nbs.append(point)
    return np.array(r_nbs)

# add neighbour core' neighbours
def indirect_reach(c_nb, d_nbs, ind_nbs, points, cores, eps):
    nbs = direct_reach(c_nb, points, eps)
    for nb in nbs:
        added = False
        for ind_nb in ind_nbs:
            if np.array_equal(ind_nb, nb):
                added = True
        if added:
            continue
        is_d_nb = False
        for d_nb in d_nbs:
            if np.array_equal(d_nb, nb):
                is_d_nb = True
        if is_d_nb:
            continue
        if np.array_equal(np.array([2,5]),nb):
            continue
        ind_nbs = np.append(ind_nbs, np.array([nb]), axis=0)
        # print("add", nb)
        # if it is a core 
        for core in cores:
            if np.array_equal(core, nb):
                # core's nb
                # print("detect", nb)
                ind_nbs = np.append(ind_nbs, indirect_reach(nb, d_nbs, ind_nbs, points, cores, eps), axis=0)
                break
    return ind_nbs

def get_dist(pdist, i, j, l):
    if i < j:
        res = (i*(l-2)+j-i*(i-1)/2-1) 
    elif i > j:
        res = (j*(l-2)+i-j*(j-1)/2-1) 
    # print(res)
    return pdist[int(res)]

def print_points(points, title):
    print(title)
    for point in points:
        print(point)

def main():
    # configuration
    eps = 1.5
    minpts = 3
    print("===================== a. cores, borders & noise points =====================")
    points = load_data("dbscan_points")
    cores = label_cores(points, eps, minpts)
    print_points(cores, "cores:")
    borders = label_borders(points, cores, eps)
    print_points(borders, "borders:")
    noises = label_noises(points, cores, borders)
    print_points(noises, "noise points:")
    print("===================== b. reachable from R(2,5) =====================")
    r_nbs = direct_reach(np.array([2,5]), points, eps)
    print_points(r_nbs, "R(2,5) is a Core, hence his neighbours are directly reachable:")
    ind_nbs = np.zeros([0,2])
    for r_nb in r_nbs:
        for core in cores:
            if np.array_equal(core, r_nb):
                # print("detect", r_nb)
                r_nb_nbs = indirect_reach(r_nb, r_nbs, ind_nbs, points, cores, eps)
                added = False
                for r_nb_nb in r_nb_nbs:
                    for ind_nb in ind_nbs:
                        if np.array_equal(r_nb_nb, ind_nb):
                            added = True
                            break
                if not added:
                    ind_nbs = np.append(ind_nbs, r_nb_nbs, axis=0)
    print_points(ind_nbs, "indirectly:")
    return

if __name__ == "__main__":
    main()
