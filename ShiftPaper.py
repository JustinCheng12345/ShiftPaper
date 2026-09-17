#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import paper, roster, info

logging.basicConfig(level=logging.INFO)

### Config ###
callsign = 'NN'


logging.info("ShiftPaper Demo")
eroster = roster.Roster(callsign)
epaper = paper.Paper(eroster)
eatis = info.AtisReader()

while True:
    #epaper.draw_paper()
    eatis.get_runway()
    break