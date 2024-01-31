from machine import I2S
from machine import Pin
import time
import math



#This example generates a sine wave, and plays Greensleeves.

#It took me a while to get any sound at all out of the I2S speaker. Seems like it prefers to be in stereo mode. 

SCK_PIN = 41
WS_PIN = 43
SD_PIN = 42
I2S_ID = 1
BUFFER_LENGTH_IN_BYTES = 8192
SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.STEREO
SAMPLE_RATE_IN_HZ = 64000


audio_out = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.TX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
    )

song = const(('A4','A4','C5','C5','C5','C5','D5','D5','E5','E5','E5','E5','F5','E5','D5','D5','D5','D5','B4','B4','G4','G4','G4','G4','A4','B4','C5','C5','C5','C5','A4','A4','A4','A4','GS4','GS4','A4','A4','B4','B4','B4','B4','-','GS4','GS4','E4','E4','E4','E4','A4','A4','C5','C5','C5','C5','D5','D5','E5','E5','E5','E5','F5','E5','D5','D5','D5','D5','B4','B4','G4','G4','G4','G4','A4','B4','C5','C5','B4','B4','A4','A4','GS4','GS4','-','FS4','FS4','-','GS4','GS4','-','A4','A4','A4','A4','A4','A4','-','A4','A4','A4','A4','A4','A4','','','G5','G5','G5','G5','','','G5','G5','G5','G5','-','FS5','E5','D5','D5','D5','D5','-','B4','B4','G4','G4','G4','G4','A4','B4','C5','C5','C5','C5','-','A4','A4','-','A4','A4','GS4','GS4','A4','A4','B4','B4','B4','B4','GS4','GS4','E4','E4','E4','E4','','','G5','G5','G5','G5','','','G5','G5','G5','G5','-','FS5','E5','D5','D5','D5','D5','-','B4','B4','G4','G4','G4','G4','A4','B4','C5','C5','-','B4','B4','-','A4','A4','-','GS4','GS4','-','FS4','FS4','-','-','GS4','GS4','-','-','-','A4','A4','A4','A4','A4','A4','-','-','A4','A4','A4','A4','A4','A4'))
tones = {
"LOW": 50,
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978,
"HIGH": 8000
}



def gen_sin_wave(freq, volume):
    #8 bits per sample (times 2 for 16 in stereo), 8000 samples per second
    radians_increment = (math.pi / SAMPLE_RATE_IN_HZ) * freq / 2
    
    samples = bytearray()
    rads_current = 0
    while rads_current < math.pi:
        sample = math.floor(((math.sin(rads_current)) * 127.5 * volume))
        samples += bytearray((sample, sample))
        rads_current += radians_increment
    return samples


        
def play_tone(freq, vol, length):
    samples = gen_sin_wave(freq, vol)
    num_sample_loops = int(length * freq)
    for i in range(num_sample_loops):
        audio_out.write(samples)
        
def play_note(note, vol, length):
    freq = tones[note]
    play_tone(freq, vol, length)

def jingle(mysong,speed=1, vol=0.1):
    for i in range(len(mysong)):
        if (mysong[i] == ""):
            play_tone(400, 0, 0.15 / speed)
            #play_nothing(0.15 / speed)
        elif (mysong[i] == "-"):
            play_tone(400, 0, 0.02 / speed)
            #play_nothing(0.02 / speed)
        else:
            play_note(mysong[i], vol, 0.15 / speed)




if __name__ == "__main__":

    
    #play_tone(440, 0.05, 1)
    jingle(song, speed=0.8)

    time.sleep(0.5)



audio_out.deinit()