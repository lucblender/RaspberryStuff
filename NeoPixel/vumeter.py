import alsaaudio as alsa
import time
import audioop
import math
import time
import board
import neopixel


# GPIO10, GPIO12, GPIO18 or GPIO21 
pixels = neopixel.NeoPixel(board.D18, 30)


def POWERGPIO(p7,p11,p13,p15,p12,p16,p18,p22):
	if(p7):
		pixels[0] = (255, 0, 0)
	else:
		pixels[0] = (0, 0, 0)
	if(p11):
		pixels[1] = (255, 0, 0)
	else:
		pixels[1] = (0, 0, 0)
	if(p13):
		pixels[2] = (255, 0, 0)
	else:
		pixels[2] = (0, 0, 0)
	if(p15):
		pixels[3] = (255, 0, 0)
	else:
		pixels[3] = (0, 0, 0)
	if(p12):
		pixels[4] = (255, 0, 0)
	else:
		pixels[4] = (0, 0, 0)
	if(p16):
		pixels[5] = (255, 0, 0)
	else:
		pixels[5] = (0, 0, 0)
	if(p18):
		pixels[6] = (255, 0, 0)
	else:
		pixels[6] = (0, 0, 0)
	if(p22):
		pixels[7] = (255, 0, 0)
	else:
		pixels[7] = (0, 0, 0)
	return

def SETGPIO(d):
	if(d == 'a'):
		POWERGPIO(0,0,0,0,0,0,0,0)
	elif(d == 'b'):
		POWERGPIO(1,0,0,0,0,0,0,0)
	elif(d == 'c'):
		POWERGPIO(1,1,0,0,0,0,0,0)
	elif(d == 'd'):
		POWERGPIO(1,1,1,0,0,0,0,0)
	elif(d == 'e'):
		POWERGPIO(1,1,1,1,0,0,0,0)
	elif(d == 'f'):
		POWERGPIO(1,1,1,1,1,0,0,0)
	elif(d == 'g'):
		POWERGPIO(1,1,1,1,1,1,0,0)
	elif(d == 'h'):
		POWERGPIO(1,1,1,1,1,1,1,0)
	elif(d == 'i'):
		POWERGPIO(1,1,1,1,1,1,1,1)
	return
    
def SETGPIOTest(charD):
    d = ord(charD)-97
    pixels[0:d] = [(255,255,0)]*d
    pixels[d:len(pixels)] = [(0,0,0)]*(len(pixels)-d)
    
print "##############################"
print "# Waiting for a song to play #"
print "##############################"

inp = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, 'hw:Loopback,1,0')
out = alsa.PCM(alsa.PCM_PLAYBACK, alsa.PCM_NORMAL, 'plughw:0,0')

rate = 44100
period = 320

inp.setchannels(2)
inp.setrate(rate)
inp.setformat(alsa.PCM_FORMAT_S16_LE)
inp.setperiodsize(320)


lo = 10000
hi = 32000

log_lo = math.log(lo)
log_hi = math.log(hi)

while True:
	l,data = inp.read()
	if l:
		try:
            if len(data)%2 != 0: #add padding
                data+= b'\0'
			d = audioop.max(data, 2)
			vu = (math.log(float(max(audioop.max(data, 2),1)))-log_lo)/(log_hi-log_lo)
			teste = chr(ord('a')+min(max(int(vu*20),0),19))
			if teste != 'a':
				print teste
			if d>0:
				SETGPIO(teste)
		except():
			break


