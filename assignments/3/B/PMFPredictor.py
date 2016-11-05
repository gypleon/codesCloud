#!/usr/bin/python
#-*- coding:utf-8 -*-

import numpy as np
import time
import pickle

class PMFPredictor:
    def __init__(self, inputTrain, latent_d=5):
        self.latent_d = latent_d
        # initialize learning rate
        self.learning_rate = .0001
        
        self.ratings = np.array(self.loadData(inputTrain))
        self.converged = False
        
        self.num_users = int(np.max(self.ratings[:, 0]) + 1)
        self.num_movies = int(np.max(self.ratings[:, 1]) + 1)
        
        print (self.num_users, self.num_movies, self.latent_d)
        print self.ratings
        
        self.users = np.random.random((self.num_users, self.latent_d))
        self.movies = np.random.random((self.num_movies, self.latent_d))

        self.sigma = np.std(self.ratings, axis=0)[2]
        self.lambda_U = 0.1
        self.lambda_M = 0.1
        
        self.new_users = np.random.random((self.num_users, self.latent_d))
        self.new_movies = np.random.random((self.num_movies, self.latent_d))
    
    
    def loadData(self, inputTrain):
        count = 0
        mylist = []
        with file(inputTrain, 'r') as f:
            for line in f.readlines():
                user, movie, rating = line.split()
                dataformat = [int(user), int(movie), float(rating)]
                mylist.append(dataformat)
                count += 1
                if count % 100000 == 0:
                    print count
        return mylist


    def objectiveFunc(self, users=None, movies=None):
        if None == users:
            users = self.users
        else:
            sigma_U = np.std(users)
            self.lambda_U = np.square(self.sigma/sigma_U)
        if None == movies:
            movies = self.movies
        else:
            sigma_M = np.std(movies)
            self.lambda_M = np.square(self.sigma/sigma_M)

        # empirical risk term            
        error = 0
        for rating_tuple in self.ratings:
            i, j, rating = rating_tuple
            r_hat = np.sum(users[i] * movies[j])
            error += (rating - r_hat)**2

        # regularization term
        users_i_norm = 0
        movies_j_norm = 0
        for i in range(self.num_users):
            for d in range(self.latent_d):
                users_i_norm += users[i, d]**2
        for i in range(self.num_movies):
            for d in range(self.latent_d):
                movies_j_norm += movies[i, d]**2

        return error + self.lambda_U * users_i_norm + self.lambda_M * movies_j_norm


    def update(self):
        # updates_o holds updates to the latent features of users
        # updates_d holds updates to the latent features of movies
        updates_o = np.zeros((self.num_users, self.latent_d))
        updates_d = np.zeros((self.num_movies, self.latent_d))
        
        # converge if likelihood changes by less than .1 or if learning rate goes below 1e-10
        # speed up by 1.25x if improving, slow down by 0.5x if not improving
        while (not self.converged):
            initial_lik = self.objectiveFunc()
            
            print "[", time.ctime(), "]", "likelihood =", self.objectiveFunc(), "  rate =", self.learning_rate, "  lambda U M =", self.lambda_U, " ", self.lambda_M
            # apply updates to self.new_users and self.new_movies
            self.try_updates(updates_o, updates_d)
            
            final_lik = self.objectiveFunc(self.new_users, self.new_movies)
            
            # if the new latent feature vectors are better, keep the updates, and increase the learning rate (i.e. momentum)
            if final_lik < initial_lik:
                self.apply_updates(updates_o, updates_d)
                self.learning_rate *= 1.25
                if initial_lik - final_lik < .1:
                    self.converged = True
            else:
                self.learning_rate *= .5
                pass
            
            if self.learning_rate <= 3e-5:
                self.converged = True
        
        return not self.converged
    
    
    def apply_updates(self, updates_o, updates_d):
        for i in range(self.num_users):
            for d in range(self.latent_d):
                self.users[i, d] = self.new_users[i, d]
        for i in range(self.num_movies):
            for d in range(self.latent_d):
                self.movies[i, d] = self.new_movies[i, d]
    
    
    def try_updates(self, updates_o, updates_d):
        """
        Update self.new_users and self.new_movies with updates calculated with batch GD
        """
        # batch update: run through all ratings for each iteration
        for rating_tuple in self.ratings:
            (i, j, rating) = rating_tuple
            # r_hat is the predicted rating for user i on movie j
            r_hat = np.sum(self.users[i] * self.movies[j])
            # update each feature
            for d in range(self.latent_d):
                updates_d[j, d] += self.users[i, d] * (r_hat - rating)
                updates_o[i, d] += self.movies[j, d] * (r_hat - rating)
        for i in range(self.num_users):
            for d in range(self.latent_d):
                self.new_users[i, d] = self.users[i, d] - self.learning_rate * (updates_o[i, d] + self.lambda_U * self.users[i, d])
        for i in range(self.num_movies):
            for d in range(self.latent_d):
                self.new_movies[i, d] = self.movies[i, d] - self.learning_rate * (updates_d[i, d] + self.lambda_M * self.movies[i, d])
    
    
    def print_latent_vectors(self):
        print "Users"
        for i in range(self.num_users):
            print i,
            for d in range(self.latent_d):
                print self.users[i, d],
            print
            
        print "Items"
        for i in range(self.num_movies):
            print i,
            for d in range(self.latent_d):
                print self.movies[i, d],
            print
    
    
    def save_latent_vectors(self):
        self.users.dump("training%sd_users.pickle" % self.latent_d)
        self.movies.dump("training%sd_movies.pickle" % self.latent_d)
    
    
if __name__ == "__main__":
    # configurations
    inputTrain = "../dataset/train.txt"
    # inputTrain = "./test_train.txt"
    outputPrediction = "./scores.txt"
    
    # load data
    myPredictor = PMFPredictor(inputTrain, latent_d=10)
    
    myPredictor.update()
    
    myPredictor.print_latent_vectors()
    myPredictor.save_latent_vectors()
