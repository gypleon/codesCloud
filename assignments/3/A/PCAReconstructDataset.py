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
        self.prediction = []

    # TODO: this function is the core of PCA prediction
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
                print 'computing user means %d' % count
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
                print 'computing movie means %d' % count
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
                print 'filling or centering data %d' % count
            for j in range(self.num_movies):
                if 0 != self.rating_matrix[i][j]:
                    self.rating_matrix[i][j] -= (user_weight * user_means[i] + movie_weight * movie_means[j])
        print self.rating_matrix, self.rating_matrix.shape

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
            sigma[j] = np.sqrt(float(sigma[j]) / self.num_users)
        for j in range(self.num_movies):
            for i in range(self.num_users):
                if sigma[j] != 0:
                    normalized_matrix[i][j] = self.rating_matrix[i][j] / sigma[j]
        self.cov_matrix = np.cov(normalized_matrix, rowvar=0)
        print self.cov_matrix.shape

    def computeEigs(self):
        print "compute eigenvalues and eigenvectors"
        (eigvals, eigvecs) = np.linalg.eig(self.cov_matrix)
        print eigvals.shape, eigvecs.shape
        for i in range(len(eigvals)):
            self.eigs.append([eigvals[i], eigvecs[i]])
        # sort eigenvalues & eigenvectors
        sorted(self.eigs, key=lambda eigval:eigval[0], reverse=True)

    def reduceDimension(self, num_eigs):
        print "reduce dimensions with %d eigens" % num_eigs
        eig_matrix = []
        for i in range(num_eigs):
            sum_sq = 0
            for j in self.eigs[i][1]:
                sum_sq += j**2
            norm = np.sqrt(sum_sq)
            eigvec = []
            for j in self.eigs[i][1]:
                eigvec.append(j / norm)
            eig_matrix.append(eigvec)
        eig_matrix = np.matrix(eig_matrix)
        eig_matrix = eig_matrix.transpose()
        self.reduced_matrix = np.matrix(self.rating_matrix) * eig_matrix
        print self.reduced_matrix.shape

    def predict(self, input_test):
        print "predict (reconstruct the rating matrix)"
        self.reconst_matrix = self.reduced_matrix * self.reduced_matrix.transpose()
        print self.reconst_matrix, self.reconst_matrix.shape
        self.reconst_matrix = np.array(self.reconst_matrix)
        with file(input_test, 'r') as f:
            for line in f.readlines():
                (user, movie) = line.strip().split()
                self.prediction.append(self.reconst_matrix[int(user)-1][int(movie)-1])

    def outputPrediction(self, output):
        with file(output, 'w') as f:
            for pred_rating in self.prediction:
                f.write("%.3f\n" % pred_rating)
            

def main():
    # configuration
    input_train = "../dataset/train.txt"
    # input_train = "./testtrain.txt"
    input_test = "../dataset/test.txt"
    amount_of_eigs = [5, 20, 50]
    outputs = [ "./scores-%d.txt" % i for i in amount_of_eigs]
    # load train and test data
    myPredictor = PCAPredictor(input_train, amount_of_eigs)
    # construct original matrix with missing values
    # center values
    myPredictor.fillInMatrix()
    # compute covariance
    myPredictor.covariance()
    # compute eigenvalues & eigenvectors
    myPredictor.computeEigs()
    # dimensionality reduction
    for num_eigs in amount_of_eigs:
        myPredictor.reduceDimension(num_eigs)
        # reconstruct rating matrix
        myPredictor.predict(input_test)

    # generate prediction results
    for output in outputs:
        myPredictor.outputPrediction(output)

if __name__ == "__main__":
    main()
