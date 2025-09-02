# Analyse the images to find the position of each LED

# Input:  a positions_camera_frame.npy file (2D coords for each camera frame)
# Output: a positions.csv file (3D coords)

import numpy as np

NO_LEDS = 300
scan_name = 'scan2'

# Open the positions_camera_frame.npy file
positions_camera_frame = np.load(f'{scan_name}/positions_camera_frame.npy')

# Create an empty array for the 3D positions
positions_global = np.zeros((NO_LEDS, 3)) 

# Convert the set of 2D coordinates into 3D coordinates
for i in range(NO_LEDS):
    coords = positions_camera_frame[:,i,:]

    xF, yF = coords[0]
    xB, yB = coords[2]
    xL, yL = coords[1]
    xR, yR = coords[3]

    # Calculate the 3D coordinates
    # X
    # # y = (yL + yR) / 2
    # z = (xF - xB) / 2
    # z = (yL - yR) / 2

    X = [xF, 480 - xB] # multiple ways to calculate
    X = X[X != 0] # filter out zeros
    if not X:
        print('Couldn\'t figure out position of LED', i)
        positions_global[i] = None
        continue
    else:
        X = np.mean(X) # take the average 

    Y = [xL, 480 - xR]
    Y = Y[Y != 0]
    if not Y:
        print('Couldn\'t figure out position of LED', i)
        positions_global[i] = None
        continue
    else:
        Y = np.mean(Y) 

    Z = [yF, yB, yL, yR]
    Z = Z[Z != 0]
    if not Z:
        print('Couldn\'t figure out position of LED', i)
        positions_global[i] = None
        continue
    else:
        Z = np.mean(Z)

    print(X, Y, Z)
    
    # Save position
    positions_global[i] = [X, Y, Z]

    

# Save the positions to a CSV file
np.savetxt(f'{scan_name}/positions.csv', positions_global, delimiter=',')