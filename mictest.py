from machine import I2S
from machine import Pin
import time
import math
import neopixel

#led is used in this basic example to show that mic data is being picked up
ledPin = Pin(21)
led = neopixel.NeoPixel(ledPin, 1, bpp=3)



#init the PDM microphone.
#I struggled to find real documentation on how this mic should be used, but it seems very picky about its sample rate. 22050 seems to work. 

SCK_PIN = 43
WS_PIN = 41
SD_PIN = 46
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 8192
SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO
SAMPLE_RATE_IN_HZ = 22050

audio_in = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.RX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
    )



num_samples = 100
buf = bytearray(2)
for i in range(0,1000):
    
    #take samples and average them
    value_sum = 0
    for j in range (num_samples):
        audio_in.readinto(buf)
        value_sum += (int(buf[0]) + int(buf[1])) // 2
    
    val = value_sum // num_samples
    
    amplitude = abs(val - 130)
    
    led.fill((amplitude,(amplitude ** 2) // 257,(amplitude ** 2) // 257))
    led.write()
    
    #time.sleep(0.05)

led.fill((0,0,0))
led.write()
audio_in.deinit()
