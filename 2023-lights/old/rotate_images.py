from PIL import Image, ImageChops


NO_LEDS = 300
cams = [0]
angles = [
    0,
    90,
    180,
    270
]
scan_name = 'scan2'

# Rotate every image by 270 degrees

# # Base
for cam in cams:
    for angle in angles:
        img = Image.open(f'{scan_name}/{cam}_{angle}_base.jpg')
        img = img.rotate(270, expand=True)
        img.save(f'{scan_name}/0_{cam}_base.jpg')

# # Bright
# for cam in cams:
#     img = Image.open(f'{scan_name}/{cam}_bright.jpg')
#     img = img.rotate(270, expand=True)
#     img.save(f'{scan_name}/{cam}_bright.jpg')

# # # Main
# for i in range(NO_LEDS):
#     for cam in cams:
#         img = Image.open(f'{scan_name}/{cam}_{i}.jpg')
#         img = img.rotate(270, expand=True)
#         img.save(f'{scan_name}/{cam}_{i}.jpg')