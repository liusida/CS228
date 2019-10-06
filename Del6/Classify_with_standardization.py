import sys, os
sys.path.insert(0, './')

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import numpy as np
import pickle
import os, shutil

from knn import KNN
from knn_backup import KNN as KNN_backup

import standardization
import show

#Read in dataset for 0 1 2 3 4 5 6 7 8 9
train_test = ['train', 'test']
import glob
train_sets = [0] * 10
test_sets = [0] * 10
for t in train_test:
    fnames = glob.glob("Del6/userData/good/*_%s*.p"%(t))
    for fname in fnames:
        if (type(test_sets[int(fname[-3])])==int and t=="test") or (type(train_sets[int(fname[-3])])==int and t=="train"):
            print("reading "+fname, int(fname[-3]))
            with open(fname, "rb") as f:
                if t=="test":
                    test_sets[int(fname[-3])] = pickle.load(f)
                else:
                    train_sets[int(fname[-3])] = pickle.load(f)
        
# Slow way
def ReshapeData2( set1, set2 ):
    X = np.zeros((2000,5*4*6), dtype='f')
    for row in range(0,1000):
        col = 0
        for fingure in range(5):
            for bone in range(4):
                for tipbasexyz in range(6):
                    X[row, col] = set1[fingure, bone, tipbasexyz, row]
                    X[row+1000, col] = set2[fingure, bone, tipbasexyz, row]
                    col += 1
    Y = np.zeros(2000, dtype='i')
    for row in range(0,1000):
        Y[row] = 2
        Y[row+1000] = 3
    return X, Y

# Fastest way
def ReshapeData( sets, digits ):
    size = sets[0].shape[3]
    X = [ np.moveaxis(single_set, 3, 0) for single_set in sets]
    X = np.concatenate(X).reshape(len(digits)*size,-1)
    Y = [ np.array([single_digit]*size) for single_digit in digits]
    Y = np.concatenate(Y).flatten()
    return X, Y

def ReduceData(X):
    #X = np.delete(X,1,1)
    #X = np.delete(X,1,1)
    X = np.delete(X, obj=[1,2], axis=1)
    X = np.delete(X, obj=[0,1,2], axis=2)
    return X

def CenterData(X):
    allXCoordinates = X[:,:,0,:]
    meanValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanValue

    X[:,:,1,:] = X[:,:,1,:] - X[:,:,1,:].mean()
    X[:,:,2,:] = X[:,:,2,:] - X[:,:,2,:].mean()
    return X

# for i, dataset in enumerate(train_sets):
#     train_sets[i] = CenterData(ReduceData(train_sets[i]))
#     test_sets[i] = CenterData(ReduceData(test_sets[i]))
for i, dataset in enumerate(train_sets):
    print("Standardizing ", i)
    train_sets[i] = standardization.do(train_sets[i])
    test_sets[i] = standardization.do(test_sets[i])

trainX, trainY = ReshapeData( train_sets, range(10) )
testX, testY = ReshapeData( test_sets, range(10) )
print(testX.shape)
def SaveDataToPickle(var, fname):
    pickle_out = open("userData/"+fname,"wb")
    pickle.dump(var, pickle_out)
    pickle_out.close()

SaveDataToPickle([trainX, trainY, testX, testY], "KNN_dataset")

knn = KNN()
knn.Use_K_Of(15)
knn.Fit(trainX,trainY)
print('fitted.')

import time
start_time = time.time()
if False: # using KNN_backup
    great = 0
    for row in range(0,2000):
        prediction = knn.Predict(testX[row])
        if prediction==testY[row]:
            great += 1

else:
    print('start.')
    step_size = 1
    for i in range(0, testX.shape[0], step_size):
        predictions = knn.Predict(testX[i:i+step_size])
        great = np.sum(np.equal(predictions,testY[i:i+step_size]))
        print("accuracy:", (1.*great)/step_size)
        if great!=step_size:
            # Error occur
            print(predictions)
            print(testY[i:i+step_size])
            print(testX[i].shape)
            err = testX[i].reshape(5,4,6)
            show.show_hand(err, "err_%s.png"%time.time())
            #exit()

print("time: ", time.time()-start_time)

# First accuracy: 90.75%
# Second accuracy: 97.4%
# Third accuracy: 98.65%

pickle.dump(knn, open('Del6/userData/classifier_with_standardization.p','wb'))
