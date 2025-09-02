# Analyse the images to find the position of each LED

# Input: a folder of images
# Output: a positions.csv file

from PIL import Image, ImageChops
import numpy as np
import cv2

NO_LEDS = 250
cams = ['A', 'B', 'C']
scan_name = 'scan1'


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
    brightest_pixel = (0, 0)
    max_brightness = 0

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            # Calculate the brightness of the pixel (you can use different formulas)
            brightness = sum(pixel)  # Sum of R, G, and B values

            if brightness > max_brightness:
                max_brightness = brightness
                brightest_pixel = (x, y)

    return brightest_pixel


# Load the base images
base_img = {}
for cam in cams:
    base_img[cam] = Image.open(f'{scan_name}/{cam}_base.jpg')

# # Find a pixel-to-mm scale for each camera
# pixels_per_mm = {}
# for cam in cams:
#     pixels_per_mm[cam] = find_pixel_to_mm_scale(f'{scan_name}/{cam}_bright.jpg')

# print(pixels_per_mm)

# positions = np.zeros((NO_LEDS, 3))

positions = np.zeros((NO_LEDS, 3))

for i in range(NO_LEDS):
    for cam in cams:
        img = Image.open(f'{scan_name}/{cam}_{i}.jpg')
        diff_img = ImageChops.difference(img, base_img[cam])

        x, y = find_brightest_pixel(diff_img)
        # print(f'Brightest in image {cam}: ({x}, {y})')


        # Save position
        positions[i] = [x, y, 0]
    
    np.savetxt('positions.csv', positions, delimiter=",", fmt="%d")



