# Conventions:
#
# A Matrix: M
# | a_11 a_12 |
# | a_21 a_22 |
#
# An array: a
# a[0,1] = a_12
# a[1,0] = a_21
#
# A set of n 3D points: p
# p.shape = [3, n]
#
# Transformation always dot matrix on the left:
# A x = b
# or, M p = p_new
#
# Rotation is to the counter-clock wise
#
# Best Practice:
# Step 1. Describe the transformation as several rotation, translation, and scale
# Step 2. Get all transformational matrics T1, T2, T3 by calling matrix_xxx one by one
# Step 3. Use transform(data, [T1, T2, T3]) to do transformation in one step.
#
import numpy as np

def matrix_rotate(degree=0.5*np.pi, axis=0):
    sin = np.sin(degree)
    cos = np.cos(degree)
    if axis==0:
        A = np.array([
            [1,  0,    0,  0],
            [0, cos, -sin, 0],
            [0, sin,  cos, 0],
            [0,  0,    0,  1]
        ])
    elif axis==1:
        A = np.array([
            [ cos, 0, sin, 0],
            [  0,  1,  0,  0],
            [-sin, 0, cos, 0],
            [  0,  0,  0,  1]
        ])
    elif axis==2:
        A = np.array([
            [cos, -sin, 0,  0],
            [sin,  cos, 0,  0],
            [ 0,    0,  1,  0],
            [ 0,    0,  0,  1]
        ])
    return A

def matrix_translation(dx=0, dy=0, dz=0):
    A = np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0,  1]
    ])
    return A

def matrix_scale(sx=1, sy=1, sz=1):
    A = np.array([
        [sx, 0,  0, 0],
        [0, sy,  0, 0],
        [0,  0, sz, 0],
        [0,  0,  0, 1]
    ])
    return A

def matrix_mirror(axis=0):
    if axis==0:
        A = np.array([
            [-1, 0, 0, 0 ],
            [ 0, 1, 0, 0 ],
            [ 0, 0, 1, 0 ],
            [ 0, 0, 0, 1 ]
        ])
    elif axis==1:
        A = np.array([
            [ 1, 0, 0, 0 ],
            [ 0,-1, 0, 0 ],
            [ 0, 0, 1, 0 ],
            [ 0, 0, 0, 1 ]
        ])
    else:
        A = np.array([
            [ 1, 0, 0, 0 ],
            [ 0, 1, 0, 0 ],
            [ 0, 0,-1, 0 ],
            [ 0, 0, 0, 1 ]
        ])
    return A

def transform(data, matrics):
    A = matrics[-1]
    for i in range(len(matrics)-2, -1, -1):
        A = np.matmul( A, matrics[i] )
    
    d = np.concatenate((data, np.ones(shape=(1,data.shape[1]))), axis=0)
    d = np.matmul(A, d)
    d = d[0:3,:]
    return d


if __name__ == "__main__":

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np
    import pickle
    import os, shutil
    import glob

    def ball( origin=(0,0), radius=10, epsilon=0.01 ):
        data = []
        for x in range(-radius, radius):
            for y in range(-radius, 0):
                for z in range(-radius,0):
                    e = radius - np.linalg.norm([x,y,z])
                    if e<epsilon and e>-epsilon:
                        data.append([x,y,z])
        return np.array(data).T
    def draw(data, ax):
        lim = [-20,20]
        ax.set_xlim(lim)
        ax.set_ylim(lim)
        ax.set_zlim(lim)
        ax.scatter(xs=data[0,:], ys=data[1,:], zs=data[2,:])
        ax.view_init(90, 0)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        
    data = ball(epsilon=0.3)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[14,5], subplot_kw=dict(projection='3d'))
    draw(data, axes[0])
    A = matrix_rotate(degree=0.1*np.pi, axis=2)
    #C = translation_matrix(dx=20)
    B = matrix_mirror(axis=1)
    data = transform(data, [A])
    draw(data, axes[1])
    plt.show()


