#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
#import epd4in26g
import dummyepd
import time, datetime
from PIL import Image,ImageDraw,ImageFont
from roster import Roster

logging.basicConfig(level=logging.INFO)

def font_type(size):
    return ImageFont.truetype('./Font.ttc', size)

def draw_text_centre(draws, x, y, message, fonts, colour):
    # x: centre line of text to draw
    # y: top of text to draw
    draws.text((x - draw.textlength(message, fonts) / 2, y), message, font=fonts, fill=colour)

def draw_text_right(draws, x, y, message, fonts, colour):
    # x: right most pixel of text to draw
    # y: top of text to draw
    draws.text((x-draw.textlength(message, fonts), y), message, font = fonts, fill = colour)

try:
    logging.info("ShiftPaper Demo")

    callsign = 'NN'

    #epd = epd4in26g.EPD()
    epd = dummyepd.EPD()
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

    roster = Roster(callsign)

    #120*6+16*5=800 #480-120-16=
    # Drawing on the image
    logging.info("Drawing on the image...")
    #epd.init()
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

    logging.info("Drawing today")
    day = datetime.date.today()
    draw_text_centre(draw, 172, 20, day.strftime('%b'), font_type(60), epd.RED)
    draw_text_centre(draw, 172, 80, day.strftime('%d'), font_type(120), epd.RED)
    draw_text_centre(draw, 172, 200, day.strftime('%a'), font_type(50), epd.RED)
    daily_roster = roster.get_shift(day.strftime('%B'), day.day)
    draw_text_centre(draw, 172, 255, daily_roster[0] + ' ' + daily_roster[1], font_type(55), epd.RED)

    logging.info("Drawing extra dates")
    for i in range(0,6):
        day = day + datetime.timedelta(days=1)
        daily_roster = roster.get_shift(day.strftime('%B'), day.day)
        draw_text_centre(draw, 60 + 136 * i, 375, day.strftime('%d'), font_type(40), epd.BLACK)
        draw_text_centre(draw, 60 + 136 * i, 425, daily_roster[0] + ' ' + daily_roster[1], font_type(30), epd.BLACK)

    logging.info("Drawing extra info")
    lu_str = "Last update: "+datetime.datetime.now().strftime('%H:%M')
    draw_text_right(draw, 800, 330, lu_str, font_type(25), epd.BLACK)

    cu_str = roster.callsign + ' ' + roster.name
    draw_text_right(draw, 800, 0, cu_str, font_type(35), epd.BLACK)
    
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
    
    
    """
    logging.info("Clear...")
    epd.Clear()
    """
    
    logging.info("Goto Sleep...")
    #epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in26g.epdconfig.module_exit(cleanup=True)
    exit()
