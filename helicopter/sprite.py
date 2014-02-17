import Tkinter
import tkMessageBox
from PIL import ImageTk # apt-get install python-imaging-tk
import time
import math

class Sprite():

    canvas   = None
    images   = []
    id       = None
    index    = 0
    speed    = 0
    x        = 0
    y        = 0
    offset_x = 0
    offset_y = 0
    ticker   = 0
    frames   = 0

    def __init__(self,canvas,root_filename,x,y,index,frames=60):

        self.canvas = canvas
        self.init_images(root_filename,frames)

        self.id    = self.canvas.create_image(x,y,anchor=Tkinter.NW,image=self.images[index]) 

        self.x     = x
        self.y     = y
        self.index = index
        self.frames = frames

    def init_images(self,root_filename,frames):
        self.images = []

        for i in range(0,frames):
            filename = "%s_%03d.gif" % (root_filename,i)
            self.images.append(Tkinter.PhotoImage(file=filename))

    def static(self,x,y,index):

        # Creates static objects on canvas
        # Object is not recorded and cannot be removed safely without
        # id.

        self.canvas.create_image(x,y,anchor=Tkinter.NW,image=self.images[index])

    def move(self,x,y,index):

        self.canvas.delete(self.id)

        self.id    = self.canvas.create_image(x,y,anchor=Tkinter.NW,image=self.images[index])
        self.x     = x
        self.y     = y
        self.index = index

    def vector(self,speed,index):

        # update my speed and index.

        self.speed = speed
        self.index = index

        # index is angle (in degrees * 6)
        # computers do angles in radians (rads)
        # 2 * pi radians in a circle or pi / 180 = 1 degree
        # rotation starts from 3 o'clock (East) position (by mathmatical convention)
        # so we can bring this back to 12 o'clock (North) position by subtracting 90

        # Thus we get: 

        rads = (math.pi/180.0) * ((self.index*6) - 90.0)

        # New Co-ordinates are calculated thus:

        self.offset_x = self.speed * math.cos(rads)
        self.offset_y = self.speed * math.sin(rads)

        self.x = self.x + self.offset_x
        self.y = self.y + self.offset_y

        self.move(self.x,self.y,index)

    def process_event(self,event):

        # Process any event passed here for processing....

        if(event == 38):
           self.speed = self.speed + 1
        
        if(event == 52):
           self.speed = self.speed - 1

        if(event == 59):
           self.index = self.index - 1

        if(event == 60):
           self.index = self.index + 1

        # Remember index can must be 0 - 59 so use our magic
        # modulus trick

        self.index = self.index % 60

    def tick(self):
        pass


class PodSprite(Sprite):

    def __init__(self,canvas,root_filename,x,y,index):
        Sprite.__init__(self,canvas,root_filename,x,y,index)

    def tick(self,offset_x,offset_y):

        self.x = self.x - offset_x
        self.y = self.y - offset_y

        self.ticker = self.ticker + 1
        self.index  = self.ticker  % 60

        self.move(self.x,self.y,self.index) 


