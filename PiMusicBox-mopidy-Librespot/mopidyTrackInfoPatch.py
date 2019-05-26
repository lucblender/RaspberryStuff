from time import sleep
from mopidyapi import MopidyAPI
from imageDivider import divideFromSource
from musicDisplay import musicDisplay
from track import Track
import sys
from threading import Lock, Semaphore
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
    image = m.library.get_images([resultTrack['uri']])
    localTrack.imageURI= image['result'][resultTrack['uri']][0]['uri']
    return localTrack

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
 #artist, title, album, timeAudio, imageURI

resultTrack = m.playback.get_current_track()['result']

print(resultTrack)
if resultTrack != None:
    currentTrack = trackFromResult(resultTrack)
    divideFromSource(inputFile=currentTrack.imageURI)
    print(currentTrack)                            
    if displaySemaphore.acquire(False):
        displayMutex.acquire()
        musicDisplay(artist = currentTrack.artist,title = currentTrack.title,album = currentTrack.album,timeAudio = currentTrack.timeAudio, albumBlack = 'albumOutBlack.bmp',albumRed = 'albumOutRed.bmp', spotifyConnect = False)               
        displayMutex.release()
        displaySemaphore.release()
                                
path = trackingPath
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=False)
observer.start()

while(1):
    sleep(0.5)
