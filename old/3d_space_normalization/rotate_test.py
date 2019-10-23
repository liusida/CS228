# Note:

# Translation:
#                | 1 0 0 dx |
# T(dx,dy,dz) =  | 0 1 0 dy |
#                | 0 0 1 dz |
#                | 0 0 0 1  |

# Scaling:
#                | sx  0  0  0 |
# S(sx,sy,sz) =  |  0 sy  0  0 |
#                |  0  0 sz  0 |
#                |  0  0  0  1 |

# Rotating:
#         | 1      0        0   0 |
# Rx(A) = | 0  cos A   -sin A   0 |
#         | 0  sin A    cos A   0 |
#         | 0      0        0   1 |
 
#         | cos A   0   sin A   0 |
# Ry(A) = |     0   1       0   0 |
#         | -sin A  0   cos A   0 |
#         |     0   0       0   1 |

#         | cos A  -sin A   0   0 |
# Rz(A) = | sin A   cos A   0   0 |
#         |     0       0   1   0 |
#         |     0       0   0   1 |


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os, shutil
import glob

class Easy3D:
    def __init__(self):
        pass
    def rotate(self, data, degree, axis=0):
        return data
    def translate(self, data, dx, dy, dz):
        return data
    def scale(self, data, scale):
        return data

def ball( origin=(0,0), radius=10, epsilon=0.01 ):
    data = []
    for x in range(-radius, radius):
        for y in range(-radius, radius):
            for z in range(-radius,0):
                e = radius - np.linalg.norm([x,y,z])
                if e<epsilon and e>-epsilon:
                    data.append([x,y,z])
    return np.array(data)

def draw(data, ax):
    lim = [-20,20]
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_zlim(lim)
    ax.scatter(xs=data[:,0], ys=data[:,1], zs=data[:,2])
    ax.view_init(20, 120)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")


data = ball(epsilon=0.3)
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[14,5], subplot_kw=dict(projection='3d'))
ax = axes[0]
draw(data, ax)

Rotate_Degree = 0.2 * np.pi
#         | cos A   0   sin A   0 |
# Ry(A) = |     0   1       0   0 |
#         | -sin A  0   cos A   0 |
#         |     0   0       0   1 |
A = [
    [np.cos(Rotate_Degree), 0, np.sin(Rotate_Degree), 0],
    [0, 1, 0, 0],
    [-np.sin(Rotate_Degree), 0, np.cos(Rotate_Degree), 0],
    [0, 0, 0, 1]
]

d = np.concatenate((data, np.ones(shape=(data.shape[0],1))), axis=1)
print(d)
data = d.dot(A)[:,0:3]

draw(data, axes[1])

plt.show()