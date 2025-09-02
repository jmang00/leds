from PIL import Image, ImageChops
import yaml

# Load settings
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


NO_LEDS = config['NO_LEDS']
cams = config['CAMS'].keys()
angles = config['SCAN']['ANGLES']

# # Base
for cam in cams:
    for angle in angles:
        # Base
        img = Image.open(f'scan/images/{cam}_{angle}_base.jpg')
        img = img.rotate(270, expand=True)
        img.save(f'scan/images/{cam}_{angle}_base.jpg')

        # All
        for i in range(NO_LEDS):
            img = Image.open(f'scan/images/{cam}_{angle}_{i}.jpg')
            img = img.rotate(270, expand=True)
            img.save(f'scan/images/{cam}_{angle}_{i}.jpg')