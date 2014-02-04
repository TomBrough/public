import Tkinter
import tkMessageBox
import time
import math

from sprite import *
from controls import *

# Program: test006.py
# Author: Tom Brough

# Description:


i = 0
speed = 20
play = True

buoys = [( 413, -915, 0),( 451,-1284, 1),( 612,-1584, 2),( 772,-1849, 3),
         ( 900,-2177, 4),(1040,-2451, 5),(1177,-2665, 6),(1372,-2898, 7),
         (1561,-3080, 8),(1802,-3234, 9),(2068,-3337,10),(2356,-3351,11),
         (2591,-3255,12),(2672,-3026,13),(2699,-2785,14),(2685,-2502,15),
         (2609,-2230,16),(2412,-1991,17),(2157,-1814,18),(1815,-1748,19),
         (1461,-1811,20),(1200,-1879,21),( 966,-1954,22),( 733,-2086,23),
         ( 495,-2257,24),( 359,-2540,25),( 241,-2831,26),( 210,-3187,27),
         ( 198,-3445,28),( 183,-3736,29),( 186,-4017,30),( 245,-4300,31),
         ( 434,-4502,32),( 727,-4615,33),(1020,-4664,34),(1337,-4656,35),
         (1655,-4623,36),(1964,-4599,37),(2257,-4559,38),(2591,-4518,39),
         (2886,-4436,40)]
buoy_sprites = []


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

ss = Sprite(space,"images/ss/ship_rotate",150,150,0)
#tpod = PodSprite(space,"images/tpod/tpod",230,0,0)
btux = Sprite(space,"images/small_tux",300,-1200,0,1)

for b in buoys:
    (bx,by,bindex) = b
    by = by + 1000
    buoy_sprites.append(PodSprite(space,"images/buoy/%03d/buoy_%03d" % (bindex,bindex),bx,by,0))

space.pack()
top.update()

while(play):

    btux.move(btux.x - ss.offset_x,btux.y - ss.offset_y,0)
    # Get an event (returns None if there are none...)

    event = controls.get_event()

    #tpod.tick(ss.offset_x,ss.offset_y)

    for b in buoy_sprites:
        b.tick(ss.offset_x,ss.offset_y)

    while(event != None):
        ss.process_event(event)

        if(event == 9):
            # Esc Pressed exit play...
            play = False

        event = controls.get_event()

    ss.vector(ss.speed,ss.index)
    ss.move(150,150,ss.index)

    # And everything else you have seen before...

    top.update()

    i = i + 1
    i = i % 60

    time.sleep(0.0625)
    top.mainloop(1)

time.sleep(2)
