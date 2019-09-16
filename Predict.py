from knn import KNN
import matplotlib.pyplot as plt
import numpy as np

knn = KNN()

knn.Load_Dataset("iris.csv")

trainX = knn.data[::2,1:3]
trainY = knn.target[::2]
testX = knn.data[1::2,1:3]
testY = knn.target[1::2]

colors = np.zeros((3,3),dtype='f') 
colors[0,:] = [1,0.5,0.5] 
colors[1,:] = [0.5,1,0.5] 
colors[2,:] = [0.5,0.5,1]

knn.Use_K_Of(15)
knn.Fit(trainX,trainY)

plt.figure()
[numItems,numFeatures] = knn.data.shape
for i in range(0,numItems/2):
    itemClass = int(trainY[i])
    currColor = colors[itemClass,:]
    plt.scatter(trainX[i,0],trainX[i,1],facecolor=currColor,s=50,lw=2,edgecolors='black')
for i in range(0,numItems/2):
    itemClass = int(testY[i])
    currColor = colors[itemClass,:]
    prediction = int( knn.Predict( testX[i,:] ) ) 
    edgeColor = colors[prediction,:]
    plt.scatter(testX[i,0],testX[i,1],facecolor=currColor,s=50,lw=2,edgecolors=edgeColor)
    
great = 0
for i in range(0,numItems/2):
    actualClass = testY[i] 
    prediction = knn.Predict(testX[i,:]) 
    if actualClass==prediction:
        great += 1
print("%d in %d"%(great,numItems/2))
print(2.*great/numItems*100)
plt.savefig("del04.png")
plt.show()

