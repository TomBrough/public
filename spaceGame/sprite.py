import Tkinter
import tkMessageBox
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

    def __init__(self,canvas,root_filename,x,y,index,frames=60):

        self.canvas = canvas
        self.init_images(root_filename,frames)

        self.id    = self.canvas.create_image(x,y,anchor=Tkinter.NW,image=self.images[index]) 

        self.x     = x
        self.y     = y
        self.index = index


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
