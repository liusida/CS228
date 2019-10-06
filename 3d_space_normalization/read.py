from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os, shutil
import glob
import easy3d

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=[6,5], subplot_kw=dict(projection='3d'))

for digit in range(1):
    fnames = glob.glob("Del6/userData/Castrejon_Sanchez_test8.dat.p")
    fname = fnames[0]
    print(fname)

    with open(fname, "rb") as fp:
        data = pickle.load(fp)

    print(data.shape)

    #print(data[0,0,::3,0])
    index = np.random.randint(low=0, high=data.shape[3], dtype='i')
    finger_colors = ["#000055", "#111155", "#222255", "#333355", "#444455"]
    ax = axes
    print(ax)
    ax.set_aspect("equal")
    ax.set_title("%s_%d"%(fname,index))
    for finger in range(5):
        for bone in range(4):
            ax.plot(xs=data[finger,bone,::3,index], ys=data[finger,bone,1::3,index], zs=data[finger,bone,2::3,index], color=finger_colors[finger], lw=6-bone)

plt.show()