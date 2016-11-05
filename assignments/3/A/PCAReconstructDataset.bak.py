#!/usr/bin/python

# Usage:
#

# Reference
#

import numpy as np


def loadMatrix():

def expectation():

def maximization():

def convergenceCheck():

def outputPrediction():

def main():
    # configuration
    inputTrain = "../dataset/train.txt"
    inputTest = "../dataset/test.txt"
    amountOfEigenv = 5
    output = "scores-%d.txt" % (amountOfEigenv)
    # load train and test data
    # construct original matrix with missing values (the scores we are going to predict)
    matrix = loadMatrix(inputTrain, inputTest)
    # initial parameters

    # E-M loop
    while( convergenceCheck()):
        expectation()
        maximization()
    # generate prediction results
    outputPrediction()

if __name__ == "__main__":
    main()
