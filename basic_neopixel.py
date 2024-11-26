# A basic example using the neopixel library

import board
import neopixel
from time import sleep

leds = neopixel.NeoPixel(board.D18, 50, brightness=0.4, auto_write=False, pixel_order=neopixel.GRB)

while True:
    leds.fill((255,255,255))
    sleep(5)
    leds.show()
    sleep(5)