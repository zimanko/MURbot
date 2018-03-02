import tkinter as TK
import MURbot_Functions as MF

class MainWndButtons(TK.Button):
    def __init__(self, parent, **configs):
        TK.Button.__init__(self, parent, **configs)
        self.config(fg = 'grey',
                    bg = 'white',
                    font = ('Helvetic', 10, 'normal'),
                    height = 1,
                    width = 8,
                    padx = 3,
                    pady = 5,
                    relief = 'flat',
                    overrelief = 'raised',
                    activebackground = 'white',
                    activeforeground = 'grey',
                    bd = 1)
        self.pack(side='top', anchor='e', padx=10, pady=5)

    def Setup():
        MF.setup()

    def Start():
        MF.run()

    def Stop():
        MF.reset_all()
