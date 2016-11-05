#!/usr/bin/python

# Usage:
#

# Reference
#

import numpy as np
import time


class PCAPredictor:
    def __init__(self, inputTrain, amount_of_eigs=5):
        print "initialize predictor"
        self.num_users = 0
        self.num_movies = 0
        self.obs_ratings = []
        with file(inputTrain, 'r') as f:
            for line in f.readlines():
                (user, movie, rating) = line.strip().split()
                self.obs_ratings.append([int(user), int(movie), float(rating)])
                if self.num_users < int(user):
                    self.num_users = int(user)
                if self.num_movies < int(movie):
                    self.num_movies = int(movie)
        print self.num_users, self.num_movies
        self.rating_matrix = np.zeros(shape=[self.num_users, self.num_movies])
        self.obs_ratings = np.array(self.obs_ratings)
        self.eigs = []
        self.cov_matrix = []
        self.reduced_matrix = []
        self.reconst_matrix = []

    def fillInMatrix(self):
        print "fill in matrix and center data"
        # initialize rating matrix
        for rating_tup in self.obs_ratings:
            (i, j, rating) = rating_tup
            self.rating_matrix[i-1][j-1] = rating
        # fill in missing values (or center observed values) with naive method, weighted means of ratings
        # compute means for rows(users) and columns(movies)
        user_means = []
        movie_means = []
        count = 0
        for i in range(self.num_users):
            count += 1
            if count % 1000 == 0:
                print 'user', time.ctime()
            user_count = 0
            user_sum = 0
            for j in range(self.num_movies):
                rating = self.rating_matrix[i][j]
                if rating != 0:
                    user_count += 1
                    user_sum += rating
            if user_count != 0:
                user_means.append(float(user_sum)/user_count)
            else:
                user_means.append(float(0))
        count = 0
        for j in range(self.num_movies):
            count += 1
            if count % 1000 == 0:
                print 'movie', time.ctime()
            movie_count = 0
            movie_sum = 0
            for i in range(self.num_users):
                rating = self.rating_matrix[i][j]
                if rating != 0:
                    movie_count += 1
                    movie_sum += rating
            if movie_count != 0:
                movie_means.append(float(movie_sum)/movie_count)
            else:
                movie_means.append(float(0))
        # center these data with weights
        user_weight = 1
        movie_weight = 0
        count = 0
        for i in range(self.num_users):
            count += 1
            if count % 1000 == 0:
                print 'fill', time.ctime()
            for j in range(self.num_movies):
                if 0 != self.rating_matrix[i][j]:
                    self.rating_matrix[i][j] -= (user_weight * user_means[i] + movie_weight * movie_means[j])
        print self.rating_matrix

    # Wiberg's method for missing values
    # TODO: implement it later
    def fillExpectation(self):
        pass
    def fillMaximization(self):
        pass
    def fillConvergence(self):
        pass
    
    def covariance(self):
        print "compute covariance matrix"
        sigma = []
        normalized_matrix = self.rating_matrix
        for j in range(self.num_movies):
            sigma.append(0)
            for i in range(self.num_users):
                sigma[j] += (self.rating_matrix[i][j]**2)
            sigma[j] = float(sigma[j]) / self.num_users
        for j in range(self.num_movies):
            for i in range(self.num_users):
                normalized_matrix[i][j] = self.rating_matrix[i][j] / sigma[j]
        self.cov_matrix = np.cov(normalized_matrix, rowvar=0)

    def computeEigs(self):
        print "compute eigenvalues and eigenvectors"
        (eigvals, eigvecs) = np.linalg.eig(self.cov_matrix)
        for i in range(eigvals):
            self.eigs.append([eigvals[i], eigvecs[i]])
        # sort eigenvalues & eigenvectors
        self.eigs.sort(reverse=True)

    def reduceDimension(self, num_eigs):
        print "reduce dimensions"
        eig_matrix = []
        for i in range(num_eigs):
            eig_matrix.append(self.eigs[i][1])
        eig_matrix = np.matrix(eig_matrix)
        eig_matrix = eig_matrix.transpose()
        self.reduced_matrix = np.matrix(self.rating_matrix) * eig_matrix

    def predict(self):
        print "predict"
        self.reconst_matrix

    def outputPrediction(self, input_test, output):
        with file(input_test, 'r') as f:
            for line in f.readlines():
                (user, movie) = line.split()
        with file(output, 'w') as f:
            pass
            

def main():
    # configuration
    input_train = "../dataset/train.txt"
    input_test = "../dataset/test.txt"
    amount_of_eigs = [5, 20, 50]
    output = "./scores-%d.txt" % (amount_of_eigs)
    # load train and test data
    myPredictor = PCAPredictor(input_train, amount_of_eigs)
    # construct original matrix with missing values
    # center values
    myPredictor.fillInMatrix()
    # compute covariance
    myPredictor.covariance()
    # dimensionality reduction
    for num_eigs in amount_of_eigs:
        myPredictor.reduceDimension(num_eigs)
        # reconstruct rating matrix
        myPredictor.predict()

    # generate prediction results
    myPredictor.outputPrediction(input_test, output)

if __name__ == "__main__":
    main()