class ScrollSprite(Sprite):

    canvas   = None # canvas that sprite is associated with.
    images   = []   # list of images (frames) in sprite
    id       = None # id of sprite in canvas
    frames   = 0    # No. of frame in sprite
    index    = 0    # index to currently visible frame of sprite
    speed    = 0    # speed of object
    x        = 0    # x co-ord in visible canvas
    y        = 0    # y co-ord in visible canvas
    offset_x = 0    # offset x caused by "rotational direction" of sprite
    offset_y = 0    # offest y caused by "rotational direction" of sprite
    ticker   = 0    # ticker for animated frame sprites
    virtual_x = 0   # x co-ord in "virtual" space
    virtual_y = 0   # y co-ord in "virutal" space
    c_height  = 0   # canvas height (y)
    c_width   = 0   # canvas width  (x)

    def __init__(self,canvas,root_filename,x,y,index,frames=60):
        Sprite.__init__(self,canvas,root_filename,x,y,index,frames)

        self.canvas = canvas
        self.frames = frames
        self.init_images(root_filename,frames)

        self.id        = self.canvas.create_image(x,y,anchor=Tkinter.NW,image=self.images[index]) 

        self.x         = x
        self.y         = y

        self.virtual_x = x
        self.virtual_y = y

        self.index     = index
        (dummy1,dummy2,self.c_width,self.c_height) = self.canvas.cget("scrollregion").split(" ") 
        self.c_width    = int(self.c_width)
        self.c_height   = int(self.c_height)


    def init_images(self,root_filename,frames):
        self.images = []

        for i in range(0,frames):
            filename = "%s_%03d.png" % (root_filename,i)
            self.images.append(ImageTk.PhotoImage(file=filename))

    def static(self,x,y,index):

        # Creates static objects on canvas
        # Object is not recorded and cannot be removed safely without
        # id.

        self.canvas.create_image(x,y,anchor=Tkinter.NW,image=self.images[index])

    def move(self,x,y,index):

        self.canvas.delete(self.id)

        self.id    = self.canvas.create_image(x,y,anchor=Tkinter.NW,image=self.images[index])
        self.x     = x
        self.y     = y
        self.index = index

    def vector(self,speed,index):

        # update my speed and index.

        self.speed = speed
        self.index = index

        # index is angle (in degrees * 6)
        # computers do angles in radians (rads)
        # 2 * pi radians in a circle or pi / 180 = 1 degree
        # rotation starts from 3 o'clock (East) position (by mathmatical convention)
        # so we can bring this back to 12 o'clock (North) position by subtracting 90

        # Thus we get: 

        rads = (math.pi/180.0) * ((self.index*(360.0/self.frames)) - 90.0)

        # New Co-ordinates are calculated thus:

        self.offset_x  = self.speed * math.cos(rads)
        self.offset_y  = self.speed * math.sin(rads)

        #self.x         = self.x + self.offset_x
        #self.y         = self.y + self.offset_y

        if(self.virtual_x >= 250 and 
           self.virtual_x <= (self.c_width - 250)):
            self.virtual_x = self.virtual_x + int(self.offset_x)
            self.x         = self.x + int(self.offset_x)

        if(self.virtual_x < 250):
            self.virtual_x = 250

        if(self.virtual_x > (self.c_width - 506)):
            self.virtual_x = self.c_width - 506

        if(self.virtual_y >= 250):
            self.virtual_y = self.virtual_y + int(self.offset_y)
            self.y         = self.y + int(self.offset_y)

        if(self.virtual_y < 250):
            self.virtual_y = 250

        self.move(self.x,self.y,index)

    def process_event(self,event):

        # Process any event passed here for processing....

        if(event == 38):
           self.speed = self.speed + 1
        
        if(event == 52):
           self.speed = self.speed - 1

        if(event == 59):
           self.index = self.index - 1

        if(event == 60):
           self.index = self.index + 1

        # Remember index can must be 0 - self.frames - 1 so use our magic
        # modulus trick

        self.index = self.index % self.frames

    def tick(self):
        pass


class PodSprite(Sprite):

    def __init__(self,canvas,root_filename,x,y,index):
        Sprite.__init__(self,canvas,root_filename,x,y,index)

    def tick(self,offset_x,offset_y):

        self.x = self.x - offset_x
        self.y = self.y - offset_y

        self.ticker = self.ticker + 1
        self.index  = self.ticker  % self.frames

        self.move(self.x,self.y,self.index) 


class HelicopterSprite(ScrollSprite):

    def __init__(self,canvas,root_filename,x,y,index,frames):
        ScrollSprite.__init__(self,canvas,root_filename,x,y,index,frames=60)


    def init_images(self,root_filename,frames):
        self.images = []

        for i in range(0,60):
            for j in range(0,15):
                filename = "%s_%03d_%03d.png" % (root_filename,i,j)
                self.images.append(ImageTk.PhotoImage(file=filename))

        print len(self.images)

    def tick(self):
        self.ticker = self.ticker + 2
        self.ticker = self.ticker % 15
        self.move(self.x,self.y,self.index)


    def move(self,x,y,index):

        self.canvas.delete(self.id)

        self.id    = self.canvas.create_image(x,y,anchor=Tkinter.NW,image=self.images[(index*15) + self.ticker])
        self.x     = x
        self.y     = y
        self.index = index
