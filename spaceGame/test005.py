import Tkinter
import tkMessageBox
import time
import math

from sprite import *
from controls import *

# Program: test005.py
# Author: Tom Brough

# Description:



top = Tkinter.Tk()
space = Tkinter.Canvas(top, bg="black", height=600, width=600)

# Now we hook the controls management stack into the
# "top" frame object.

# Tkinter fires events to active frames. Top is the
# master frame and receives all events. The
# Controls class binds keyboard events to the top
# frame and adds them to a list of events.

# See controls.py for more info.

controls = Controls(top)

ss = Sprite(space,"images/ss/ship_rotate",-70,110,0)
tpod = Sprite(space,"images/tpod/tpod",200,200,0)

space.pack()
top.update()

i = 0
speed = 20
play = True

while(play):

    # Get an event (returns None if there are none...)

    event = controls.get_event()

    tpod.move(200,200,(i*59 % 60))

    while(event != None):
        ss.process_event(event)

        if(event == 9):
            # Esc Pressed exit play...
            play = False

        print event
        event = controls.get_event()

    ss.vector(ss.speed,ss.index)

    # And everything else you have seen before...

    top.update()

    i = i + 1
    i = i % 60

    time.sleep(0.0625)
    top.mainloop(1)

time.sleep(2)
