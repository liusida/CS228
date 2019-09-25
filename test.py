import numpy as np

X = np.arange(5)
X1 = np.arange(10,20).reshape(2,5)
print(X.shape)
Y = X-X1

print(Y)