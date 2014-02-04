import Tkinter
import tkMessageBox
import time
import math

from sprite import *

# Program: test004.py
# Author: Tom Brough

# Description:

# This test program extends test003.py by adding
# a new sprite Torpedo pod (tpod) into space
# at a fixed point adding it as a reference point
# for the spinning space ship.

# Spoiler: tpod's are fast indistructable pods containing torpedos
#          they will be manufactured by the base stations at 
#          defined intervals and automatically home in on the
#          space craft which can use them to replenish supplies.

# Spoiler 2: OK now I guess I have given away the fact that there
#            is going to be a base station object too!

top = Tkinter.Tk()
space = Tkinter.Canvas(top, bg="black", height=600, width=600)

ss = Sprite(space,"images/ss/ship_rotate",-70,110,0)

# And now we can use the Sprite class again to add the
# new tpod object.

tpod = Sprite(space,"images/tpod/tpod",200,200,0)

space.pack()
top.update()

i = 0
speed = 20

while(True):


    ss.vector(speed,i)
    ss.move(ss.x,ss.y,(i*2 % 60))

    # We can make the tpod object spin around
    # it's centre in just the same way that
    # we make the space craft rotate.....

    tpod.move(200,200,(i*59 % 60))

    # wow... that was easy!

    # And everything else you have seen before...

    top.update()

    i = i + 1
    i = i % 60

    time.sleep(0.0625)

time.sleep(2)
