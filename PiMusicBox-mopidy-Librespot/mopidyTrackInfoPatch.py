from time import sleep
from mopidyapi import MopidyAPI
from imageDivider import divideFromSource
#from musicDisplay import musicDisplaySmall as musicDisplay #for 2.7 inches
from musicDisplay import musicDisplay # for 5.83 inches
from track import Track
import sys
from threading import Lock, Semaphore
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import RPi.GPIO as GPIO 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PLAY_BUTTON = 5
PAUSE_BUTTON = 6
NEXT_BUTTON = 13
PREVIOUS_BUTTON = 19

trackingPath = "/root/mopidyapi/data"
trackingFile = trackingPath+"/"+"librespotOutput"
m = MopidyAPI()
currentTrack = Track("Uninitialized","Uninitialized","Uninitialized","Uninitialized","Uninitialized")

artistMutex = Lock()
displaySemaphore = Semaphore(2)
displayMutex = Lock()

def trackFromResult(resultTrack):
    localTrack = Track()
    localTrack.title= resultTrack['name']
    localTrack.artist = resultTrack['artists'][0]['name']
    localTrack.album = resultTrack['album']['name']    
    time = resultTrack['length']/1000
    localTrack.timeAudio= str(int(time/60))+":"+'%02d' % int(time%60) 
    image = m.library.get_images([resultTrack['album']['uri']])
    localTrack.imageURI= image['result'][resultTrack['album']['uri']][0]['uri']
    return localTrack
    
def button_callback(channel):
    if channel == PLAY_BUTTON:
        m.playback.play()
        print("button play pressed")
    elif channel == PAUSE_BUTTON:    
        m.playback.pause()  
        print("button pause pressed")
    elif channel == NEXT_BUTTON:
        m.playback.next()
        print("button next pressed")
    elif channel == PREVIOUS_BUTTON:  
        m.playback.previous()  
        print("button previous pressed")

@m.on_event('playback_state_changed')
def trackChanged(event):
    global currentTrack
    sleep(1)    
    resultTrack = m.playback.get_current_track()['result']                                  
    tmpTrack = trackFromResult(resultTrack)
    if tmpTrack != currentTrack:
        if tmpTrack.imageURI != currentTrack.imageURI:
            divideFromSource(inputFile=tmpTrack.imageURI)
            
        artistMutex.acquire()
        currentTrack = tmpTrack
        artistMutex.release()
        print(currentTrack)
        
        if displaySemaphore.acquire(False):
            displayMutex.acquire()
            musicDisplay(artist = currentTrack.artist,title = currentTrack.title,album = currentTrack.album,timeAudio = currentTrack.timeAudio, albumBlack = 'albumOutBlack.bmp',albumRed = 'albumOutRed.bmp', spotifyConnect = False)
            displayMutex.release()
            displaySemaphore.release()

        
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global currentTrack
        if event.src_path == trackingFile:
            fileHandle = open ( trackingFile,"r" , encoding='utf-8') 
            lineList = fileHandle.readlines()
            fileHandle.close()
                            
            if lineList[-1].find("requesting chunk")==-1 and lineList[-1].find("DEBUG:librespot_core::session:")==-1 and lineList[-1].find("DEBUG:librespot_playback::player: command=Pause") == -1:
                foundTrack = False
                i = -1
                while(foundTrack == False and i > (-len(lineList)-1)):
                    if lineList[i].find("INFO:librespot_playback::player: Loading track ")!=-1:
                        trackURI = lineList[i].split("with Spotify URI ")[-1]\
                                    .replace('"','')\
                                    .replace('\n','')    
                        resultTrack = m.library.lookup(trackURI)['result'][0]
                            
                        tmpTrack = trackFromResult(resultTrack)
                        
                        if tmpTrack != currentTrack:
                            if tmpTrack.imageURI != currentTrack.imageURI:
                                divideFromSource(inputFile=tmpTrack.imageURI)
                            artistMutex.acquire()
                            currentTrack = tmpTrack
                            artistMutex.release()
                            print(currentTrack)
                            if displaySemaphore.acquire(False):
                                displayMutex.acquire()
                                musicDisplay(artist = currentTrack.artist,title = currentTrack.title,album = currentTrack.album,timeAudio = currentTrack.timeAudio, albumBlack = 'albumOutBlack.bmp',albumRed = 'albumOutRed.bmp', spotifyConnect = True)
                                displayMutex.release()
                                displaySemaphore.release()
                                
                        foundTrack = True
                    i-=1
 
GPIO.setup(PLAY_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(PAUSE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(NEXT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(PREVIOUS_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    
GPIO.add_event_detect(PLAY_BUTTON,GPIO.FALLING,callback=button_callback,bouncetime=500) 
GPIO.add_event_detect(PAUSE_BUTTON,GPIO.FALLING,callback=button_callback,bouncetime=500) 
GPIO.add_event_detect(NEXT_BUTTON,GPIO.FALLING,callback=button_callback,bouncetime=500) 
GPIO.add_event_detect(PREVIOUS_BUTTON,GPIO.FALLING,callback=button_callback,bouncetime=500) 

resultTrack = m.playback.get_current_track()['result']

if resultTrack != None:
    currentTrack = trackFromResult(resultTrack)
    divideFromSource(inputFile=currentTrack.imageURI)
    print(currentTrack)                            
    if displaySemaphore.acquire(False):
        displayMutex.acquire()
        musicDisplay(artist = currentTrack.artist,title = currentTrack.title,album = currentTrack.album,timeAudio = currentTrack.timeAudio, albumBlack = 'albumOutBlack.bmp',albumRed = 'albumOutRed.bmp', spotifyConnect = False)               
        displayMutex.release()
        displaySemaphore.release()
else:
    musicDisplay(artist = "Welcome!",title = "",album = "",timeAudio = "", albumBlack = 'lbBlack.bmp',albumRed = 'lbRed.bmp', spotifyConnect = False)   
                                
path = trackingPath
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=False)
observer.start()

while(1):
    sleep(0.5)
