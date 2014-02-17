import requests
import math
import os

from sprite import Sprite, ScrollSprite


class MapTileManager():

    # Large tile matries require high compute time and rendering in the cycle. By managing
    # the number of tiles in the list to thoes that are necessary to keep the viewable
    # map area completly covered in tiles plus a buffer area.

    # Because we will be fetching tiles into the cache and re-reading tiles from the cache
    # if user back tracks beyond the 11 x 11 PERIMETER_FETCH matrix. we need a strategy for
    # keeping order as efficiently as posible.

    # FETCH Matries are used to determine which tiles (relative to current position) need fetching.
    # and which ones need removing.
    #
    # The FETCHES matrix is used during initation of the program and
    # is a full 9 x 9 matrix of tiles required to fill the canvas area + working buffer.
    #
    # The PERIMETER_FETCH contains the relative matrix co-ordinates for a perimeter only of a 11 x 11
    # matrix. These are fetched when master object crosses tile threshold.a
    #
    # The PERMITER_REMOVE matrix is an even larger 13 x 13 matrix (perimeter only). If we remove anything
    # beyond the perimeter boarder then this will remove unessary tiles in the tile list thus keeping.
    # tile movement calculation and rendering to a minmum.


    FETCHES          =                 [(-4,-4),(-3,-4),(-2,-4),(-1,-4),( 0,-4),( 1,-4),( 2,-4),( 3,-4),( 4,-4),
                                        (-4,-3),(-3,-3),(-2,-3),(-1,-3),( 0,-3),( 1,-3),( 2,-3),( 3,-3),( 4,-3),
                                        (-4,-2),(-3,-2),(-2,-2),(-1,-2),( 0,-2),( 1,-2),( 2,-2),( 3,-2),( 4,-2),
                                        (-4,-1),(-3,-1),(-2,-1),(-1,-1),( 0,-1),( 1,-1),( 2,-1),( 3,-1),( 4,-1),
                                        (-4, 0),(-3, 0),(-2, 0),(-1, 0),( 0, 0),( 1, 0),( 2, 0),( 3, 0),( 4, 0),
                                        (-4, 1),(-3, 1),(-2, 1),(-1, 1),( 0, 1),( 1, 1),( 2, 1),( 3, 1),( 4, 1),
                                        (-4, 2),(-3, 2),(-2, 2),(-1, 2),( 0, 2),( 1, 2),( 2, 2),( 3, 2),( 4, 2),
                                        (-4, 3),(-3, 3),(-2, 3),(-1, 3),( 0, 3),( 1, 3),( 2, 3),( 3, 3),( 4, 3),
                                        (-4, 4),(-3, 4),(-2, 4),(-1, 4),( 0, 4),( 1, 4),( 2, 4),( 3, 4),( 4, 4)]

    PERIMETER_FETCH  =         [(-5,-5),(-4,-5),(-3,-5),(-2,-5),(-1,-5),( 0,-5),( 1,-5),( 2,-5),( 3,-5),( 4,-5),( 5,-5),
                                (-5,-4),                                                                        ( 5,-4),
                                (-5,-3),                                                                        ( 5,-3),
                                (-5,-2),                                                                        ( 5,-2),
                                (-5,-1),                                                                        ( 5,-1),
                                (-5, 0),                                                                        ( 5, 0),
                                (-5, 1),                                                                        ( 5, 1),
                                (-5, 2),                                                                        ( 5, 2),
                                (-5, 3),                                                                        ( 5, 3),
                                (-5, 4),                                                                        ( 5, 4),
                                (-5, 5),(-4, 5),(-3, 5),(-2, 5),(-1, 5),( 0, 5),( 1, 5),( 2, 5),( 3, 5),( 4, 5),( 5, 5)]

    PERIMETER_REMOVE = [(-6,-6),(-5,-6),(-4,-6),(-3,-6),(-2,-6),(-1,-6),( 0,-6),( 1,-6),( 2,-6),( 3,-6),( 4,-6),( 5,-6),( 6,-6),
                        (-6,-5),                                                                                        ( 6,-5),
                        (-6,-4),                                                                                        ( 6,-4),
                        (-6,-3),                                                                                        ( 6,-3),
                        (-6,-2),                                                                                        ( 6,-2),
                        (-6,-1),                                                                                        ( 6,-1),
                        (-6, 0),                                                                                        ( 6, 0),
                        (-6, 1),                                                                                        ( 6, 1),
                        (-6, 2),                                                                                        ( 6, 2),
                        (-6, 3),                                                                                        ( 6, 3),
                        (-6, 4),                                                                                        ( 6, 4),
                        (-6, 5),                                                                                        ( 6, 5),
                        (-6, 6),(-5, 6),(-4, 6),(-3, 6),(-2, 6),(-1, 6),( 0, 6),( 1, 6),( 2, 6),( 3, 6),( 4, 6),( 5, 6),( 6, 6)]

    home    = None # tile x,y reference to first position (home) in the game.
    master  = None # reference to sprite object containg users sprite.
    canvas  = None # reference to canvas area in which sprites and other graphical objects are manipulated / mapped.
    tiles   = []   # list of tiles rendered.
    current = None # current x,y reference to tile currently "hosting" the master sprite object.
    scale   = None # scale used 0 - 19 map tiles 19 being the lagest scale.

    def __init__(self,master,canvas,home=(257008,176745),scale=19):
        self.master  = master
        self.canvas  = canvas
        self.home    = home
        self.current = home
        self.scale   = scale

    def pre_render(self,trange=10):
        for x in range(self.home[0] - trange, self.home[0] + trange):
            for y in range(self.home[1] - trange,self.home[1] + trange):
                tile_ref = (x,y)
                map = "cache/map-%d-%d-%d_000.png" % (self.scale,tile_ref[0],tile_ref[1])

                if(not os.path.exists(map)):
                    url = "http://a.tile.openstreetmap.org/%d/%d/%d.png" % \
                          (self.scale,tile_ref[0],tile_ref[1])
                    response = requests.get(url)

                    file = open(map,"wb")
                    file.write(response.content)
                    file.flush()
                    file.close()

                fetch = (x,y)
                new_x = ((x - self.home[0]) * 256) # - self.master.virtual_x
                new_y = ((y - self.home[1]) * 256) # - self.master.virtual_y

                sprite = Sprite(self.canvas,"cache/map-%d-%d-%d" % \
                           (self.scale,tile_ref[0],tile_ref[1]),new_x,new_y,0,1)
                self.tiles.append(sprite)

    #def load_cached_tiles(self):

    #    for file in os.listdir("cache"):

    #        (dummy,x,y) = file.split("-")
    #        (y,dummy)   = y.split("_")

    #        x = (int(x) - self.home[0]) * 256
    #        y = (int(y) - self.home[1]) * 256

    #        sprite = Sprite(self.canvas,"cache/%s" % (file.split("_"))[0],
    #                        x,y,0,1)

    #        self.tiles.append(sprite)
    #        tile = self.tiles[-1]

    #    # In case there is no cache ....

    #    self.render_tiles()

    def check_tiles(self):

        check_x =  int((self.master.virtual_x / 256) + self.home[0]) 
        check_y =  int((self.master.virtual_y / 256) + self.home[1])

        if(check_x != self.current[0] or check_y != self.current[1]):

            print self.current
            self.current = (check_x,check_y)
            print self.current

            self.render_tiles()

    def render_tiles(self):

        #new_tiles = []

        for fetch in self.FETCHES:
            tile_ref=(self.current[0]+fetch[0],self.current[1]+fetch[1])
            map = "cache/map-%d-%d-%d_000.png" % (self.scale,tile_ref[0],tile_ref[1])

            if(not os.path.exists(map)):
                url = "http://a.tile.openstreetmap.org/%d/%d/%d.png" % \
                      (self.scale,tile_ref[0],tile_ref[1])
                response = requests.get(url)

                file = open(map,"wb")
                file.write(response.content)
                file.flush()
                file.close()

            new_x = ((fetch[0] + self.current[0] - self.home[0]) * 256) - self.master.virtual_x
            new_y = ((fetch[1] + self.current[1] - self.home[1]) * 256) - self.master.virtual_y

            sprite = ScrollSprite(self.canvas,"cache/map-%d-%d-%d" % \
                       (self.scale,tile_ref[0],tile_ref[1]),new_x,new_y,0,1)
            self.tiles.append(sprite)

        #self.tiles = new_tiles

    def move(self,offset_x,offset_y):

        for t in self.tiles:
            t.move(t.x - offset_x,t.y - offset_y,0)

def deg2num(lat_deg, lon_deg,zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)
