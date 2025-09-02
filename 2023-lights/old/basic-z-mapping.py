# Analyse the images to find the position of each LED

# Input: a folder of images
# Output: a positions.csv file

from PIL import Image, ImageChops, ImageDraw
import numpy as np
import cv2


debug = False

NO_LEDS = 250
NO_CAMS = 3
cams = ['A', 'B', 'C']


def find_pixel_to_mm_scale(image_path, reference_length_mm=75):
    # Load the image
    image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Use a color threshold to detect the pink strip (you may need to adjust the threshold values)
    lower_pink = np.array([245, 153, 187])
    upper_pink = np.array([255, 255, 255])

    mask = cv2.inRange(cv2.cvtColor(image, cv2.COLOR_BGR2HSV), lower_pink, upper_pink)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it corresponds to the pink strip)
    try:
        largest_contour = max(contours, key=cv2.contourArea)
    except:
        return None
    
    # Find the bounding box of the contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Display the contour
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Calculate pixels per mm
    pixels_per_mm = w / reference_length_mm

    return pixels_per_mm

def find_brightest_pixel(image):
    width, height = image.size
    brightest_pixel = None
    max_brightness = 0

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            # Calculate the brightness of the pixel (you can use different formulas)
            brightness = sum(pixel)  # Sum of R, G, and B values

            if brightness > max_brightness:
                max_brightness = brightness
                brightest_pixel = np.array((x, y))

    return brightness, brightest_pixel

def find_led_coords(image):
    # Input: an image
    # Output: the coorrdinates of the LED, or None if there isn't one visible

    # Just use a brightness threshold
    brightness, brightest_pixel = find_brightest_pixel(image)

    print(brightness)
    print(brightest_pixel)
    if brightness < 20:
        return None
    return brightest_pixel

def dist(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)



# Tree coordinates in each camera frame
tree_top = np.array([(255,53), (264, 36), (305, 18)])
tree_bottom = np.array([(264, 599), (268, 492), (266, 633)])
actual_tree_height_mm = 2130

# Calculate a mm per pixel scale for each camera
# Do I need to do more complex camera properties stuff??
mm_per_pixel = []
for c in range(len(cams)):
    height_pixels = dist(tree_top[c], tree_bottom[c])
    mm_per_pixel.append(
        actual_tree_height_mm / height_pixels
    )

print(mm_per_pixel)
scan_name = 'scan1'


# Load the base images
base_img = {}
for cam in cams:
    img = Image.open(f'{scan_name}/{cam}_base.jpg')
    base_img[cam] = img


# Look through the images for each LED
positions = np.zeros((NO_LEDS, 3))
z_pos = np.zeros((NO_LEDS, 1))

