from machine import I2S
from machine import Pin
import time
import math
import neopixel

#led is used in this basic example to show that mic data is being picked up
ledPin = Pin(21)
led = neopixel.NeoPixel(ledPin, 1, bpp=3)

@micropython.viper
def get_bits(byte:int):
    return (
        (byte >> 7) & 1,
        (byte >> 6) & 1,
        (byte >> 5) & 1,
        (byte >> 4) & 1,
        (byte >> 3) & 1,
        (byte >> 2) & 1,
        (byte >> 1) & 1,
        byte & 1
        )

def avg_amplitude(buf, samples):
    reading = 0
    
    for i in range(0,samples - 1):
        bits = get_bits(buf[i])
        for bit in bits:
            reading += bit
    
    reading /= samples * 8
    #print(f'{reading},')
    #time.sleep(1)

    return abs(reading - 0.5)
    

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

num_multi_samples = 30

num_samples = 16
buf = bytearray(num_samples)
counter = 0
start_time = time.ticks_ms()
while True:
    
    # get amplitude several times, for accuracy
    multi_sample = []
    for i in range(0,num_multi_samples):
        #take samples and average them
        samples_read = audio_in.readinto(buf)
        multi_sample.append(avg_amplitude(buf, samples_read))
    
    amplitude = max(multi_sample)
    
    #g=math.floor(min(max(amplitude - 0.04, 0) * 1000, 255))
    #b=math.floor(min((max(amplitude - 0.04, 0) ** 2) * 100000, 255))
    
    led.fill((
        math.floor(min((max(amplitude - 0.05, 0) ** 3) * 100000, 255)),
        math.floor(min(max(amplitude - 0.04, 0) * 1000, 255)),
        math.floor(min((max(amplitude - 0.04, 0) ** 2) * 100000, 255))))
    
    led.write()
    #time.sleep(0.05)

led.fill((0,0,0))
led.write()
audio_in.deinit()

