import numpy as np

X = np.arange(5*4*6).reshape(5,4,6)
print(X)
X = np.delete(X,[1,2],1)
print(X.shape)
print(X)
