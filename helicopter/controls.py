import Tkinter

class Controls():

    top = None
    events = []

    def __init__(self,top):

        #receive the top frame as part of the initiation and
        #keep our own reference to it. 

        self.top = top

        # Now bind key events from the top frame to the
        # key_callback method in this class (see below).
 
        self.top.bind("<Key>",self.key_callback)

    def key_callback(self,event):

        # When we receive an event just append it to
        # our own events list (self.events)

        self.events.append(event.keycode)

    def get_event(self):

        # If the user asks for an event from the event
        # list give them the top most (pop it).

        # list is thus processed in FIFO order
        # First In, First Out

        if(len(self.events) > 0):
            return(self.events.pop(0))
        else:
            return(None)

