import Tkinter
import tkMessageBox
import time
from sprite import *

# Program: test001.py
# Author: Tom Brough

# Decription:

# This test program rotates the space ship around itself.
# The centre of rotation is (more or less) the centre of
# The blue portal.

# Create the "master" or "top" frame for Tkinter.

top = Tkinter.Tk()

# Now create a canvas (called space)
space = Tkinter.Canvas(top, bg="black", height=600, width=600)

# Now create space ship sprite (ss), pass the canvas,
# image file root, initial x,y and index image (angle)

# Each Sprite is made up of 60 images (at 6 degree offsets)
# which allows rotation. The index value chooses the appropriate
# image and also implies the angle in degrees (based on index * 6)

# image root is the filename for the root image, so root image
# "xyz" is translated into xyz_000.gif to xyz_059.gif
# giving us the 60 different images at 6 degree offsets.
# if images do not exist or the root image name is incorrect
# loading will fail..... 

ss = Sprite(space,"images/ss/ship_rotate",100,100,0)

# If you want to learn more about Sprite class look at the
# sprite.py program..... 

# now pack the space canvas into the Tk master frame

space.pack()

# Update the master frame

top.update()

# initialise our index counter

i = 0

while(True): 
    # move our Sprite to fixed point in space (150,150) and
    # choose the image associated with our index counter

    ss.move(150,150,i)

    # update the frame with the Sprite/Canvas Changes
    
    top.update()

    # Increment our index (to go counter clockwise
    # decrement i instead eg i = i - 1)

    i = i + 1

    # Index runs from 0 to 59 so use modulus operator (%)
    # to restrict i to 60 values (0 to 59).

    i = i % 60

    # go to sleep for an 8th of a second. Reduce this
    # value if you want to rotate faster. But remember
    # you may suffer a blackout ;-) .....

    time.sleep(0.125)

# If we ever drop out of the "infinite" loop
# wait a couple of seconds before exiting....

time.sleep(2)
