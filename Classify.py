import numpy as np
import pickle
import constants
import os, shutil

from knn import KNN
from knn_backup import KNN as KNN_backup

pickle_in = open("userData/train2.dat","rb")
train2 = pickle.load(pickle_in)
pickle_in.close()
pickle_in = open("userData/test2.dat","rb")
test2 = pickle.load(pickle_in)
pickle_in.close()
pickle_in = open("userData/train3.dat","rb")
train3 = pickle.load(pickle_in)
pickle_in.close()
pickle_in = open("userData/test3.dat","rb")
test3 = pickle.load(pickle_in)
pickle_in.close()

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
def ReshapeData( set1, set2 ):
    X1 = np.moveaxis(set1, 3, 0)
    X2 = np.moveaxis(set2, 3, 0)
    X = np.concatenate((X1, X2)).reshape(2000,-1)
    Y1 = np.array([2]*1000)
    Y2 = np.array([3]*1000)
    Y = np.concatenate((Y1, Y2)).flatten()
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

train2 = ReduceData(train2)
train3 = ReduceData(train3)
test2 = ReduceData(test2)
test3 = ReduceData(test3)

train2 = CenterData(train2)
train3 = CenterData(train3)
test2 = CenterData(test2)
test3 = CenterData(test3)


trainX, trainY = ReshapeData( train2, train3 )
testX, testY = ReshapeData( test2, test3 )

def SaveDataToPickle(var, fname):
    pickle_out = open("userData/"+fname,"wb")
    pickle.dump(var, pickle_out)
    pickle_out.close()

SaveDataToPickle([trainX, trainY, testX, testY], "KNN_dataset")

knn = KNN()
knn.Use_K_Of(15)
knn.Fit(trainX,trainY)

predictions = knn.Predict1(testX)
great = np.sum(np.equal(predictions,testY))
print("accuracy:", great/2000.)

# First accuracy: 90.75%
# Second accuracy: 97.4%
# Third accuracy: 98.65%