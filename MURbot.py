import turtle
import random

coordinates = []
for i in range(200):
    x = random.randrange(-255, 255)
    y = random.randrange(-255, 255)
    t = x, y
    coordinates.append(t)

scr = turtle.Screen()
TR = turtle.Turtle()
TR.hideturtle()
TR.penup()

p = 0
while p < len(coordinates):
    c = coordinates[p]
    TR.setpos(c[0], c[1])
    TR.dot(10, 'blue')
    scr.title(str(p+1))
    p += 1

turtle.done()
