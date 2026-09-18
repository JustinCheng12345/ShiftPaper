#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import paper, roster, info

logging.basicConfig(level=logging.INFO)

### Config ###
callsign = 'NN'

logging.info("ShiftPaper Demo")
eroster = roster.Roster(callsign)
eatis = info.AtisReader()
eweather = info.WeatherReader()
epaper = paper.Paper(eroster)

while True:
    #epaper.update_paper()
    #eatis.get_runway()
    eweather.get_weather()
    break
