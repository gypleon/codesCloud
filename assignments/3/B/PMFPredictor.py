#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
    INSTRUCTION:
        Please configure parameters in __main__, 
        especially the configurable variable "trainFlag", which is the SWITCH between TRAINING_MODE and PREDICTION_MODE.
        TRAINING_MODE will generate two files for User_Feature_Model and Movie_Feature_Model respectively, which could be used for prediction.
        PREDICTION_MODE is based on the saved Model_Files
'''

import numpy as np
import time
import pickle

class PMFPredictor:
    def __init__(self, inputTrain, num_features=5, train=True, thresholdLikelihood=0.1, thresholdLearningRate=1e-5):
        self.num_features = num_features
        # initialize
        self.learning_rate = .0001
        self.threshold_likelihood = thresholdLikelihood
        self.threshold_learning_rate = thresholdLearningRate
        
        if train:
            self.ratings = np.array(self.loadData(inputTrain))
            self.converged = False
            
            self.num_users = int(np.max(self.ratings[:, 0]))
            self.num_movies = int(np.max(self.ratings[:, 1]))
            
            self.users = np.random.random((self.num_users, self.num_features))
            self.movies = np.random.random((self.num_movies, self.num_features))

            self.sigma = np.std(self.ratings, axis=0)[2]
            self.lambda_U = 0.1
            self.lambda_M = 0.1
            
            self.new_users = np.random.random((self.num_users, self.num_features))
            self.new_movies = np.random.random((self.num_movies, self.num_features))
    
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
                    print "loading data %d" % count
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

        # compute squared error
        error = 0
        for rating_tuple in self.ratings:
            i, j, rating = rating_tuple
            r_hat = np.sum(users[i-1] * movies[j-1])
            error += (rating - r_hat)**2

        # compute regularization
        users_i_norm = 0
        movies_j_norm = 0
        for i in range(self.num_users):
            for d in range(self.num_features):
                users_i_norm += users[i, d]**2
        for i in range(self.num_movies):
            for d in range(self.num_features):
                movies_j_norm += movies[i, d]**2

        return error + self.lambda_U * users_i_norm + self.lambda_M * movies_j_norm

    def train(self):
        updated_users = np.zeros((self.num_users, self.num_features))
        updated_movies = np.zeros((self.num_movies, self.num_features))
        
        while (not self.converged):
            cur_likelihood = self.objectiveFunc()
            print "[", time.ctime(), "]", "current likelihood =", cur_likelihood, " learning rate =", self.learning_rate, " lambda U&M =", self.lambda_U, " ", self.lambda_M
            self.updates_test(updated_users, updated_movies)
            
            new_likelihood = self.objectiveFunc(self.new_users, self.new_movies)
            
            if new_likelihood < cur_likelihood:
                # on the right direction, speed up
                self.updates()
                self.learning_rate *= 1.25
                if cur_likelihood - new_likelihood < self.threshold_likelihood:
                # convergence threshold for likelihood
                    self.converged = True
            else:
                # just passed the objective, slow down
                self.learning_rate *= 0.5
                pass
            if self.learning_rate <= self.threshold_learning_rate:
                # convergence threshold for learning rate
                self.converged = True
    
    def updates(self):
        for i in range(self.num_users):
            for d in range(self.num_features):
                self.users[i, d] = self.new_users[i, d]
        for i in range(self.num_movies):
            for d in range(self.num_features):
                self.movies[i, d] = self.new_movies[i, d]
    
    def updates_test(self, updated_users, updated_movies):
        for rating_tuple in self.ratings:
            (i, j, rating) = rating_tuple
            # r_hat is the predicted rating for user i on movie j
            r_hat = np.sum(self.users[i-1] * self.movies[j-1])
            # update each feature
            for d in range(self.num_features):
                updated_movies[j-1, d] += self.users[i-1, d] * (r_hat - rating)
                updated_users[i-1, d] += self.movies[j-1, d] * (r_hat - rating)
        for i in range(self.num_users):
            for d in range(self.num_features):
                self.new_users[i, d] = self.users[i, d] - self.learning_rate * (updated_users[i, d] + self.lambda_U * self.users[i, d])
        for i in range(self.num_movies):
            for d in range(self.num_features):
                self.new_movies[i, d] = self.movies[i, d] - self.learning_rate * (updated_movies[i, d] + self.lambda_M * self.movies[i, d])
    
    def save_model(self, trainedUsers, trainedMovies):
        self.users.dump(trainedUsers)
        self.movies.dump(trainedMovies)

    def predict(self, trainedUsers, trainedMovies, inputTest, output):
        with file(trainedUsers, 'r') as f:
            users = pickle.load(f)
        with file(trainedMovies, 'r') as f:
            movies = pickle.load(f)
        predicted_matrix = np.matrix(users) * np.matrix(movies).transpose()
        predicted_matrix = np.array(predicted_matrix)
        predicted_ratings = []
        with file(inputTest, 'r') as f:
            for line in f.readlines():
                (user, movie) = line.strip().split()
                predicted_ratings.append(predicted_matrix[int(user)-1][int(movie)-1])
        with file(output, 'w') as f:
            for rating in predicted_ratings:
                f.write("%.3f\n" % rating)
    
if __name__ == "__main__":
    # configurations
    # latent features
    numFeatures = 10
    thresholdLikelihood = 0.1
    thresholdLearningRate = 1e-5
    # path of input dataset
    inputTrain = "../dataset/train.txt"
    inputTest = "../dataset/test.txt"
    # path of output scores
    outputPrediction = "./scores.txt"
    # path of saved model
    trainedUsers = "./trained_users_%sfeatures.pickle" % numFeatures
    trainedMovies = "./trained_movies_%sfeatures.pickle" % numFeatures

    # TODO: choose a operation mode:
    # True - training model, False - load saved model and predict
    # trainFlag = True
    trainFlag = False

    # load data
    myPredictor = PMFPredictor(inputTrain, num_features=numFeatures, \
            train=trainFlag, thresholdLikelihood=thresholdLikelihood, thresholdLearningRate=thresholdLearningRate)
    if trainFlag:
        # train model 
        myPredictor.train()
        # save model
        myPredictor.save_model(trainedUsers, trainedMovies)
    else:
        # predict scores based on trained model
        myPredictor.predict(trainedUsers, trainedMovies, inputTest, outputPrediction)
