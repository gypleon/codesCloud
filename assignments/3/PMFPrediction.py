#!/usr/bin/python
#-*- coding:utf-8 -*-

import pandas
import numpy as np
# import pickle

class PMFPredictor:
    """
    Attributes
    * latent_d
    * learning_rate, regularization_strength
    * ratings, users, items
    * num_users, num_items
    * new_ratings, new_items (probably don't need these)
    
    Methods
    * likelihood
    * update
    * apply_updates
    * try_updates
    * undo_updates
    * print_latent_vectors
    * save_latent_vectors
    """
    
    def __init__(self, inputTrain, latent_d=1, verbose=True):
        self.latent_d = latent_d
        self.learning_rate = .0001 # alpha
        self.regularization_strength = 0.1 # lambda
        
        self.ratings = np.array(self.loadData(inputTrain))
        self.converged = False
        
        self.num_users = int(np.max(self.ratings[:, 0]) + 1)
        self.num_items = int(np.max(self.ratings[:, 1]) + 1)
        
        if verbose:
            print (self.num_users, self.num_items, self.latent_d)
            print self.ratings
        
        self.users = np.random.random((self.num_users, self.latent_d))
        self.items = np.random.random((self.num_items, self.latent_d))
        
        self.new_users = np.random.random((self.num_users, self.latent_d))
        self.new_items = np.random.random((self.num_items, self.latent_d))
    
    
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


    def likelihood(self, users=None, items=None):
        if users is None:
            users = self.users
        if items is None:
            items = self.items

        # empirical risk term            
        sq_error = 0
        for rating_tuple in self.ratings:
            if len(rating_tuple) == 3:
                (i, j, rating) = rating_tuple
                weight = 1
            elif len(rating_tuple) == 4:
                (i, j, rating, weight) = rating_tuple
            
            r_hat = np.sum(users[i] * items[j])
            
            sq_error += weight * (rating - r_hat)**2
        
        # regularization term
        L2_norm = 0
        for i in range(self.num_users):
            for d in range(self.latent_d):
                L2_norm += users[i, d]**2
        
        for i in range(self.num_items):
            for d in range(self.latent_d):
                L2_norm += items[i, d]**2
        
        return -sq_error - self.regularization_strength * L2_norm
        
        
    def update(self):
        # updates_o holds updates to the latent features of users
        # updates_d holds updates to the latent features of items
        updates_o = np.zeros((self.num_users, self.latent_d))
        updates_d = np.zeros((self.num_items, self.latent_d))
        
        # batch update: run through all ratings for each iteration
        for rating_tuple in self.ratings:
            if len(rating_tuple) == 3:
                (i, j, rating) = rating_tuple
                weight = 1
            elif len(rating_tuple) == 4:
                (i, j, rating, weight) = rating_tuple
            
            # r_hat is the predicted rating for user i on item j
            r_hat = np.sum(self.users[i] * self.items[j])
            
            # update each feature according to weight accurracy
            for d in range(self.latent_d):
                updates_o[i, d] += self.items[j, d] * (rating - r_hat) * weight
                updates_d[j, d] += self.users[i, d] * (rating - r_hat) * weight
        
        # converge if likelihood changes by less than .1 or if learning rate goes below 1e-10
        # speed up by 1.25x if improving, slow down by 0.5x if not improving
        while (not self.converged):
            initial_lik = self.likelihood()
            
            print "  likelihood =", self.likelihood()
            print "  setting learning rate =", self.learning_rate
            # apply updates to self.new_users and self.new_items
            self.try_updates(updates_o, updates_d)
            
            final_lik = self.likelihood(self.new_users, self.new_items)
            
            # if the new latent feature vectors are better, keep the updates, and increase the learning rate (i.e. momentum)
            if final_lik > initial_lik:
                self.apply_updates(updates_o, updates_d)
                self.learning_rate *= 1.25
                
                if final_lik - initial_lik < .1:
                    self.converged = True
            else:
                self.learning_rate *= .5
                self.undo_updates()
            
            if self.learning_rate < 1e-10:
                self.converged = True
        
        return not self.converged
    
    
    def apply_updates(self, updates_o, updates_d):
        for i in range(self.num_users):
            for d in range(self.latent_d):
                self.users[i, d] = self.new_users[i, d]
        
        for i in range(self.num_items):
            for d in range(self.latent_d):
                self.items[i, d] = self.new_items[i, d]
    
    
    def try_updates(self, updates_o, updates_d):
        """
        Update self.new_users and self.new_items with updates calculated with batch GD
        """
        alpha = self.learning_rate
        beta = -self.regularization_strength
        
        for i in range(self.num_users):
            for d in range(self.latent_d):
                self.new_users[i, d] = self.users[i, d] + \
                                        alpha * (beta * self.users[i, d] + updates_o[i, d])
        for i in range(self.num_items):
            for d in range(self.latent_d):
                self.new_items[i, d] = self.items[i, d] + \
                                        alpha * (beta * self.items[i, d] + updates_d[i, d])
    
    
    def undo_updates(self):
        # Don't need to do anything here
        pass
    
    
    def print_latent_vectors(self):
        print "Users"
        for i in range(self.num_users):
            print i,
            for d in range(self.latent_d):
                print self.users[i, d],
            print
            
        print "Items"
        for i in range(self.num_items):
            print i,
            for d in range(self.latent_d):
                print self.items[i, d],
            print
    
    
    def save_latent_vectors(self):
        self.users.dump("training%sd_users.pickle" % self.latent_d)
        self.items.dump("training%sd_items.pickle" % self.latent_d)
    
    
if __name__ == "__main__":
    # configurations
    # inputTrain = "./dataset/train.txt"
    inputTrain = "./test_train.txt"
    outputPrediction = "./scores.txt"
    
    myPredictor = PMFPredictor(inputTrain, latent_d=10)
    
    liks = []
    while (myPredictor.update()):
        lik = myPredictor.likelihood()
        liks.append(lik)
        print "L=", lik
        pass
    
    myPredictor.print_latent_vectors()
    myPredictor.save_latent_vectors()
