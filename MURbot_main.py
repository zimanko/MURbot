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

import tkinter as TK
from MURbot_GUIclasses import *

root = TK.Tk()

main_wnd = TK.Frame(root)
main_wnd.config(bg='white', width=10)
main_wnd.pack(fill='both', side='left')

TK.Label(main_wnd,
         height = 4,
         width = 9,
         text='MURbot',
         bg='white',
         fg='grey',
         font=('Piboto Light', 18, 'normal')).pack(side='top')

MainWndButtons(main_wnd, text='Setup', command=MainWndButtons.Setup)
MainWndButtons(main_wnd, text='Start', command=MainWndButtons.Start)
MainWndButtons(main_wnd, text='Freeride', command=MainWndButtons.Freeride)
MainWndButtons(main_wnd, text='Stop', command=MainWndButtons.Stop)

NavCanvas(root)

root.title('MURbot v0.2')
root.mainloop()

