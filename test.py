import numpy as np

import matplotlib.pyplot as plt

axis1 = np.array([1,0])
axis2 = np.array([-1,1])
v = np.array([0,1])
# make a transformative matrix A
A = np.vstack((axis1, axis2)).T
# get inverse
A_1 = np.linalg.inv(A)
# A.dot is transformation
# A_1.dot is normalization

print(A)
v1 = A.dot(v)
print(v1)
v2 = A_1.dot(v1)
print(v2, v)

def plot_vector((x,y)):
    plt.plot([0,x], [0,y])

plot_vector(v1)
plot_vector(v)
plot_vector(axis1)
plot_vector(axis2)
plt.xlim([-2,2])
plt.ylim([-2,2])
plt.axis("equal")
plt.show()