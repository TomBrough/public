import Tkinter
import tkMessageBox
import time
import math

from sprite import *

# Program: test003.py
# Author: Tom Brough

# Description:

# This test program rotates around a fixed point in space while
# also rotating space ship's body around portal. Effectively
# a combination of test001.py and test002.py
# This gives us a space ship that looks like its out of
# control.

top = Tkinter.Tk()
space = Tkinter.Canvas(top, bg="black", height=600, width=600)

ss = Sprite(space,"images/ss/ship_rotate",-70,110,0)

space.pack()
top.update()

i = 0
speed = 20

while(True):

    # Angle and movement all done by vector method in Sprite class. 

    ss.vector(speed,i)

    # We can also manipulate Sprite directly using move for fine tuning.
    # In this case we are using the move method to provide a spin on
    # the body of the space craft while it is rotating in a circle around
    # an abritory point in space.

    ss.move(ss.x,ss.y,(i*2 % 60))

    # Experiment with i * 3, i * 4, i * ... the spin get more eratic the higher
    # the number. Try i * 30(+) to get a counter spin effect.

    # Update our screen

    top.update()

    # Move to next index (angle).

    i = i + 1

    # Reminder: if you wish you can make the craft circle counter clockwise by
    #           using i = i - 1 instead of the above.

    # Limit index to 60 (0 - 59) as each indexed image  represent 6 degree shift clockwise.

    i = i % 60

    time.sleep(0.0625)

time.sleep(2)
