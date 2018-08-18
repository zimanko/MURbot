import tkinter as TK
import MURbot_Functions as MF
import random
import math

'''Global variables'''
PREV_X_MODIFIER = 0
PREV_Y_MODIFIER = 0
X_MODIFIER = 0
Y_MODIFIER = 0
X_ZERO = 0
Y_ZERO = 0
OBS_WIN_W = 0
OBS_WIN_H = 0
CANVAS_W = 0
SCALE_W = 0
SCALE = 1

'''GUI Classes and Functions'''
class MainWndButtons(TK.Button):
    def __init__(canvas, parent, **configs):
        TK.Button.__init__(canvas, parent, **configs)
        canvas.config(fg = 'grey',
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
        canvas.pack(side='top', anchor='n', padx=10, pady=5)

    def Setup():
        MF.setup()

    def Start():
        MF.run()

    def Freeride():
        MF.freeride()

    def Stop():
        MF.reset_all()


class NavCanvas(TK.Canvas):
    def __init__(self, canvas, scale):

        test_radardata = []
        a = 1
        while a < 181:
            n = (a, random.randrange(200, 255))
            test_radardata.append(n)
            del n
            a += 1

        def forward(event):
            global X_MODIFIER, Y_MODIFIER
            X_MODIFIER += 2 * math.cos(MF.HEADING)
            Y_MODIFIER += 2 * math.sin(MF.HEADING)
            redraw(event)
            canvas.update()

        def backward(event):
            global X_MODIFIER, Y_MODIFIER
            X_MODIFIER -= 2 * math.cos(MF.HEADING)
            Y_MODIFIER -= 2 * math.sin(MF.HEADING)
            redraw(event)
            canvas.update()

        def left(event):
            global HEADING
            MF.HEADING -= math.pi * 0.01
            redraw(event)
            canvas.update()

        def right(event):
            global HEADING
            MF.HEADING += math.pi * 0.01
            redraw(event)
            canvas.update()

        def redraw(event):
            global PREV_X_MODIFIER, PREV_Y_MODIFIER, X_MODIFIER, Y_MODIFIER, X_ZERO, Y_ZERO, OBS_WIN_W, OBS_WIN_H
            win_w = canvas.winfo_width()
            win_h = canvas.winfo_height()
            if win_w != OBS_WIN_W or win_h != OBS_WIN_H:
                try:
                    canvas.move('Env_dots', (win_w - OBS_WIN_W) / 2, (win_h - OBS_WIN_H) / 2)
                except:
                    None
                OBS_WIN_W = win_w
                OBS_WIN_H = win_h
                canvas.update()
            #if X_MODIFIER < -100 or Y_MODIFIER < -100 or X_MODIFIER > 100 or Y_MODIFIER > 100:
                #canvas.move('Env_dots', PREV_X_MODIFIER - X_MODIFIER, PREV_Y_MODIFIER - Y_MODIFIER)
                #canvas.update()
                #X_MODIFIER = PREV_X_MODIFIER
                #Y_MODIFIER = PREV_Y_MODIFIER
            else:
                X_ZERO = win_w / 2 + X_MODIFIER
                Y_ZERO = win_h / 2 + Y_MODIFIER
                PREV_X_MODIFIER = X_MODIFIER
                PREV_Y_MODIFIER = Y_MODIFIER
                canvas.delete('MURbot')
                murbot_pos(X_ZERO, Y_ZERO)

        def murbot_pos(X_ZERO, Y_ZERO):
            angle = [0, 4.8, 7.2]
            murbot_pos_coords = [0, 0, 0, 0, 0, 0]
            radius = SCALE * 15
            for i in range(len(angle)):
                murbot_pos_coords[2 * i] = int(radius * math.cos((angle[i] * math.pi / 6) + MF.HEADING))
                murbot_pos_coords[2 * i + 1] = int(radius * math.sin((angle[i] * math.pi / 6) + MF.HEADING))
            canvas.create_polygon(X_ZERO + murbot_pos_coords[0], Y_ZERO + murbot_pos_coords[1],
                                  X_ZERO + murbot_pos_coords[2], Y_ZERO + murbot_pos_coords[3],
                                  X_ZERO + murbot_pos_coords[4], Y_ZERO + murbot_pos_coords[5],
                                  X_ZERO + murbot_pos_coords[0], Y_ZERO + murbot_pos_coords[1],
                                  fill='light green',
                                  outline='green',
                                  tags='MURbot')
            MURbot = canvas.coords('MURbot')
            print(MURbot)

        def env_dots(event):
            global OBS_WIN_W, OBS_WIN_H
            OBS_WIN_W = canvas.winfo_width()
            OBS_WIN_H = canvas.winfo_height()
            i = 0
            while i < len(test_radardata):
                tup = test_radardata[i]
                alpha = tup[0] * math.pi / 180
                x = math.sin(alpha) * tup[1] * SCALE
                y = math.cos(alpha) * tup[1] * SCALE
                canvas.create_oval(X_ZERO + x + 2 * SCALE, Y_ZERO + y + 2 * SCALE,
                                   X_ZERO + x - 2 * SCALE, Y_ZERO + y - 2 * SCALE,
                                   fill='red',
                                   tag='Env_dots')
                i += 5

        def scroll_right(event):
            canvas.xview_scroll(1, TK.UNITS)

        def scroll_left(event):
            canvas.xview_scroll(-1, TK.UNITS)

        def scroll_up(event):
            canvas.yview_scroll(-1, TK.UNITS)

        def scroll_down(event):
            canvas.yview_scroll(1, TK.UNITS)


        canvas.bind('<Configure>', redraw)
        canvas.bind('<FocusIn>', redraw)
        canvas.bind('<Up>', forward)
        canvas.bind('<Down>', backward)
        canvas.bind('<Left>', left)
        canvas.bind('<Right>', right)
        canvas.bind('<Control_L>', env_dots)
        canvas.bind('<KeyPress-d>', scroll_right)
        canvas.bind('<KeyPress-a>', scroll_left)
        canvas.bind('<KeyPress-w>', scroll_up)
        canvas.bind('<KeyPress-s>', scroll_down)
        canvas.focus_force()

        scale.bind('<Motion>', redraw)
        scale.pack(pady=20, side='top')


def CreateCanvasAndScale(parent_for_canvas, parent_for_scale):
    global CANVAS_W
    CANVAS_W = TK.Canvas(parent_for_canvas,
                         bg='white',
                         highlightthickness=0.5,
                         highlightcolor='#f6f6f6',
                         height=350,
                         xscrollincrement=2,
                         yscrollincrement=2)

    CANVAS_W.pack(expand=1, fill='both')

    global SCALE_W
    SCALE_W = TK.Scale(parent_for_scale,
                       bg='white',
                       from_=0.5,
                       to=1.5,
                       resolution=-1,
                       showvalue=0,
                       orient='horizontal',
                       sliderrelief='ridge',
                       highlightthickness=0,
                       troughcolor='#f6f6f6',
                       command=SetScaleValue)
    SCALE_W.set(1)


def SetScaleValue(scalevalue):
    global SCALE
    SCALE = float(scalevalue)


