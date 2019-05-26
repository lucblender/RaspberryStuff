#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd5in83b
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from random import randrange

#******************************************************************************
#
# @brief 
# @param[in] artist : String, artist name to display
# @param[in] titre : String, titre name to display
# @param[in] album : String, album name to display
# @param[in] timeAudio : String, track length to display
# @param[in] albumBlack :  String, path of black/with picture black channel 
# @param[in] albumRed :  String, path of black/with picture red channel 
# @return void
# 
#******************************************************************************
def musicDisplay(artist = "Ghost", title = "Rats", album = "Prequelle", timeAudio = "4:22", albumBlack = 'albumOutBlack.bmp', albumRed = 'albumOutRed.bmp', spotifyConnect = True):

    if len(artist) > 15:
        artist = artist[:15]+"..."    
    if len(title) > 15:
        title = title[:15]+"..."    
    if len(album) > 15:
        album = album[:15]+"..."

    originAlbumX = 15
    originAlbumy = 15
    albumLineOffset = 5
    albumSize = 350

    try:
        epd = epd5in83b.EPD()
        epd.init()
        #print("Clear...")
        #epd.Clear(0xFF)
        
        # Drawing on the Horizontal image
        HBlackimage = Image.new('1', (epd5in83b.EPD_WIDTH, epd5in83b.EPD_HEIGHT), 255)  # 600*448
        HRedimage = Image.new('1', (epd5in83b.EPD_WIDTH, epd5in83b.EPD_HEIGHT), 255)  # 600*448 
        
        # Horizontal
        print("Drawing")
        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRedimage)
        albumOutBlack = Image.open(albumBlack)      
        albumOutRed = Image.open(albumRed)      
        blackimage1 = Image.new('1', (epd5in83b.EPD_WIDTH, epd5in83b.EPD_HEIGHT), 255)
        redimage1 = Image.new('1', (epd5in83b.EPD_WIDTH, epd5in83b.EPD_HEIGHT), 255)
        blackimage1.paste(albumOutBlack, (originAlbumX,originAlbumy))    
        redimage1.paste(albumOutRed, (originAlbumX,originAlbumy))  
        if(spotifyConnect == True):
            spotifyImage = Image.open("spotify.bmp")
            redimage1.paste(spotifyImage,(500,10))
            
        drawblack = ImageDraw.Draw(blackimage1)
        drawred = ImageDraw.Draw(redimage1)
        
        font25Medium = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Medium.ttf', 25)
        font25Regular = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Regular.ttf', 25)
        
        font15Medium = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Medium.ttf', 19)
        font15Regular = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Regular.ttf', 19)
        drawblack.text((375, 50), artist, font = font25Medium, fill = 0)
        drawred.text((375, 85), "Title", font = font15Regular, fill = 0)
        drawblack.text((375, 110), title, font = font25Regular, fill = 0)
        drawred.text((375+27, 150), "Album", font = font15Regular, fill = 0)
        drawblack.text((375, 175), album, font = font25Regular, fill = 0)
        drawred.text((375, 215), timeAudio, font = font15Regular, fill = 0) 
        
        if(spotifyConnect == True):
            drawblack.text((530, 27), "Connect", font = font15Regular, fill = 0)
            drawred.text((530, 27), "Connect", font = font15Regular, fill = 1)
        
        heightVinyl = 143
        drawblack.ellipse((375,heightVinyl,375+25,heightVinyl+25),fill = 0)
        drawred.ellipse((375+8,heightVinyl+8,375+9+8,heightVinyl+9+8),fill = 0)
        drawblack.ellipse((375+11,heightVinyl+11,375+3+11,heightVinyl+3+11),fill = 1)    
        drawred.ellipse((375+11,heightVinyl+11,375+3+11,heightVinyl+3+11),fill = 1)
        
        
        drawred.line((originAlbumX-albumLineOffset, originAlbumy-albumLineOffset,
            originAlbumX-albumLineOffset, originAlbumy+albumLineOffset+albumSize), fill = 0, width=4)
            
        drawred.line((originAlbumX-albumLineOffset, originAlbumy-albumLineOffset,
            originAlbumX+albumLineOffset+albumSize, originAlbumy-albumLineOffset), fill = 0, width=4)
            
        drawblack.line((originAlbumX+albumLineOffset+albumSize, originAlbumy+albumLineOffset+albumSize,
            originAlbumX-albumLineOffset, originAlbumy+albumLineOffset+albumSize), fill = 0, width=4)
            
        drawblack.line((originAlbumX+albumLineOffset+albumSize, originAlbumy+albumLineOffset+albumSize,
            originAlbumX+albumLineOffset+albumSize, originAlbumy-albumLineOffset), fill = 0, width=4)
            
        ellipseRadius = 30
        drawblack.ellipse((epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-ellipseRadius-10-ellipseRadius,
            epd5in83b.EPD_WIDTH/2+ellipseRadius,epd5in83b.EPD_HEIGHT-10),fill = 0)
            
        offsetLine = 4+6
        line0 = 7+3
        line1 = line0 + offsetLine
        line2 = line1 + offsetLine
        line3 = line2 + offsetLine
        line4 = line3 + offsetLine
        line5 = line4 + offsetLine
        
        randIndex = randrange(0,5)
        
        logoLines = [drawblack]*5
        logoLinesFill = [1]*5
        logoLines[randIndex] = drawred
        logoLinesFill[randIndex] = 0
        
        logoLines[0].line((line0+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20-20,
            line0+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20), fill = logoLinesFill[0], width=6)
            
        logoLines[1].line((line1+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20-30,
            line1+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20), fill = logoLinesFill[1], width=6)
            
        logoLines[2].line((line2+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20-15,
            line2+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20), fill = logoLinesFill[2], width=6)
            
        logoLines[3].line((line3+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20-25,
            line3+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20), fill = logoLinesFill[3], width=6)
            
        logoLines[4].line((line4+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20-20,
            line4+epd5in83b.EPD_WIDTH/2-ellipseRadius,epd5in83b.EPD_HEIGHT-10-20), fill = logoLinesFill[4], width=6)
            
            
        drawred.line((15,epd5in83b.EPD_HEIGHT-20,
            epd5in83b.EPD_WIDTH/2-35,epd5in83b.EPD_HEIGHT-20), fill = 0, width=4)        
        drawblack.line((epd5in83b.EPD_WIDTH-15,epd5in83b.EPD_HEIGHT-20,
            epd5in83b.EPD_WIDTH/2+35,epd5in83b.EPD_HEIGHT-20), fill = 0, width=4)
            
        drawblack.line((15,epd5in83b.EPD_HEIGHT-33,
            epd5in83b.EPD_WIDTH/2-35,epd5in83b.EPD_HEIGHT-33), fill = 0, width=4)        
        drawblack.line((epd5in83b.EPD_WIDTH-15,epd5in83b.EPD_HEIGHT-33,
            epd5in83b.EPD_WIDTH/2+35,epd5in83b.EPD_HEIGHT-33), fill = 0, width=4)
            
        drawblack.line((15,epd5in83b.EPD_HEIGHT-46,
            epd5in83b.EPD_WIDTH/2-35,epd5in83b.EPD_HEIGHT-46), fill = 0, width=4)        
        drawred.line((epd5in83b.EPD_WIDTH-15,epd5in83b.EPD_HEIGHT-46,
            epd5in83b.EPD_WIDTH/2+35,epd5in83b.EPD_HEIGHT-46), fill = 0, width=4)
        
        drawblack.line((15,epd5in83b.EPD_HEIGHT-60,
            epd5in83b.EPD_WIDTH/2-35,epd5in83b.EPD_HEIGHT-60), fill = 0, width=4)        
        drawblack.line((epd5in83b.EPD_WIDTH-15,epd5in83b.EPD_HEIGHT-60,
            epd5in83b.EPD_WIDTH/2+35,epd5in83b.EPD_HEIGHT-60), fill = 0, width=4)
            
            
        epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))
        time.sleep(2)
       
    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
