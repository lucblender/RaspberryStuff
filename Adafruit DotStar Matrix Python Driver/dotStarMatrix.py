import board
import adafruit_dotstar as dotstar
from PIL import Image,ImageDraw,ImageFont
import cv2

from time import sleep, time


width = 32
height = 8 
fps = 24

def writeFrame(dots, image):
    for x in range(0,width):
        for y in range(0,height):
            if(x%2==1):  
                dots[x*height+(7-y)] = image[y][x]    
            else:
                dots[x*height+y] = image[y][x] 
    dots.show()       

dots = dotstar.DotStar(board.SCK, board.MOSI, width*height, brightness=0.7, auto_write=False)

    

class DotStarMatrix:

    def __init__(self, width, height, syncPin, dataPin, brightness):
        self.width = width
        self.height = height
        self.dots = dotstar.DotStar(syncPin, dataPin, width*height, brightness=brightness, auto_write=False)
    
    def writePilImage(self, image):
        pix = image.load()
        for x in range(0,self.width):
            for y in range(0,self.height):
                if(x%2==1):  
                    self.dots[x*self.height+((self.height-1)-y)] = pix[x,y]    
                else:
                    self.dots[x*self.height+y] = pix[x,y]
        self.dots.show()    
        
    def writeOpenCVFrame(self, frame):
        for x in range(0,self.width):
            for y in range(0,self.height):
                if(x%2==1):  
                    self.dots[x*self.height+((self.height-1)-y)]  = frame[y][x]    
                else:
                    self.dots[x*self.height+y] = frame[y][x] 
        self.dots.show()   
        
    def writeMovie(self, path):
        vidcap = cv2.VideoCapture(path)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        success,frame = vidcap.read()
        lastTime = 0

        while success:   
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            while(time()-lastTime<1/fps):
                time()
            self.writeOpenCVFrame(frame)
            lastTime = time()
            success,frame = vidcap.read()            
    
    def writeImageFromPath(self, path):
        im = Image.open(path) # Can be many different formats.
        self.writePilImage(im)   
        
    def scrollText(self, text, font, color, scrollDelay):
        sizeTxt = font.getsize(text)
        mask = font.getmask(text, "1")
        mask.save_ppm("temp.ppm")
        mask = Image.open("temp.ppm")

        for i in range(self.width, sizeTxt[0]*-1-2, -1):
            picture = Image.new("RGB", (self.width, self.height))
            pictureMask = Image.new("L", (self.width, self.height))
            picture1 = Image.new("RGB", (self.width, self.height),color)
            pictureMask.paste(mask,(i,0))
            picture.paste(picture1,(0,0),pictureMask)

            self.writePilImage(picture)
            

            sleep(scrollDelay)
    
    


