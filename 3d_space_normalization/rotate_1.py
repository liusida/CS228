#
# When we get any dataset, the first step should be visualization.
# There probably are many bad data hiding in the dataset.
# Especially when you use a naive simple learning algorithmn.
#
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os, shutil
import glob
import easy3d
import standardization

fnames = glob.glob("Del6/userData/good/*_train*.p")
for fname in fnames:
    print(fname)
    pathname = fname[:-2]
    # if not os.path.exists(pathname):
    #     os.mkdir(pathname)
    if not os.path.exists(pathname+"_front/"):
        os.mkdir(pathname+"_front/")
    if not os.path.exists(pathname+"_side/"):
        os.mkdir(pathname+"_side/")
        


    with open(fname, "rb") as fp:
        data = pickle.load(fp)

    print(data.shape)

    finger_colors = ["#000055", "#111155", "#222255", "#333355", "#444455"]
    fig, (ax) = plt.subplots(nrows=1, ncols=1, figsize=[7,5], subplot_kw=dict(projection='3d'))

    visual_data = standardization.do(data[:,:,:,:])

    for index in range(5):
        ax.cla()

        hand = visual_data[:,:,:,index]

        if True:
            for finger in range(5):
                for bone in range(4):
                    ax.plot(xs=hand[finger,bone,::3], ys=hand[finger,bone,1::3], zs=hand[finger,bone,2::3], color=finger_colors[finger], lw=6-bone)


        view_scale=1

        ax.set_aspect("equal")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        ax.set_xlim([-view_scale,view_scale])
        ax.set_ylim([-view_scale,view_scale])
        ax.set_zlim([-view_scale,view_scale])
        ax.view_init(elev=90, azim=-90)
        plt.savefig(pathname+'_front/%.5d.png'%index)
        ax.view_init(elev=0, azim=0)
        plt.savefig(pathname+'_side/%.5d.png'%index)
        print(pathname+'/%.5d'%index)
        #plt.show()
        #exit()
