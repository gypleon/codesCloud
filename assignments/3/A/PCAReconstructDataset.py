#!/usr/bin/python

# Usage:
#

# Reference
#

import numpy as np


class PCAPredictor:
    def __init__(self, inputTrain, amount_of_eigs=5):
        ratings = []
        with file(inputTrain, 'r') as f:
            for line in f.readlines():
                (user, movie, rating) = line.split()
                ratings.append([user, movie, rating])
        (self.num_users, self.num_movies, _) = np.max(ratings, axis=0)
        self.rating_matrix = np.matrix()

    def fillInMatrix(self):
        pass

    def fillExpectation(self):
        pass

    def fillMaximization(self):
        pass

    def fillConvergence(self):
        pass

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
    amount_of_eigs = 5
    output = "./scores-%d.txt" % (amount_of_eigs)
    # load train and test data
    myPredictor = PCAPredictor(input_train, amount_of_eigs)
    # construct original matrix with missing values (the scores we are going to predict)
    myPredictor.fillInMatrix()
    # initial parameters

    # generate prediction results
    myPredictor.outputPrediction(input_test, output)

if __name__ == "__main__":
    main()
