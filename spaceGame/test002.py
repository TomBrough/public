import Tkinter
import tkMessageBox
import time
import math

from sprite import *

# Program: test002.py
# Author: Tom Brough

# Description:

# This program rotates the space ship in a circle around a fixed
# point in space (rather than spinning around on its own centre
# point).

# The speed factor (here set to 20) determins how big the circular
# path is. Note the spacecraft uses index to choose an image that
# matches the nose of the space craft to its current angle of
# trajectory. This angle is constantly changing thus giving it
# a circular movement around the fixed point.

# Setup "Top" frame, space canvas and space ship sprite as we
# did in test001.py. However note that initial x and y have
# been altered in this version.

top = Tkinter.Tk()
space = Tkinter.Canvas(top, bg="black", height=600, width=600)

# Create sprite pass canvas, base filename, inital x,y and index)

ss = Sprite(space,"images/ss/ship_rotate",-70,110,0)

# Pack and update just as we did in test001.py.

space.pack()
top.update()

# This time we are going to set an initial speed as well as index.

i     = 0
speed = 20

while(True):

    # Calculate Vector & plot based on speed and
    # index angle.

    # In this case speed is constant while angle
    # is changing. Larger speads bigger circle.

    # This time we are going to use the vector method
    # to calculate movement and plot it onto the canvas
    # instead of the move method used in test001.py.

    # vector method uses speed and angle inferred from
    # from index (index * 6 degrees).

    ss.vector(speed,i) 

    # Update our screen as before

    top.update()

    # Move to next index (angle) as we did in test001.py.

    i = i + 1
    i = i % 60

    # wait a short time before plotting next move.
    # Again just as we did in test001.py

    time.sleep(0.0625)

time.sleep(2)
