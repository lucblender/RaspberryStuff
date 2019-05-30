#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd5in83b
import epd2in7b
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
       
        print("Drawing")
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

        
def musicDisplaySmall(artist = "Ghost", title = "Rats", album = "Prequelle", timeAudio = "4:22", albumBlack = 'albumOutBlack.bmp', albumRed = 'albumOutRed.bmp', spotifyConnect = True):

    if len(artist) > 8:
        artist = artist[:8]+"..."    
    if len(title) > 9:
        title = title[:9]+"..."    
    if len(album) > 9:
        album = album[:9]+"..."

    originAlbumX = 30
    originAlbumy = 7
    albumLineOffset = 3
    albumSize = 130

    try:
        epd = epd2in7b.EPD()
        epd.init()          
        # Horizontal
        print("Drawing")
        albumOutBlack = Image.open(albumBlack).resize((albumSize,albumSize))  
        albumOutRed = Image.open(albumRed).resize((albumSize,albumSize))
        blackimage1 = Image.new('1', (epd2in7b.EPD_HEIGHT,epd2in7b.EPD_WIDTH), 255)# 264*176
        redimage1 = Image.new('1', (epd2in7b.EPD_HEIGHT,epd2in7b.EPD_WIDTH), 255)# 264*176
        blackimage1.paste(albumOutBlack, (originAlbumX,originAlbumy))    
        redimage1.paste(albumOutRed, (originAlbumX,originAlbumy))  
        if(spotifyConnect == True):
            spotifyImage = Image.open("spotify.bmp").resize((30,30))
            redimage1.paste(spotifyImage,(225,142))
            
        drawblack = ImageDraw.Draw(blackimage1)
        drawred = ImageDraw.Draw(redimage1)
        
        font25Medium = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Medium.ttf', 19)
        font25Regular = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Regular.ttf', 16)
        
        font15Medium = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Medium.ttf', 15)
        font15Regular = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Regular.ttf', 15)
        textX = 170
        drawblack.text((textX, 35), artist, font = font25Medium, fill = 0)
        drawred.text((textX, 60), "Title", font = font15Medium, fill = 0)
        drawblack.text((textX, 75), title, font = font25Regular, fill = 0)
        drawred.text((textX, 96), "Album", font = font15Medium, fill = 0)
        drawblack.text((textX, 110), album, font = font25Regular, fill = 0)
        drawred.text((textX, 125), timeAudio, font = font15Medium, fill = 0) 
        
        if(spotifyConnect == True):
            drawblack.text((225-40, 142+20), "Connect", font = font15Medium, fill = 0)
            drawred.text((225-40, 142+20), "Connect", font = font15Medium, fill = 1)

        drawred.line((originAlbumX-albumLineOffset, originAlbumy-albumLineOffset,
            originAlbumX-albumLineOffset, originAlbumy+albumLineOffset+albumSize), fill = 0, width=2)
            
        drawred.line((originAlbumX-albumLineOffset, originAlbumy-albumLineOffset,
            originAlbumX+albumLineOffset+albumSize, originAlbumy-albumLineOffset), fill = 0, width=2)
            
        drawblack.line((originAlbumX+albumLineOffset+albumSize, originAlbumy+albumLineOffset+albumSize,
            originAlbumX-albumLineOffset, originAlbumy+albumLineOffset+albumSize), fill = 0, width=2)
            
        drawblack.line((originAlbumX+albumLineOffset+albumSize, originAlbumy+albumLineOffset+albumSize,
            originAlbumX+albumLineOffset+albumSize, originAlbumy-albumLineOffset), fill = 0, width=2)
            
        button = 20
        buttonX = 2
        buttonY = 0
        
        drawred.polygon([(buttonX,buttonY), (buttonX, buttonY+button), (buttonX+button,buttonY+button/2)], fill = 0)
        
        if(spotifyConnect == False):
            buttonY = 50
            
            drawred.rectangle([(buttonX,buttonY), (buttonX+7, buttonY+button)], fill = 0)        
            drawred.rectangle([(buttonX+13,buttonY), (buttonX+button, buttonY+button)], fill = 0)
            
            buttonY = 100
            
            drawred.polygon([(buttonX,buttonY), (buttonX, buttonY+button), (buttonX+button/2,buttonY+button/2)], fill = 0)
            drawred.polygon([(buttonX+button/2,buttonY), (buttonX+button/2, buttonY+button), (buttonX+button,buttonY+button/2)], fill = 0)        
            
            buttonY = 150
            
            drawred.polygon([(buttonX+button/2,buttonY), (buttonX+button/2, buttonY+button), (buttonX,buttonY+button/2)], fill = 0)
            drawred.polygon([(buttonX+button,buttonY), (buttonX+button, buttonY+button), (buttonX+button/2,buttonY+button/2)], fill = 0)
        else:
            font = ImageFont.load_default()

            fontRotate = ImageFont.truetype('/root/mopidyapi/Noir/NoirStd-Regular.ttf', 16)
            # Text to be rotated...
            rotate_text = u'back in Mopidy'

            # Image for text to be rotated
            img_txt = Image.new('1', fontRotate.getsize(rotate_text),255)
            draw_txt = ImageDraw.Draw(img_txt)
            draw_txt.text((0,0), rotate_text, font=fontRotate, fill=0)
            t = img_txt.rotate(270, expand=1)
            redimage1.paste(t,(3,28))
            
        ellipseRadius = 15
        ellipseX = 225
        ellipseY = 2
        drawblack.ellipse((ellipseX,ellipseY,ellipseX+2*ellipseRadius,ellipseY+2*ellipseRadius),fill = 0)
            
        offsetLine = 5
        line0 = 5
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
        
        lineX = 225
        lineY = 25
        
        logoLines[0].line((line0+lineX,lineY-10,
            line0+lineX,lineY), fill = logoLinesFill[0], width=3)
            
        logoLines[1].line((line1+lineX,lineY-15,
            line1+lineX,lineY), fill = logoLinesFill[1], width=3)
            
        logoLines[2].line((line2+lineX,lineY-7,
            line2+lineX,lineY), fill = logoLinesFill[2], width=3)
            
        logoLines[3].line((line3+lineX,lineY-13,
            line3+lineX,lineY), fill = logoLinesFill[3], width=3)
            
        logoLines[4].line((line4+lineX,lineY-10,
            line4+lineX,lineY), fill = logoLinesFill[4], width=3)
            
        startLineX = 27
        startLineY = 148
        lenght = 264-27-5
        offset = 6
        
        if(spotifyConnect == True):
            lenght = lenght - 40
            
        drawblack.line((startLineX,startLineY,startLineX+lenght,startLineY), fill = 0, width=2)   
            
        drawred.line((startLineX,startLineY+offset*1,startLineX+lenght,startLineY+offset*1),fill = 0, width=2)   
            
        drawblack.line((startLineX,startLineY+offset*2,startLineX+lenght,startLineY+offset*2),fill = 0, width=2)  
        if(spotifyConnect == True):
            lenght = lenght - 40
        drawblack.line((startLineX,startLineY+offset*3,startLineX+lenght,startLineY+offset*3), fill = 0, width=2)     
            
            
        epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))
        time.sleep(2)
       
    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
