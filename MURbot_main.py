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
import MURbot_Functions as MF

title_font = ('Piboto Light', 18, 'normal')
button_font = ('Piboto Light', 10, 'normal')
button_config = {'fg' : 'grey',
                 'bg' : 'white',
                 'font' : button_font,
                 'height' : 2,
                 'width' : 12,
                 'relief' : 'flat',
                 'activebackground' : 'white',
                 'activeforeground' : 'green',
                 'bd' : 0}


root = TK.Tk()
root.geometry('280x160')
root.resizable(width=False, height=False)

main_wnd = TK.Frame(root)
main_wnd.pack(expand=1, fill='both')

TK.Label(main_wnd,
         text='MURbot',
         bg='white',
         fg='grey',
         font=title_font).pack(expand=1, fill='both', side='left')

TK.Button(main_wnd,
          text='Setup',
          **button_config,
          command=MF.setup).pack(expand=1, fill='both', side='top', anchor='e')

TK.Button(main_wnd,
          text='Start',
          **button_config,
          command=MF.run).pack(expand=1, fill='both', side='top', anchor='e')

TK.Button(main_wnd,
          text='Stop',
          **button_config,
          command=MF.reset_all).pack(expand=1, fill='both', side='top', anchor='e')

root.title('MURbot')
root.mainloop()
