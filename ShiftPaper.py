#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import paper, roster

logging.basicConfig(level=logging.INFO)

### Config ###
callsign = 'NN'


logging.info("ShiftPaper Demo")
eroster = roster.Roster(callsign)
epaper = paper.Paper(eroster)

while True:
    epaper.draw_paper()
    break