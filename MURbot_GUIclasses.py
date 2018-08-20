import tkinter as TK
import MURbot_Functions as MF
import random
import math

'''Global variables'''
MURBOT_POSITION = [0, 0]            #The x, y coordinate of MURbot
TOP_LEFT_CANVAS_COORD = [0, 0]      #The x, y coordinate of the top left corner of the canvas
MB_VELOCITY = [0, 2]                #The velocity in y (heading) and x (perpendicular to heading) direction in m/s regarding regarding the IMU sensor
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
            global MURBOT_POSITION
            MURBOT_POSITION[0] += MB_VELOCITY[1] * math.cos(MF.HEADING)
            MURBOT_POSITION[1] -= MB_VELOCITY[1] * math.sin(MF.HEADING)
            print('MBpos: ' + str(MURBOT_POSITION))
            redraw_canvas(event)
            canvas.update()

        def backward(event):
            global MURBOT_POSITION
            MURBOT_POSITION[0] -= MB_VELOCITY[1] * math.cos(MF.HEADING)
            MURBOT_POSITION[1] += MB_VELOCITY[1] * math.sin(MF.HEADING)
            print('MBpos: ' + str(MURBOT_POSITION))
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
            global TOP_LEFT_CANVAS_COORD
            canvas.delete('MURbot')

            i = 0.2     #percentege of canvas area what has to be always visable
            border_left = TOP_LEFT_CANVAS_COORD[0] + canvas.winfo_width() * i
            border_right = TOP_LEFT_CANVAS_COORD[0] + canvas.winfo_width() * (1 - i)
            border_up = TOP_LEFT_CANVAS_COORD[1] - canvas.winfo_height() * i
            border_down = TOP_LEFT_CANVAS_COORD[1] - canvas.winfo_height() * (1 - i)

            if MURBOT_POSITION[0] < border_left - 2 or MURBOT_POSITION[0] > border_right + 2 or \
                    MURBOT_POSITION[1] > border_up + 2 or  MURBOT_POSITION[1] < border_down - 2:
                out_of_zone = True
            else:
                out_of_zone = False

            if out_of_zone == False:
                if MURBOT_POSITION[0] < border_left:
                    canvas.xview_scroll(-MB_VELOCITY[1], TK.UNITS)
                    TOP_LEFT_CANVAS_COORD[0] = TOP_LEFT_CANVAS_COORD[0] - MB_VELOCITY[1]
                if MURBOT_POSITION[0] > border_right:
                    canvas.xview_scroll(MB_VELOCITY[1], TK.UNITS)
                    TOP_LEFT_CANVAS_COORD[0] = TOP_LEFT_CANVAS_COORD[0] + MB_VELOCITY[1]
                if MURBOT_POSITION[1] > border_up:
                    canvas.yview_scroll(-MB_VELOCITY[1], TK.UNITS)
                    TOP_LEFT_CANVAS_COORD[1] = TOP_LEFT_CANVAS_COORD[1] + MB_VELOCITY[1]
                if MURBOT_POSITION[1] < border_down:
                    canvas.yview_scroll(MB_VELOCITY[1], TK.UNITS)
                    TOP_LEFT_CANVAS_COORD[1] = TOP_LEFT_CANVAS_COORD[1] - MB_VELOCITY[1]

            draw_murbot(MURBOT_POSITION)
            print('MBpos: ' + str(MURBOT_POSITION))
            print('TPLC: ' + str(TOP_LEFT_CANVAS_COORD))

        def draw_murbot(coords):
            angle = [0, 0.66, 1.33]
            murbot_coords = [0, 0, 0, 0, 0, 0]
            radius = SCALE * 30
            radius2 = SCALE * 20.6
            murbot_coords[0] = int(radius * math.cos((angle[0] * math.pi) + MF.HEADING))
            murbot_coords[1] = int(radius * math.sin((angle[0] * math.pi) + MF.HEADING))
            murbot_coords[2] = int(radius2 * math.cos((angle[1] * math.pi) + MF.HEADING))
            murbot_coords[3] = int(radius2 * math.sin((angle[1] * math.pi) + MF.HEADING))
            murbot_coords[4] = int(radius2 * math.cos((angle[2] * math.pi) + MF.HEADING))
            murbot_coords[5] = int(radius2 * math.sin((angle[2] * math.pi) + MF.HEADING))
            canvas.create_polygon(coords[0] + murbot_coords[0], -coords[1] + murbot_coords[1],
                                  coords[0] + murbot_coords[2], -coords[1] + murbot_coords[3],
                                  coords[0] + murbot_coords[4], -coords[1] + murbot_coords[5],
                                  fill='light green',
                                  outline='green',
                                  tags='MURbot')
            canvas.create_oval(coords[0] + 5 * SCALE, -coords[1] + 5 * SCALE,
                               coords[0] - 5 * SCALE, -coords[1] - 5 * SCALE,
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
                canvas.create_oval(MURBOT_POSITION + x + 2 * SCALE, POS_Y + y + 2 * SCALE,
                                   MURBOT_POSITION + x - 2 * SCALE, POS_Y + y - 2 * SCALE,
                                   fill='red',
                                   tag='Env_dots')
                i += 5

        def scroll_right(event):
            global TOP_LEFT_CANVAS_COORD
            canvas.xview_scroll(1, TK.UNITS)
            TOP_LEFT_CANVAS_COORD[0] = TOP_LEFT_CANVAS_COORD[0] + 1
            print('TPLC: ' + str(TOP_LEFT_CANVAS_COORD))

        def scroll_left(event):
            global TOP_LEFT_CANVAS_COORD
            canvas.xview_scroll(-1, TK.UNITS)
            TOP_LEFT_CANVAS_COORD[0] = TOP_LEFT_CANVAS_COORD[0] - 1
            print('TPLC: ' + str(TOP_LEFT_CANVAS_COORD))

        def scroll_up(event):
            global TOP_LEFT_CANVAS_COORD
            canvas.yview_scroll(-1, TK.UNITS)
            TOP_LEFT_CANVAS_COORD[1] = TOP_LEFT_CANVAS_COORD[1] + 1
            print('TPLC: ' + str(TOP_LEFT_CANVAS_COORD))

        def scroll_down(event):
            global TOP_LEFT_CANVAS_COORD
            canvas.yview_scroll(1, TK.UNITS)
            TOP_LEFT_CANVAS_COORD[1] = TOP_LEFT_CANVAS_COORD[1] - 1
            print('TPLC: ' + str(TOP_LEFT_CANVAS_COORD))

        def reorganize_canvas(event):
            global TOP_LEFT_CANVAS_COORD
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)
            TOP_LEFT_CANVAS_COORD = [0, 0]
            canvas.xview_scroll(int(canvas.winfo_width() / -2), TK.UNITS)
            canvas.yview_scroll(int(canvas.winfo_height() / -2), TK.UNITS)
            TOP_LEFT_CANVAS_COORD[0] = canvas.winfo_width() / -2
            TOP_LEFT_CANVAS_COORD[1] = canvas.winfo_height() / 2
            print('TPLC: ' + str(TOP_LEFT_CANVAS_COORD))

        canvas.xview_scroll(int(canvas.winfo_width() / -2), TK.UNITS)
        canvas.yview_scroll(int(canvas.winfo_height() / -2), TK.UNITS)
        TOP_LEFT_CANVAS_COORD[0] = TOP_LEFT_CANVAS_COORD[0] - int(canvas.winfo_width() / 2)
        TOP_LEFT_CANVAS_COORD[1] = TOP_LEFT_CANVAS_COORD[1] + int(canvas.winfo_height() / 2)
        print('TPLC: ' + str(TOP_LEFT_CANVAS_COORD))

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


