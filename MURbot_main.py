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
root.resizable(width=False, height=False)

main_wnd = TK.Frame(root)
main_wnd.config(bg='white')
main_wnd.pack(expand=1, fill='both')

TK.Label(main_wnd,
         text='MURbot',
         bg='white',
         fg='grey',
         font=('Piboto Light', 18, 'normal')).pack(side='left', padx=20)

MainWndButtons(main_wnd, text='Setup', command=MainWndButtons.Setup)
MainWndButtons(main_wnd, text='Start', command=MainWndButtons.Start)
MainWndButtons(main_wnd, text='Stop', command=MainWndButtons.Stop)

root.title('MURbot v0.2')
root.mainloop()
