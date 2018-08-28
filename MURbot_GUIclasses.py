import tkinter as TK
import MURbot_Functions as MF
import random
import math
import time

'''Global variables'''
MB_POS = [0, 0]                         #The x, y coordinate of MURbot
MB_CANV_CRD = [0, 0]                    #X, y coordinates for drawing
ENV_OFFSET = [0, 0]                     #Enviroment offset coordinates for drawing
POS_PER_CANVAS = [0, 0]                 #MB_CANV_CRD / canvas dimensions -> positioning driver when the window size has changed
CANVAS_W = 0                            #Canvas handler
SCALE_W = 0                             #Sclaing scrollbar handler
SCALE = 1                               #Scale value
MB_VELOCITY = [0, 2]                    #The velocity in y (heading) and x (perpendicular to heading) in m/s regarding regarding the IMU sensor


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

        def radar(event):
            test_data = []
            coords_for_canvas = []
            a = 1
            while a < 181:
                n = (a, random.randrange(180, 255))
                test_data.append(n)
                del n
                a += 1

            i = 0
            while i < len(test_data):
                tup = test_data[i]
                alpha = tup[0] * math.pi / 180
                x = math.sin(alpha) * tup[1]
                y = math.cos(alpha) * tup[1]
                n = (x, y)
                coords_for_canvas.append(n)
                i += 1

            observation = {'ID':     int(time.time()),
                           'MBpos':  (MB_POS[0], MB_POS[1]),
                           'MBCanvCrd': MB_CANV_CRD,
                           'DottOffset': ENV_OFFSET,
                           'RawRD':  test_data,
                           'Coords': coords_for_canvas}

            MF.RADARDATA.append(observation)
            #print(MF.RADARDATA)
            redraw_canvas(event)

        def forward(event):
            global MB_POS, MB_CANV_CRD
            xd = MB_VELOCITY[1] * math.cos(MF.HEADING)
            yd = MB_VELOCITY[1] * math.sin(MF.HEADING)
            MB_POS[0] += xd
            MB_POS[1] -= yd
            MB_CANV_CRD[0] += xd * SCALE
            MB_CANV_CRD[1] += yd * SCALE
            redraw_canvas(event)
            canvas.update()

        def backward(event):
            global MB_POS, MB_CANV_CRD
            xd = MB_VELOCITY[1] * math.cos(MF.HEADING)
            yd = MB_VELOCITY[1] * math.sin(MF.HEADING)
            MB_POS[0] -= xd
            MB_POS[1] += yd
            MB_CANV_CRD[0] -= xd * SCALE
            MB_CANV_CRD[1] -= yd * SCALE
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
            global MB_CANV_CRD, ENV_OFFSET, POS_PER_CANVAS
            canvas.delete('MURbot')
            canvas.delete('Env_dots')
            canvas.delete('rec')

            #Establish an inner rectangle zone in the canvas. If the MB reaches the border the canvas scrolls automatically to keep it visiable
            border_thickness = 0.2  #in percentage of the canvas width and height
            border_left = canvas.winfo_width() * border_thickness
            border_right = canvas.winfo_width() * (1 - border_thickness)
            border_up = canvas.winfo_height() * border_thickness
            border_down = canvas.winfo_height() * (1 - border_thickness)
            canvas.create_rectangle(border_left, border_down, border_right, border_up, fill=None, outline='red', tags='rec')

            #Out_of_zone flag shows if the MB outside or not of the borders
            if MB_CANV_CRD[0] < border_left - 5 or MB_CANV_CRD[0] > border_right + 5 or \
                    MB_CANV_CRD[1] < border_up - 5 or MB_CANV_CRD[1] > border_down + 5:
                out_of_zone = True
            else:
                out_of_zone = False

            #The canvas scrolls automatically only if the MB inside the borders to keep it visible
            if out_of_zone == False:
                if MB_CANV_CRD[0] < border_left:
                    d = border_left - MB_CANV_CRD[0]
                    MB_CANV_CRD[0] += d
                    ENV_OFFSET[0] += d
                if MB_CANV_CRD[0] > border_right:
                    d = MB_CANV_CRD[0] - border_right
                    MB_CANV_CRD[0] -= d
                    ENV_OFFSET[0] -= d
                if MB_CANV_CRD[1] < border_up:
                    d = border_up - MB_CANV_CRD[1]
                    MB_CANV_CRD[1] += d
                    ENV_OFFSET[1] += d
                if MB_CANV_CRD[1] > border_down:
                    d = MB_CANV_CRD[1] - border_down
                    MB_CANV_CRD[1] -= d
                    ENV_OFFSET[1] -= d

            POS_PER_CANVAS[0] = MB_CANV_CRD[0] / canvas.winfo_width()
            POS_PER_CANVAS[1] = MB_CANV_CRD[1] / canvas.winfo_height()
            draw_murbot(MB_CANV_CRD)
            env_dots(MF.RADARDATA)


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
            canvas.create_polygon(coords[0] + murbot_coords[0], coords[1] + murbot_coords[1],
                                  coords[0] + murbot_coords[2], coords[1] + murbot_coords[3],
                                  coords[0] + murbot_coords[4], coords[1] + murbot_coords[5],
                                  fill='light green',
                                  outline='green',
                                  tags='MURbot')
            canvas.create_oval(coords[0] + 5 * SCALE, coords[1] + 5 * SCALE,
                               coords[0] - 5 * SCALE, coords[1] - 5 * SCALE,
                               outline='green',
                               tags='MURbot')

        def env_dots(radardata):
            n = 0
            while n < len(radardata):
                obs = radardata[n]
                obs_pos = obs['MBpos']
                dot_coords = obs['Coords']
                i = 0
                while i < len(dot_coords):
                    tup = dot_coords[i]
                    x = (obs_pos[0] + tup[0]) * SCALE
                    y = -(obs_pos[1] + tup[1]) * SCALE
                    canvas.create_oval(x + 2 * SCALE, y + 2 * SCALE,
                                       x - 2 * SCALE, y - 2 * SCALE,
                                       fill='red',
                                       tag='Env_dots')
                    i += 5

                #for keys, values in obs.items():
                    #print(keys, values)

                n += 1

        def scroll_right(event):
            global DRAWING_CTRL
            canvas.xview_scroll(1, TK.UNITS)
            DRAWING_CTRL[0] = DRAWING_CTRL[0] + 1

        def scroll_left(event):
            global DRAWING_CTRL
            canvas.xview_scroll(-1, TK.UNITS)
            DRAWING_CTRL[0] = DRAWING_CTRL[0] - 1

        def scroll_up(event):
            global DRAWING_CTRL
            canvas.yview_scroll(-1, TK.UNITS)
            DRAWING_CTRL[1] = DRAWING_CTRL[1] + 1

        def scroll_down(event):
            global DRAWING_CTRL
            canvas.yview_scroll(1, TK.UNITS)
            DRAWING_CTRL[1] = DRAWING_CTRL[1] - 1

        def reorganize_canvas(event):
            global MB_CANV_CRD
            MB_CANV_CRD[0] = canvas.winfo_width() * POS_PER_CANVAS[0]
            MB_CANV_CRD[1] = canvas.winfo_height() * POS_PER_CANVAS[1]
            redraw_canvas(event)


        MB_CANV_CRD[0] += int(canvas.winfo_width() / 2)
        MB_CANV_CRD[1] += int(canvas.winfo_height() / 2)

        scale.bind('<Motion>', redraw_canvas)
        scale.pack(pady=20, side='top')

        canvas.bind('<Configure>', reorganize_canvas)
        canvas.bind('<FocusIn>', redraw_canvas)
        canvas.bind('<Up>', forward)
        canvas.bind('<Down>', backward)
        canvas.bind('<Left>', left)
        canvas.bind('<Right>', right)
        canvas.bind('<Control_L>', radar)
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
                       from_=0.1,
                       to=1.9,
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


