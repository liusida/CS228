from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os, shutil
import glob
import easy3d

digit=4
fnames = glob.glob("Del6/userData/*_train%s.p"%digit)
fname = fnames[0]
print(fname)

with open(fname, "rb") as fp:
    data = pickle.load(fp)

index=1
# hand[finger, bone, xyzxyz]
finger_colors = ["#000055", "#111155", "#222255", "#333355", "#444455"]
fig, (ax) = plt.subplots(nrows=1, ncols=1, figsize=[14,5], subplot_kw=dict(projection='3d'))
if False:
    for finger in range(5):
        for bone in range(4):
            ax.plot(xs=data[finger,bone,::3,index], ys=data[finger,bone,1::3,index], zs=data[finger,bone,2::3,index], color=finger_colors[finger], lw=6-bone)

def data_to_base_tips(data):
    assert( data.shape[0] == 5 and data.shape[1] == 4 and data.shape[2] == 6 )
    # print(data.shape)
    data = np.moveaxis(data, 2, 0)
    # print(data.shape)
    data = data.reshape(6,-1)
    # print(data.shape)
    base = data[0:3,:]
    # print(base.shape)
    tip = data[3:6,:]
    # print(tip.shape)
    return base,tip

def base_tips_to_data(base, tip):
    assert( base.shape[0] == 3 and tip.shape[0] == 3 )
    data = np.concatenate((base, tip), axis=0)
    # print(data.shape)
    data = data.reshape(6,5,4,-1)
    # print(data.shape)
    data = np.moveaxis(data, 0, 2)
    # print(data.shape)
    return data

def get_key_points(data):
    # index finger, metacarpal(palm), base
    finger = 1; bone = 0; is_tip = 0
    point1 = (data[finger, bone, is_tip*3:is_tip*3+3, index] )
    # index finger, metacarpal(palm), tip
    finger = 1; bone = 0; is_tip = 1
    point2 = (data[finger, bone, is_tip*3:is_tip*3+3, index] )
    # baby finger, metacarpal(palm), tip
    finger = 4; bone = 0; is_tip = 1
    point3 = (data[finger, bone, is_tip*3:is_tip*3+3, index] )
    # ring finger, tip
    finger = 3; bone = 3; is_tip = 1
    point4 = (data[finger, bone, is_tip*3:is_tip*3+3, index] )

    return np.array([point1, point2, point3, point4])

view_scale = 1

ax.scatter(0,0,0,s=100)
ax.plot([0,view_scale],[0,0],[0,0],label='x', color='red')
ax.plot([0,0],[0,view_scale],[0,0],label='y', color='green')
ax.plot([0,view_scale],[0,view_scale],[0,0],label='xy', color='gray')
ax.plot([0,0],[0,0],[0,view_scale],label='z', color='blue')

p = get_key_points(data)
print(p)
# Prepare a sequence of transformation
# Step 1, move point 1 to origin
T1 = easy3d.matrix_translation(dx=-p[0,0], dy=-p[0,1], dz=-p[0,2])
# Step 2.1, rotate along x-axis to move point 2 to x-y plane
# sin(theta) = z / sqrt(y^2+z^3)
theta = -np.arctan((p[1,2]-p[0,2])/(p[1,1]-p[0,1]))
T2 = easy3d.matrix_rotate(degree=theta, axis=0)
# Step 2.2, rotate along z-axis to move point 2 to y axis
# sin(theta) = sqrt(y^2+z^2) / sqrt(x^2+y^2+z^2)
theta = -np.arctan((p[1,0]-p[0,0])/np.linalg.norm(p[1,1:3]-p[0,1:3]))
T3 = easy3d.matrix_rotate(degree=theta, axis=2)
# step 4, scale point1 - point2 distance to 1
scale = 1/np.linalg.norm(p[1]-p[0])
T4 = easy3d.matrix_scale(scale, scale, scale)

transform_matrics = [T1,T2,T3,T4]
base, tip = data_to_base_tips(data)
new_base = easy3d.transform(base, transform_matrics)
new_tip = easy3d.transform(tip, transform_matrics)
data = base_tips_to_data(new_base, new_tip)

p = get_key_points(data)
# step 3, rotate point 3 to x-y plane

theta = np.arctan(p[2,2]/p[2,0])
T5 = easy3d.matrix_rotate(degree=theta, axis=1)

transform_matrics = [T5]
base, tip = data_to_base_tips(data)
new_base = easy3d.transform(base, transform_matrics)
new_tip = easy3d.transform(tip, transform_matrics)
data = base_tips_to_data(new_base, new_tip)

# Step 5, mirror if needed
p1 = get_key_points(data)
print(p1)
if (p1[1,1]<0): #need turn up side down
    T6 = easy3d.matrix_mirror(axis=1)
    transform_matrics = [T6]
    base, tip = data_to_base_tips(data)
    new_base = easy3d.transform(base, transform_matrics)
    new_tip = easy3d.transform(tip, transform_matrics)
    data = base_tips_to_data(new_base, new_tip)

p1 = get_key_points(data)
if (p1[3,2]<0): #need mirror
    T7 = easy3d.matrix_mirror(axis=2)
    transform_matrics = [T7]
    base, tip = data_to_base_tips(data)
    new_base = easy3d.transform(base, transform_matrics)
    new_tip = easy3d.transform(tip, transform_matrics)
    data = base_tips_to_data(new_base, new_tip)

p1 = get_key_points(data)
if (p1[2,0]<0): #need mirror
    T8 = easy3d.matrix_mirror(axis=0)
    transform_matrics = [T8]
    base, tip = data_to_base_tips(data)
    new_base = easy3d.transform(base, transform_matrics)
    new_tip = easy3d.transform(tip, transform_matrics)
    data = base_tips_to_data(new_base, new_tip)

## TODO: use one hand, summarize all matrix, do transform in one step.

for finger in range(5):
    for bone in range(4):
        ax.plot(xs=data[finger,bone,::3,index], ys=data[finger,bone,1::3,index], zs=data[finger,bone,2::3,index], color=finger_colors[finger], lw=1)


ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

ax.set_xlim([-view_scale,view_scale])
ax.set_ylim([-view_scale,view_scale])
ax.set_zlim([-view_scale,view_scale])
ax.view_init(elev=90, azim=-90)
plt.show()

