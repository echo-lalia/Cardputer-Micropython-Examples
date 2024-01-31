from machine import Pin
import time

ir = Pin(44, Pin.OUT)


#this is a very basic example, showing that the led can be blinked. Real IR-blasitng use is gonna need a real driver. 
for i in range(0,10):
    ir.value(1)
    time.sleep(0.2)
    ir.value(0)
    time.sleep(0.2)
    
    