#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
#import epd4in26g
import dummyepd
import time, datetime, holidays
from PIL import Image,ImageDraw,ImageFont

class Paper:
    def __init__(self, roster, atis, weather):
        self.roster = roster
        self.atis = atis
        self.weather = weather
        self.draw = None
        # self.epd = epd4in26g.EPD()
        self.epd = dummyepd.EPD()
        
        # Dummy item allowing splitting drawing image from epd updating
        self.height = self.epd.height
        self.width = self.epd.width
        self.BLACK  = 0x000000   #   00  BGR
        self.WHITE  = 0xffffff   #   01
        self.YELLOW = 0x00ffff   #   10
        self.RED    = 0x0000ff   #   11

    def draw_paper(self):
        def font_type(size):
            return ImageFont.truetype('./Font.ttc', size)

        def draw_text(x, y, message, font_size, colour=self.BLACK, anchor='lt', bg=False):
            if bg:
                tl = self.draw.textlength(message, font_type(font_size))
                if anchor == 'lt':
                    self.draw.rectangle([(x, y), (x+tl, y+font_size)], fill=self.WHITE)
                if anchor == 'lb':
                    self.draw.rectangle([(x, y-font_size), (x+tl, y)], fill=self.WHITE)
                elif anchor == 'rt':
                    self.draw.rectangle([(x-tl, y), (x, y+font_size)], fill=self.WHITE)
                elif anchor == 'rb':
                    self.draw.rectangle([(x-tl, y-font_size), (x, y)], fill=self.WHITE)
                elif anchor == 'mt':
                    self.draw.rectangle([(x-tl/2, y), (x+tl/2, y+font_size)], fill=self.WHITE)
                elif anchor == 'mb':
                    self.draw.rectangle([(x-tl/2, y-font_size), (x+tl/2, y)], fill=self.WHITE)
            self.draw.text((x, y), message, font=font_type(font_size), fill=colour, anchor=anchor)

        def cal_col(day):
            if day in holidays.HK() or day.weekday() > 4:
                return self.RED
            else:
                return self.BLACK

        # 120*6+16*5=800 #480-120-16=
        # Drawing on the image
        Himage = Image.new('RGB', (self.width, self.height), self.WHITE)
        self.draw = ImageDraw.Draw(Himage)

        # Main Date
        day = datetime.date.today()
        self.draw.rectangle([(0, 0), (345, 345)], outline=cal_col(day), width=5)

        draw_text(172, 25, day.strftime('%b'), 60, colour=cal_col(day), anchor='mt')
        draw_text(172, 110, day.strftime('%d'), 120, colour=cal_col(day), anchor='mt')
        draw_text(172, 210, day.strftime('%a'), 50, colour=cal_col(day), anchor='mt')
        daily_roster = self.roster.get_shift(day.strftime('%B'), day.day)
        working_day = daily_roster[0] != ''
        draw_text(172, 275, daily_roster[0] + ' ' + daily_roster[1], 55, colour=cal_col(day), anchor='mt')

        # 6 Following Dates
        for i in range(0, 6):
            day = day + datetime.timedelta(days=1)
            daily_roster = self.roster.get_shift(day.strftime('%B'), day.day)
            self.draw.rectangle([(0 + 135 * i, 355), (125 + 135 * i, 480)], outline=self.BLACK, width=5)
            draw_text(62 + 136 * i, 380, day.strftime('%d'), 40, colour=cal_col(day), anchor='mt')
            draw_text(62 + 136 * i, 430, daily_roster[0] + ' ' + daily_roster[1], 30, colour=cal_col(day), anchor='mt')

        # Art or Info
        if self.weather.typhoon or self.weather.rainstorm:
            if self.weather.typhoon:
                Image.Image.paste(Himage, Image.open('./art/'+self.weather.typhoon+'.bmp'), (350, 0))
            if self.weather.rainstorm:
                Image.Image.paste(Himage, Image.open('./art/'+self.weather.rainstorm+'.bmp'), (350, 175))
            draw_text(530, 40, self.atis.runway_config, 40)
        else:
            # No weather warning, display art background
            Image.Image.paste(Himage, Image.open('./art/art3.bmp'), (350, 5))
            draw_text(800, 40, self.atis.runway_config, 40, anchor='rt', bg=True)

        # Extra info
        logging.info("Drawing extra info")
        lu_str = "Last update: " + datetime.datetime.now().strftime('%H:%M')
        draw_text(800, 345, lu_str, 25, anchor='rb', bg=True)

        cu_str = self.roster.callsign + ' ' + self.roster.name
        draw_text(800, 0, cu_str, 35, anchor='rt', bg=True)

        return Himage

    def update_paper(self):
        try:
            logging.info("init and Clear")
            self.epd.init()
            Himage = self.draw_paper()
            self.epd.display(self.epd.getbuffer(Himage))
            time.sleep(3)

            """
            logging.info("Clear...")
            epd.Clear()
            """

            logging.info("Goto Sleep...")
            self.epd.sleep()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd4in26g.epdconfig.module_exit(cleanup=True)
            exit()

    def clear_paper(self):
        try:
            logging.info("Clear and sleep")
            self.epd.init()
            self.epd.Clear()
            time.sleep(2)
            self.epd.sleep()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd4in26g.epdconfig.module_exit(cleanup=True)
            exit()
