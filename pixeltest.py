import neopixel
from machine import Pin
import random
import time

#this incredibly simple example just blinks some random colors on the neopixel before shutting it off.

ledPin = Pin(21)
strip = neopixel.NeoPixel(ledPin, 1, bpp=3)


for i in range(10):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    strip.fill((r,g,b))
    strip.write()
    time.sleep(0.4)
    
strip.fill((0,0,0))
strip.write()