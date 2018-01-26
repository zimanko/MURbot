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

import brickpi3
import time
import turtle
import math

BP = brickpi3.BrickPi3()

def move(power):
    BP.set_motor_power(BP.PORT_B, power)
    BP.set_motor_power(BP.PORT_C, -power)
    space = (4 - len(str(power))) * ' '
    print ('Motor power set to:' + space + str(power) + '  |  Voltage: ' + str(BP.get_voltage_battery()))

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
BP.set_motor_position_kp(BP.PORT_A, 120)
BP.set_motor_position_kd(BP.PORT_A, 100)
BP.set_motor_position(BP.PORT_A, 0)

scr = turtle.Screen()
TR = turtle.Turtle()
TR.hideturtle()
TR.penup()
TR.setpos(0, 0)
TR.dot(20, 'red')

r = 50
while r < 251:
    TR.setpos(0, -r)
    TR.pendown()
    TR.color('grey')
    TR.circle(r)
    TR.penup()
    r += 50

ch = math.pi / 530

time.sleep(4)       # to ensure the sensors is activated


t = 0
while t < 1:
    BP.set_motor_dps(BP.PORT_A, 80)
    while BP.get_motor_encoder(BP.PORT_A) < 530:
        alpha = BP.get_motor_encoder(BP.PORT_A) * ch
        try:
            c1 = BP.get_sensor(BP.PORT_1)
            c2 = BP.get_sensor(BP.PORT_4)
            # print ('OK at ' + str(alpha))
        except:
            c1 = c2 = 0
            # print('Sensor Error at ' + str(alpha))
        a1 = math.sin(alpha) * c1
        b1 = math.cos(alpha) * c1
        a2 = math.sin(alpha) * c2
        b2 = math.cos(alpha) * c2
        TR.setpos(-a1, b1)
        if c1 > 250:
            TR.dot(1, 'grey')
        else:
            TR.dot(10, 'blue')
        TR.setpos(a2, -b2)
        if c2 > 250:
            TR.dot(1, 'grey')
        else:
            TR.dot(10, 'blue')
        # time.sleep(0.2)
    BP.set_motor_dps(BP.PORT_A, -80)
    while BP.get_motor_encoder(BP.PORT_A) > 0:
        alpha = BP.get_motor_encoder(BP.PORT_A) * ch
        try:
            c1 = BP.get_sensor(BP.PORT_1)
            c2 = BP.get_sensor(BP.PORT_4)
            # print ('OK at ' + str(alpha))
        except:
            c1 = c2 = 0
            # print('Sensor Error at ' + str(alpha))
        a1 = math.sin(alpha) * c1
        b1 = math.cos(alpha) * c1
        a2 = math.sin(alpha) * c2
        b2 = math.cos(alpha) * c2
        if c1 > 250:
            TR.dot(1, 'grey')
        else:
            TR.dot(10, 'blue')
        TR.setpos(a2, -b2)
        if c2 > 250:
            TR.dot(1, 'grey')
        else:
            TR.dot(10, 'blue')
        # time.sleep(0.2)
    BP.set_motor_dps(BP.PORT_A, 0)
    t += 1

BP.set_motor_position(BP.PORT_A, 0)
BP.reset_all()
turtle.done()
