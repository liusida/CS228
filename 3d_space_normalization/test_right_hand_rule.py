import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import easy3d

np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)})

fig, (ax) = plt.subplots(nrows=1, ncols=1, figsize=[14,5], subplot_kw=dict(projection='3d'))
ax.scatter(0,0,0,s=5)
scale = 1
ax.plot([0,scale],[0,0],[0,0],label='x')
ax.plot([0,0],[0,scale],[0,0],label='y')
ax.plot([0,0],[0,0],[0,scale],label='z')

#p = np.array([[1,1,1], [-1,-3,-5]], dtype='f')
#p = np.array([[1,1,1], [1,3,5], [6,6,6]], dtype='f')
p = np.array([[ 92.15207 , 232.16725 , 119.165016],
 [ 70.99465 , 236.39908  , 48.830517],
 [134.34438 , 223.57175  , 54.424366],
 [109.30874 , 249.46292 , -39.37675 ]]
)


p1 = p.T
# p1.shape is (3,n)
print(p1)
for i in range(3):
    p1[i,:] = p1[i,:] - p1[i,0]
p1 = p1/np.linalg.norm(p[1]-p[0])


def ab(a, b):
    n = np.linalg.norm([a,b])
    a = a / n
    b = b / n
    return a, b

y,z = ab(p1[1,1], p1[2,1])
T_rotate_1 = np.array([
    [ 1, 0, 0],
    [ 0, y, z],
    [ 0,-z, y]
    ])
p1 = np.matmul(T_rotate_1, p1)

x,y = ab(p1[0,1], p1[1,1])
T_rotate_2 = np.array([
    [y, -x, 0],
    [x, y, 0],
    [0, 0, 1]
    ])
p1 = np.matmul(T_rotate_2, p1)

x,z = ab(p1[0,2], p1[2,2])
T_rotate_3 = np.array([
    [x,  0, z],
    [0,  1, 0],
    [-z, 0, x]
])
p1 = np.matmul(T_rotate_3, p1)

ax.plot(p1[0,0:2],p1[1,0:2],p1[2,0:2],lw=0.3)

ax.view_init(90,-90)
ax.set_aspect("equal")
plt.legend()
plt.show()