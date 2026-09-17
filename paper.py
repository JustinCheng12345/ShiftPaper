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

    def draw_paper(self, epd):
        def font_type(size):
            return ImageFont.truetype('./Font.ttc', size)

        def draw_text(x, y, message, font_size, colour=epd.BLACK, anchor='lt', bg=False):
            if bg:
                tl = self.draw.textlength(message, font_type(font_size))
                if anchor == 'lt':
                    self.draw.rectangle([(x, y), (x+tl, y+font_size)], fill=epd.WHITE)
                elif anchor == 'rt':
                    self.draw.rectangle([(x-tl, y), (x, y+font_size)], fill=epd.WHITE)
                elif anchor == 'mt':
                    self.draw.rectangle([(x-tl/2, y), (x+tl/2, y+font_size)], fill=epd.WHITE)
            self.draw.text((x, y), message, font=font_type(font_size), fill=colour, anchor=anchor)

        def cal_col(day):
            if day in holidays.HK() or day.weekday() > 4:
                return epd.RED
            else:
                return epd.BLACK

        # 120*6+16*5=800 #480-120-16=
        # Drawing on the image
        Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
        self.draw = ImageDraw.Draw(Himage)

        # Main Date
        day = datetime.date.today()
        self.draw.rectangle([(0, 0), (345, 345)], outline=cal_col(day), width=5)

        draw_text(172, 25, day.strftime('%b'), 60, colour=cal_col(day), anchor='mt')
        draw_text(172, 110, day.strftime('%d'), 120, colour=cal_col(day), anchor='mt')
        draw_text(172, 210, day.strftime('%a'), 510, colour=cal_col(day), anchor='mt')
        daily_roster = self.roster.get_shift(day.strftime('%B'), day.day)
        draw_text(172, 275, daily_roster[0] + ' ' + daily_roster[1], 55, colour=cal_col(day), anchor='mt')

        # 6 Following Dates
        for i in range(0, 6):
            day = day + datetime.timedelta(days=1)
            daily_roster = self.roster.get_shift(day.strftime('%B'), day.day)
            self.draw.rectangle([(0 + 135 * i, 355), (125 + 135 * i, 480)], outline=epd.BLACK, width=5)
            draw_text(62 + 136 * i, 380, day.strftime('%d'), 40, colour=cal_col(day), anchor='mt')
            draw_text(62 + 136 * i, 430, daily_roster[0] + ' ' + daily_roster[1], 30, colour=cal_col(day), anchor='mt')

        # Art
        Image.Image.paste(Himage, Image.open('./art3.bmp'), (350, 5))

        # Extra info
        logging.info("Drawing extra info")
        lu_str = "Last update: " + datetime.datetime.now().strftime('%H:%M')
        draw_text(800, 345, lu_str, 25, anchor='rb', bg=True)

        cu_str = self.roster.callsign + ' ' + self.roster.name
        draw_text(800, 0, cu_str, 35, anchor='rt', bg=True)

        return Himage

    def update_paper(self):
        try:
            # epd = epd4in26g.EPD()
            epd = dummyepd.EPD()
            logging.info("init and Clear")
            epd.init()
            Himage = self.draw_paper(epd)
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
