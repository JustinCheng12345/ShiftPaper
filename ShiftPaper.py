#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
#if os.path.exists(libdir):
#    sys.path.append(libdir)

import logging
import epd4in26g
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.INFO)

def fontType(size):
    return ImageFont.truetype('./Font.ttc', size)
    
def drawText(draw, message, fonts, x, y, colour):
    # x: centre line of text to draw
    # y: top of text to draw
    draw.text((x-draw.textlength(message, fonts)/2, y), message, font = fonts, fill = colour)

try:
    logging.info("ShiftPaper Demo")

    epd = epd4in26g.EPD()   
    logging.info("init and Clear")
    #epd.init()
    #epd.Clear()
    
    """
    # read bmp file 
    logging.info("read bmp file")
    epd.init_fast()
    #Himage = Image.open(os.path.join(picdir, '06.bmp'))
    Himage = Image.open('./06.bmp')
    epd.display(epd.getbuffer(Himage))
    time.sleep(5)
    """
    
    #120*6+16*5=800 #480-120-16=
    # Drawing on the image
    logging.info("Drawing on the image...")
    epd.init()
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  
    draw = ImageDraw.Draw(Himage)
    # Main Date
    draw.rectangle([(0,0),(344,344)],outline = epd.BLACK, width = 5)
    # 6 Following Dates
    draw.rectangle([(0,360),(120,480)],outline = epd.BLACK, width = 5)
    draw.rectangle([(136,360),(256,480)],outline = epd.BLACK, width = 5)
    draw.rectangle([(272,360),(392,480)],outline = epd.BLACK, width = 5)
    draw.rectangle([(408,360),(528,480)],outline = epd.BLACK, width = 5)
    draw.rectangle([(544,360),(664,480)],outline = epd.BLACK, width = 5)
    draw.rectangle([(680,360),(800,480)],outline = epd.BLACK, width = 5)

    day = datetime.datetime.now()
    drawText(draw, day.strftime("%b"), fontType(60), 172, 20, epd.RED)
    drawText(draw, day.strftime("%d"), fontType(120), 172, 80, epd.RED)
    drawText(draw, day.strftime("%a"), fontType(50), 172, 200, epd.RED)
    
    for i in range(0,6):
        day = day + datetime.timedelta(days=1)
        logging.info(day.strftime("%d"))
        drawText(draw, day.strftime("%d"), fontType(40), 60+136*i, 375, epd.BLACK)
    
    
    """
    draw.rectangle([(0,0),(50,50)],outline = epd.BLACK)
    draw.rectangle([(55,0),(100,50)],fill = epd.RED)
    draw.line([(0,0),(50,50)], fill = epd.YELLOW,width = 1)
    draw.line([(0,50),(50,0)], fill = epd.YELLOW,width = 1)
    draw.pieslice((55, 60, 95, 100), 90, 180, outline = epd.RED)
    draw.pieslice((55, 60, 95, 100), 270, 360, fill = epd.BLACK)
    draw.chord((10, 60, 50, 100), 0, 360, fill = epd.YELLOW)
    draw.ellipse((55, 60, 95, 100), outline = epd.RED)
    draw.polygon([(110,0),(110,50),(150,25)],outline = epd.BLACK)
    draw.polygon([(190,0),(190,50),(150,25)],fill = epd.BLACK)
    draw.text((120, 60), 'e-Paper demo', font = font15, fill = epd.YELLOW)
    draw.text((110, 90), u'微雪电子', font = font24, fill = epd.RED)
    """
    #epd.display(epd.getbuffer(Himage))
    time.sleep(3)
    
    logging.info("Clear...")
    epd.Clear()
    
    logging.info("Goto Sleep...")
    #epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in26g.epdconfig.module_exit(cleanup=True)
    exit()
