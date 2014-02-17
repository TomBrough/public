import math
import urllib2
import Tkinter
import time
import ImageTk
import Image
import os
import time

from controls import Controls
from sprite import Sprite, ScrollSprite, HelicopterSprite

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

r = 11 
zoom = 18 

tile_ref = deg2num(50.4675,-3.5266,zoom) # Torbay
tile_ref = deg2num(50.43384,-3.56599,zoom) # Paignton Library
tile_ref = deg2num(50.72502,-3.52910,zoom) # Exeter Library

images = []
play = True

top = Tkinter.Tk()
canvas = Tkinter.Canvas(top,scrollregion=(0,0,((r+1)*2*256),((r+1)*2*256)),height=500,width=500,bg="white")
print (canvas.cget("scrollregion")).split(" ")[3]
canvas.config(xscrollincrement='1',yscrollincrement='1')
canvas.pack(fill=Tkinter.BOTH)

for i in range(tile_ref[0] - r, tile_ref[0] + r):
        for j in range(tile_ref[1] - r, tile_ref[1] + r):

                if(not os.path.exists("maps/%d-%d-%d.png" % (zoom,i,j))):
                        page = urllib2.urlopen("http://a.tile.openstreetmap.org/%d/%d/%d.png" % (zoom,i,j))

                        file = open("maps/%d-%d-%d.png" % (zoom,i,j),"wb")
                        data = page.read()
                        file.write(data)
                        file.flush()
                        file.close()

                images.append(ImageTk.PhotoImage(file="maps/%d-%d-%d.png" % (zoom,i,j)))

                canvas.create_image((i - tile_ref[0] + r + 1) * 256,(j - tile_ref[1] + r + 1) * 256,image=images[-1])
        print (float(i - tile_ref[0] + r) / ((r *2) +1 ) * 100)

helicopter = HelicopterSprite(canvas,"images/helicopter/red/helicopter",(r*256)+256+250,(r*256)+256+250,0,60)
controls = Controls(top)
event = controls.get_event()
canvas.xview_moveto(0.5)
canvas.yview_moveto(0.5)

prev_time = time.time()

while(play):

    event = controls.get_event()

    while(event != None): 
        helicopter.process_event(event)

        if(event == 9):
            play = False

        event = controls.get_event()

    helicopter.vector(helicopter.speed,helicopter.index)
    helicopter.tick()
    #helicopter.move(helicopter.virtual_x,helicopter.virtual_y,helicopter.index)
    #top.update()

    if(helicopter.virtual_x > 250 and helicopter.virtual_x < (helicopter.c_width - 506)):
        canvas.xview_scroll(int(helicopter.offset_x),"units")
    if(helicopter.virtual_y > 250):
        canvas.yview_scroll(int(helicopter.offset_y),"units")

    #helicopter.tick()

    top.update()

    while((prev_time + 0.04) > time.time()):
        continue

    prev_time = time.time()

    #time.sleep(0.0625)

    #print time.time()

    #time.sleep(1)
    top.mainloop(1)
