import numpy as np

scan_name = 'scan2'
angles = [
    0,
    90,
    180,
    270
]

# Open the positions_camera_frame.npy file
for angle in angles:
    p = np.load(f'{scan_name}/positions_camera_frame_{angle}.npy')
    np.savetxt(
        f'{scan_name}/positions_camera_frame_{angle}.csv',
        p,
        delimiter=','
    )
