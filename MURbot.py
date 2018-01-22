import turtle
import random
import math

sensor_values = []
for i in range(530):
    dist = random.randrange(3, 255)
    t = i, dist
    sensor_values.append(t)

scr = turtle.Screen()
TR = turtle.Turtle()
TR.hideturtle()
TR.penup()
ch = math.pi / 530

for p in range(len(sensor_values)):
    alpha = sensor_values[p][0] * ch
    a = math.sin(alpha) * sensor_values[p][1]
    b = math.cos(alpha) * sensor_values[p][1]
    # print(str(sensor_values[p]) + ': alpha:' + str(alpha))
    # print('  ' + str(math.sin(alpha)) + ' * ' + str(value[1]) + ' = ' + str(a))
    # print('  ' + str(math.cos(alpha)) + ' * ' + str(value[1]) + ' = ' + str(b))
    TR.setpos(-a, b)
    TR.dot(10, 'blue')
    scr.title(str(p + 1))

turtle.done()
