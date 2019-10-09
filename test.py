hand = get_one_hand() # So we have points of a hand, the shape is (3,5,4,2), x-y-z 3 coordinates and 5 fingers each hand, 4 bones each finger, 2 ends of each bone, in total 40 points.

p1 = get_key_points(hand) # So this is 4 points we want to use to standardize. Those key points should relatively stable, such as the metacarpal bones, which we cannot move them a lot even if we want to. The shape is (3,4), x-y-z 3 coordinates and 4 points (index finger, metacarpal, base; index finger, metacarpal, tip; baby finger, metacarpal, tip; thumb, metacarpal, tip).

# Step 1. Move index finger metacarpal(palm) bone base to origin .
for i in range(3): # move x,y,z axes seperately in this loop
    hand[i,:] = hand[i,:] - p1[i,0]
p1 = get_key_points(hand) # We need to know where those key points after last step.

# Step 2. Rotate index finger metacarpal(palm) bone to +x-y plane
y,z = ab(p1[1,1], p1[2,1]) # p1[1,1] is the y coordinate and p1[2,1] is the z coordinate, we want to rotate to let them fall into +x-y plane, but we need to normalize them, so no scaling will be introduced in this step. here ab(y1,z1) = y1/norm, z1/norm.
T_rotate = np.array([
    [ 1, 0, 0],
    [ 0, y, z],
    [ 0,-z, y]
    ]) # This matrix is saying that we fix every x coordinate, and rotate y and z.
hand = np.matmul(T_rotate, hand.reshape(3,-1)).reshape(3,5,4,2)
p1 = get_key_points(hand)
# Step 3. Rotate index finger metacarpal(palm) bone to +y axis
x,y = ab(p1[0,1], p1[1,1])
T_rotate = np.array([
    [y, -x, 0],
    [x, y, 0],
    [0, 0, 1]
    ])
hand = np.matmul(T_rotate, hand.reshape(3,-1)).reshape(3,5,4,2)
p1 = get_key_points(hand)
# Step 4. Keep index finger on +y axis, Rotate another bone (baby finger, metacarpal(palm), tip) to +x-y plane
x,z = ab(p1[0,2], p1[2,2])
T_rotate = np.array([
    [x,  0, z],
    [0,  1, 0],
    [-z, 0, x]
])
hand = np.matmul(T_rotate, hand.reshape(3,-1)).reshape(3,5,4,2)
p1 = get_key_points(hand)
# Step 6. Mirror Adjust Left-Right hand, depending on the z value of 4-th point thumb, metacarpal, tip
if p1[2,3]<0:
    hand[2,:,:,:] = - hand[2,:,:,:]
# Step 7. Normalize scale set index finger metacarpal(palm) bone = 1
hand = hand/np.linalg.norm(p1[1]-p1[0])
