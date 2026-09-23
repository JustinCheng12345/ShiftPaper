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
epaper = paper.Paper(eroster, eatis, eweather)

while True:
    eatis.get_runway()
    eweather.get_weather()
    epaper.update_paper()
    break
