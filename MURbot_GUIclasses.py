import tkinter as TK
import MURbot_Functions as MF
import random
import math

'''Global variables'''
POS_X = 0
POS_Y = 0
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
            global POS_X, POS_Y
            POS_X += 2 * math.cos(MF.HEADING)
            POS_Y += 2 * math.sin(MF.HEADING)
            print(POS_X, POS_Y)
            redraw_canvas(event)
            canvas.update()

        def backward(event):
            global POS_X, POS_Y
            POS_X -= 2 * math.cos(MF.HEADING)
            POS_Y -= 2 * math.sin(MF.HEADING)
            print(POS_X, POS_Y)
            redraw_canvas(event)
            canvas.update()

        def left(event):
            global HEADING
            MF.HEADING -= math.pi * 0.01
            redraw_canvas(event)
            canvas.update()

        def right(event):
            global HEADING
            MF.HEADING += math.pi * 0.01
            redraw_canvas(event)
            canvas.update()

        def redraw_canvas(event):
            canvas.delete('MURbot')
            draw_murbot(POS_X, POS_Y)

        def draw_murbot(x_coord, y_coord):
            angle = [0, 0.66, 1.33]
            murbot_coords = [0, 0, 0, 0, 0, 0]
            radius = SCALE * 30
            radius2 = SCALE * 20.59
            murbot_coords[0] = int(radius * math.cos((angle[0] * math.pi) + MF.HEADING))
            murbot_coords[1] = int(radius * math.sin((angle[0] * math.pi) + MF.HEADING))
            murbot_coords[2] = int(radius2 * math.cos((angle[1] * math.pi) + MF.HEADING))
            murbot_coords[3] = int(radius2 * math.sin((angle[1] * math.pi) + MF.HEADING))
            murbot_coords[4] = int(radius2 * math.cos((angle[2] * math.pi) + MF.HEADING))
            murbot_coords[5] = int(radius2 * math.sin((angle[2] * math.pi) + MF.HEADING))
            canvas.create_polygon(x_coord + murbot_coords[0], y_coord + murbot_coords[1],
                                  x_coord + murbot_coords[2], y_coord + murbot_coords[3],
                                  x_coord + murbot_coords[4], y_coord + murbot_coords[5],
                                  fill='light green',
                                  outline='green',
                                  tags='MURbot')
            canvas.create_oval(x_coord + 5 * SCALE, y_coord + 5 * SCALE,
                               x_coord - 5 * SCALE, y_coord - 5 * SCALE,
                               outline='green',
                               tags='MURbot')

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
                canvas.create_oval(POS_X + x + 2 * SCALE, POS_Y + y + 2 * SCALE,
                                   POS_X + x - 2 * SCALE, POS_Y + y - 2 * SCALE,
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

        def reorganize_canvas(event):
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)
            canvas.xview_scroll(int(canvas.winfo_width() / -2), TK.UNITS)
            canvas.yview_scroll(int(canvas.winfo_height() / -2), TK.UNITS)


        canvas.xview_scroll(int(canvas.winfo_width() / -2), TK.UNITS)
        canvas.yview_scroll(int(canvas.winfo_height() / -2), TK.UNITS)

        scale.bind('<Motion>', redraw_canvas)
        scale.pack(pady=20, side='top')

        canvas.bind('<Configure>', reorganize_canvas)
        canvas.bind('<FocusIn>', redraw_canvas)
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



def CreateCanvasAndScale(parent_for_canvas, parent_for_scale):
    global CANVAS_W
    CANVAS_W = TK.Canvas(parent_for_canvas,
                         bg='white',
                         highlightthickness=0.5,
                         highlightcolor='#f6f6f6',
                         height=350,
                         xscrollincrement=1,
                         yscrollincrement=1)
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


