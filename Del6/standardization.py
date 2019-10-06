import numpy as np
import show

# input data shape should be: (5,4,6,n)
# return data shape is: (5,4,6,n)
def do(data):
    if len(data.shape)==3:
        data = data.reshape(5,4,6,1)

    # input shape (5,4,6) 
    # output shape (3,5,4,2)
    def data_to_hand(data, inv=False):
        if not inv:
            assert( data.shape[0] == 5 and data.shape[1] == 4 and data.shape[2] == 6 )
            data = data.reshape(5,4,2,3)
            data = np.moveaxis(data, 3, 0)
            return data
        else:
            assert( data.shape[0] == 3 and data.shape[1] == 5 and data.shape[2] == 4 and data.shape[3] == 2 )
            data = np.moveaxis(data, 0, 3)
            data = data.reshape(5,4,6)
            return data

    def get_key_points(data):
        # index finger, metacarpal(palm), base
        finger = 1; bone = 0; is_tip = 0
        point1 = hand[:, finger, bone, is_tip]
        # index finger, metacarpal(palm), tip
        finger = 1; bone = 0; is_tip = 1
        point2 = hand[:, finger, bone, is_tip]
        # baby finger, metacarpal(palm), tip
        finger = 4; bone = 0; is_tip = 1
        point3 = hand[:, finger, bone, is_tip]
        # thumb, metacarpal, tip
        finger = 0; bone = 0; is_tip = 1
        point4 = hand[:, finger, bone, is_tip]

        return np.array([point1, point2, point3, point4]).T

    def ab(a, b):
        n = np.linalg.norm([a,b])
        #print(a,b)
        if n==0:
            print("Error: divide by zero.")
            #print(np.sum(data[:,:,:]))
            #show.show_hand(data[:,:,:])
            #exit()
        a = a / n
        b = b / n
        return a, b

    ret = []
    for index in range(data.shape[-1]):
        hand = data_to_hand(data[:,:,:,index])
        p1 = get_key_points(hand)
        # Step 1. Move index finger metacarpal(palm) bone base to origin
        for i in range(3):
            hand[i,:] = hand[i,:] - p1[i,0]
        p1 = get_key_points(hand)

        # Step 3. Rotate index finger metacarpal(palm) bone to +x-y plane
        y,z = ab(p1[1,1], p1[2,1])
        T_rotate = np.array([
            [ 1, 0, 0],
            [ 0, y, z],
            [ 0,-z, y]
            ])
        hand = np.matmul(T_rotate, hand.reshape(3,-1)).reshape(3,5,4,2)
        p1 = get_key_points(hand)

        # Step 4. Rotate index finger metacarpal(palm) bone to +y axis
        x,y = ab(p1[0,1], p1[1,1])
        T_rotate = np.array([
            [y, -x, 0],
            [x, y, 0],
            [0, 0, 1]
            ])
        hand = np.matmul(T_rotate, hand.reshape(3,-1)).reshape(3,5,4,2)
        p1 = get_key_points(hand)

        # Step 5. Keep index finger on +y axis, Rotate another bone (baby finger, metacarpal(palm), tip) to +x-y plane
        x,z = ab(p1[0,2], p1[2,2])
        T_rotate = np.array([
            [x,  0, z],
            [0,  1, 0],
            [-z, 0, x]
        ])
        hand = np.matmul(T_rotate, hand.reshape(3,-1)).reshape(3,5,4,2)
        p1 = get_key_points(hand)

        # Step 6. Mirror Adjust Left-Right hand, depending on the z value of 4-th point ring finger, tip
        if p1[2,3]<0:
            #print("mirror")
            hand[2,:,:,:] = - hand[2,:,:,:]

        # Step 7. Normalize scale set index finger metacarpal(palm) bone = 1
        hand = hand/np.linalg.norm(p1[1]-p1[0])
        #print(hand.shape)
        #p1 = get_key_points(hand)

        #print(p1)
        ret.append(data_to_hand(hand, inv=True))
    ret = np.array(ret)
    
    data = np.moveaxis(ret, 0, 3)
    return data