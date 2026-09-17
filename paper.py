#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
#import epd4in26g
import dummyepd
import time, datetime, holidays
from PIL import Image,ImageDraw,ImageFont

class Paper:
    def __init__(self, roster):
        self.roster = roster
        self.draw = None

    def draw_paper(self):
        try:
            #epd = epd4in26g.EPD()
            epd = dummyepd.EPD()
            logging.info("init and Clear")
            epd.init()
            #epd.Clear()

            def font_type(size):
                return ImageFont.truetype('./Font.ttc', size)

            def draw_text_left(draws, x, y, message, fonts, colour=epd.BLACK):
                draws.text((x - draw.textlength(message, fonts) / 2, y), message, font=fonts, fill=colour)

            def draw_text_centre(draws, x, y, message, fonts, colour=epd.BLACK):
                # x: centre line of text to draw
                # y: top of text to draw
                draws.text((x - draw.textlength(message, fonts) / 2, y), message, font=fonts, fill=colour)

            def draw_text_right(draws, x, y, message, fonts, colour=epd.BLACK):
                # x: right most pixel of text to draw
                draws.text((x - draw.textlength(message, fonts), y), message, font=fonts, fill=colour)

            def cal_col(day):
                if day in holidays.HK() or day.weekday() >4:
                    return epd.RED
                else:
                    return epd.BLACK

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
            Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
            draw = ImageDraw.Draw(Himage)
            
            # Main Date
            logging.info("Drawing today")
            day = datetime.date.today()
            draw.rectangle([(0,0),(345,345)],outline = cal_col(day), width = 5)
            
            draw.text((172, 25), day.strftime('%b'), font=font_type(60), fill=cal_col(day), anchor='mt')
            draw.text((172, 110), day.strftime('%d'), font=font_type(120), fill=cal_col(day), anchor='mt')
            draw.text((172, 210), day.strftime('%a'), font=font_type(50), fill=cal_col(day), anchor='mt')
            daily_roster = self.roster.get_shift(day.strftime('%B'), day.day)
            draw.text((172, 275), daily_roster[0] + ' ' + daily_roster[1], font=font_type(55), fill=cal_col(day), anchor='mt')
            
            # 6 Following Dates
            logging.info("Drawing extra dates")
            for i in range(0,6):
                day = day + datetime.timedelta(days=1)
                daily_roster = self.roster.get_shift(day.strftime('%B'), day.day)
                draw.rectangle([(0+135*i,355),(125+135*i,480)],outline = epd.BLACK, width = 5)
                draw.text((62 + 136 * i, 380), day.strftime('%d'), font=font_type(40), fill=cal_col(day), anchor='mt')
                draw.text((62 + 136 * i, 430), daily_roster[0] + ' ' + daily_roster[1], font=font_type(30), fill=cal_col(day), anchor='mt')
                
            logging.info("Drawing art")
            Image.Image.paste(Himage, Image.open('./art3.bmp'), (350, 5))

            logging.info("Drawing extra info")
            lu_str = "Last update: "+datetime.datetime.now().strftime('%H:%M')
            draw.text((800,345), lu_str, font=font_type(25), fill=epd.BLACK, anchor='rb')

            cu_str = self.roster.callsign + ' ' + self.roster.name
            draw.text((800,0), cu_str, font=font_type(35), fill=epd.BLACK, anchor='rt')
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
            epd.display(epd.getbuffer(Himage))
            time.sleep(3)


            """
            logging.info("Clear...")
            epd.Clear()
            """

            logging.info("Goto Sleep...")
            epd.sleep()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd4in26g.epdconfig.module_exit(cleanup=True)
            exit()

    def clear_paper(self):
        try:
            #epd = epd4in26g.EPD()
            epd = dummyepd.EPD()
            logging.info("Clear and sleep")
            epd.init()
            epd.Clear()
            time.sleep(2)
            epd.sleep()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd4in26g.epdconfig.module_exit(cleanup=True)
            exit()
