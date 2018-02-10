#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Project: MURbot - Ultrasonic mapping robot
#
#  MURbot.py
#  
#  Copyright 2018 Viktor KASZA <pi@dex>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  

import MURbot_Functions as MF
import brickpi3
import time

BP = brickpi3.BrickPi3()

MF.setup()
power = 30

try:
    while True:
        MF.move(power)
        MF.tilt(40, power, -1)
        MF.move(0)
        time.sleep(0.5)
        MF.move(-power)
        MF.turn('Left')
        MF.tilt(40, power, 3)
        MF.turn('Straight')
        MF.move(0)
        time.sleep(0.5)
except KeyboardInterrupt:
    MF.move(0)
    BP.reset_all()

