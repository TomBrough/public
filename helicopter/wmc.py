import cwiid

class Master():
   index = 0
   speed = 0

class WiiController():

    wm = None
    master = None

    def __init__(self,master):
        print "press 1 + 2 buttons together to sync"
        self.wm = cwiid.Wiimote()
        print "sync completed"
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        self.master = master

    def get_state(self):
        self.master.speed = (self.wm.state['acc'][2] - 135) / 2
        self.master.index = self.master.index + ((self.wm.state['acc'][0] - 120) / 10)
        self.master.index = self.master.index % 60


if(__name__ == "__main__"):
    test = Master()
    wc = WiiController(test)
    while(True):
        test.index = 0
        wc.get_state()
        print("%d,%d" % (test.speed,test.index))
