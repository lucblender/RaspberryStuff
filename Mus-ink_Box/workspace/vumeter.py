import pyaudio 
import numpy  
import audioop
import sys
import math
import struct
import board
import neopixel
from time import sleep

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser

enable = True
turningColor = True 
allLedSame = False
doFFT = True
onlyRed = True
ledsNumber = 16

trackingConfigPath = "/home/pi/workspace/conf"
trackingConfigFile = trackingConfigPath+"/"+"musinkConfig.conf"

# GPIO10, GPIO12, GPIO18 or GPIO21 
pixels = neopixel.NeoPixel(board.D21, ledsNumber*2)

def recoverConfig():
    global enable
    global turningColor
    global allLedSame
    global doFFT
    global onlyRed
    global ledsNumber
    config = configparser.ConfigParser()
    config.read(trackingConfigFile)
    if config.has_option("vumeter","enable"):
        enable = config["vumeter"].getboolean("enable")
    if config.has_option("vumeter","turningColor"):
        turningColor = config["vumeter"].getboolean("turningColor")
    if config.has_option("vumeter","allLedSame"):
        allLedSame = config["vumeter"].getboolean("allLedSame")
    if config.has_option("vumeter","turningColor"):
        doFFT = config["vumeter"].getboolean("doFFT")
    if config.has_option("vumeter","doFFT"):
        onlyRed = config["vumeter"].getboolean("onlyRed")
    if config.has_option("vumeter","ledsNumber"):
        ledsNumber = int(config["vumeter"]["ledsNumber"])

        
        

class configChanges(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == trackingConfigFile:
            recoverConfig()


def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print(str(i)+'. '+dev['name'])
        i += 1
        
def sinwheel(pos, factor):
    pos = pos % 360
    r = (math.sin(math.radians(pos))+1)/2*255
    g = (math.sin(math.radians(pos+120))+1)/2*255
    b = (math.sin(math.radians(pos+240))+1)/2*255
    return (int(r*(factor/255)), int(g*(factor/255)), int(b*(factor/255)))

def sinRedwheel(pos, factor):
    pos = pos % 360
    r = 255
    g = (math.sin(math.radians(pos+120))+1)/2*60
    b = 0
    return (int(r*(factor/255)), int(g*(factor/255)), int(b*(factor/255)))

def soundlight(): 
    chunk      = 2**11 # Change if too fast/slow, never less than 2**11
    scale      = 75    # Change if too dim/bright
    exponent   = 5     # Change if too little/too much difference between loud and quiet sounds
    samplerate = 44100 
    lo = 10000
    hi = 32000

    log_lo = math.log(lo)
    log_hi = math.log(hi)
    
    device = 4
    
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
        channels = 1,
        rate = 44100,
        input = True,
        frames_per_buffer = chunk,
        input_device_index = device)
    
    print("Starting, use Ctrl+C to stop")
    try:
        index = 0
        while True:
            if enable:
                data  = stream.read(chunk, exception_on_overflow = False)
                levels = [0]*ledsNumber   
                
                if doFFT == False:
                    rms   = audioop.rms(data, 2)
                    level = min(rms / (2.0 ** 16) * scale, 1.0) 
                    level = level**exponent 
                    level = int(level * 255)
                    
                    d = audioop.max(data, 2)
                    vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
     
                    teste = min(max(int(vu*ledsNumber),0),ledsNumber-1)
                    levels[0:teste] = [255]*teste
                else:
                    # Do FFT
                    levels = calculate_levels(data, chunk, samplerate)

                if turningColor == True:
                    rotate = 360 / ledsNumber
                else:
                    rotate = 0
                
                # Make it look better
                i = 0
                for level in levels:
                    level = max(min(level / scale, 1.0), 0.0)
                    level = level**exponent 
                    level = int(level * 255)
                    if onlyRed == True:
                        pixels[i] = sinRedwheel(index+rotate*i,level)
                        pixels[ledsNumber*2-1-i] = sinRedwheel(index+rotate*i,level)
                    else:
                        pixels[i] = sinwheel(index+rotate*i,level)
                        pixels[ledsNumber*2-1-i] = sinwheel(index+rotate*i,level)
                    i = i+1
                    
                if allLedSame == False:
                    index = (index + 5 )% 360
            else:
                decrease = False
                for pixel in pixels:
                    if pixel != (0,0,0):
                        decrease = True

                if decrease:
                    for i in range(0,len(pixels)):
                        pixels[i] = tuple([int(c / 1.5) for c in pixels[i]])
                else:
                    sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        print("\nStopping")
        stream.close()
        p.terminate()

def calculate_levels(data, chunk, samplerate):
    # Use FFT to calculate volume for each frequency

    # Convert raw sound data to Numpy array
    fmt = "%dH"%(len(data)/2)
    data2 = struct.unpack(fmt, data)
    data2 = numpy.array(data2, dtype='h')

    # Apply FFT
    fourier = numpy.fft.fft(data2)
    ffty = numpy.abs(fourier[0:int(len(fourier)/2)])/1000
    ffty1=ffty[:int(len(ffty)/2)]
    ffty2=ffty[int(len(ffty)/2)::]+2
    ffty2=ffty2[::-1]
    ffty=ffty1+ffty2
    ffty=numpy.log(ffty)-2
    
    fourier = list(ffty)[4:-4]
    fourier = fourier[:int(len(fourier)/2)]
    
    size = len(fourier)

    # Add up for x lights
    levels = [sum(fourier[i:int(i+size/ledsNumber)]) for i in range(0, size, int(size/ledsNumber))][:ledsNumber]
    
    return levels

if __name__ == '__main__':
    event_handler = configChanges()
    observer = Observer()
    observer.schedule(event_handler, trackingConfigPath, recursive=False)
    observer.start()
    recoverConfig()
    soundlight()