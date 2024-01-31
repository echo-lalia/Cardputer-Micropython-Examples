import os
import machine
import time
from machine import SDCard, Pin


#this example simply mounts the SD card and prints its contents before unmounting it. 


sd = SDCard(slot=2, sck=Pin(40), miso=Pin(39), mosi=Pin(14), cs=Pin(12))



os.mount(sd, '/sd')

os.chdir('sd')
print(os.listdir())

time.sleep(1)

os.chdir('/')
print(os.listdir())



os.umount('/sd')