for i in range(NO_LEDS):
    print(f'\nLED {i}')
    
    # Open the images and find diffs
    imgs = [
        Image.open(f'{scan_name}/{cam}_{i}.jpg')
        for cam in cams
    ]

    diff_imgs = [
        ImageChops.difference(imgs[c], base_img[cams[c]])
        for c in range(NO_CAMS)
    ]

    # Find the brightest pixel in each image
    brightness = [0]*3
    brightest_pixel = [None]*3
    for c in range(len(cams)):
        brightness[c], brightest_pixel[c] = find_brightest_pixel(diff_imgs[c])
     
    
    # Get camera with highest brightness
    c = np.argmax(brightness)
    print(f'Using camera {cams[c]}, brightness {brightness[c]}')

    # Coordinates of the brightest pixel in camera frame
    P = brightest_pixel[c]

    # Coordinates of the tree within the camera frame
    B = tree_bottom[c]
    T = tree_top[c]
    
    if debug:
        # Draw these 3 points on the diff image and show it
        img = diff_imgs[c]
        draw = ImageDraw.Draw(img)
        point_size = 3
        # Draw P
        draw.ellipse([P[0] - point_size, P[1] - point_size,
                P[0] + point_size, P[1] + point_size],
                fill="red")
        
        # Draw B and T in green
        draw.ellipse([B[0] - point_size, B[1] - point_size,
                    B[0] + point_size, B[1] + point_size],
                    fill="green")
        draw.ellipse([T[0] - point_size, T[1] - point_size,
                    T[0] + point_size, T[1] + point_size],
                    fill="green")

        draw.line([B[0], B[1], T[0], T[1]], fill="green", width=1)
        img.show()
        

    # # Could speed this up by moving some f this outside the loop
    # # Define vectors
    # v_BP = P - B
    # v_BT = T - B

    # # Compute the transformation matrix from camera from to tree frame
    # v_BT_cross = np.cross(v_BT, [0, 0, 1])[:2]

    # # Calculate the transformation matrix
    # M_BT_inv = np.linalg.inv(np.column_stack([v_BT, v_BT_cross]))
    # v_BP_transformed = M_BT_inv @ v_BP

    # # Convert to mm
    # P_T_mm = v_BP_transformed[:2] * mm_per_pixel[c]

    # x = P_T_mm[0]
    # z = P_T_mm[1]

    z = B[1] - P[1]
    z_mm = z * mm_per_pixel[c]
    
    y = B[0] - P[0]
    y_mm = y * mm_per_pixel[c]
    
    print(f'Height: {z_mm/10} cm')
    print(f'Distance from trunk: {y_mm/10} cm')

    # Save position
    positions[i] = [0,0,z_mm]

# store positions in csv
print(positions)
np.savetxt('positions.csv', positions, delimiter=",", fmt="%d")








# old stuff


# print(P_mm)
# print(P, B, T)
# # Define the line from B to T
# r = lambda t: B + (T-B)*t
# print(r(0), r(1))
# print(r)
# print(np.dot(P-r(t),r(t)))
# tsols = np.linalg.solve(
#     np.dot(P-r(t),r(t)),
#     0
# )
# P_rel = P-r(tsols[0])

# Find the coordinates of the LED relative to the tree
# From Mathematica
# P_rel = [
#     (-B[0] + P[0] - ((-B[0] + T[0]) * (2 * B[0]**2 + 2 * B[1]**2 - B[0] * P[0] - B[1] * P[1] - 2 * B[0] * T[0] + P[0] * T[0] - 2 * B[1] * T[1] + P[1] * T[1] + np.sqrt(-4 * (B[0]**2 - B[0] * P[0] + B[1] * (B[1] - P[1])) * (B[0]**2 + B[1]**2 - 2 * B[0] * T[0] + T[0]**2 - 2 * B[1] * T[1] + T[1]**2) + (2 * B[0]**2 + 2 * B[1]**2 + P[0] * T[0] - B[0] * (P[0] + 2 * T[0]) + P[1] * T[1] - B[1] * (P[1] + 2 * T[1]))**2))) / (2 * (B[0]**2 + B[1]**2 - 2 * B[0] * T[0] + T[0]**2 - 2 * B[1] * T[1] + T[1]**2))),
#     (-B[1] + P[1] - ((-B[1] + T[1]) * (2 * B[0]**2 + 2 * B[1]**2 - B[0] * P[0] - B[1] * P[1] - 2 * B[0] * T[0] + P[0] * T[0] - 2 * B[1] * T[1] + P[1] * T[1] + np.sqrt(-4 * (B[0]**2 - B[0] * P[0] + B[1] * (B[1] - P[1])) * (B[0]**2 + B[1]**2 - 2 * B[0] * T[0] + T[0]**2 - 2 * B[1] * T[1] + T[1]**2) + (2 * B[0]**2 + 2 * B[1]**2 + P[0] * T[0] - B[0] * (P[0] + 2 * T[0]) + P[1] * T[1] - B[1] * (P[1] + 2 * T[1]))**2))) / (2 * (B[0]**2 + B[1]**2 - 2 * B[0] * T[0] + T[0]**2 - 2 * B[1] * T[1] + T[1]**2)))
# ]
