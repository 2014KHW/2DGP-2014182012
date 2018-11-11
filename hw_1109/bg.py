from pico2d import *

class Parallex_Pics:
    def __init__(self, level):
        self.l, self.r = False, False
        self.pic = self.init_pics_by_level(level)
        self.x, self.y = 0, self.init_y_by_level(level)
        self.speed = 1 * level
        self.lev = level
    def init_pics_by_level(self, level):
        pics_table = {
            1: load_image('../term/Pics/sky_background.png'),
            2: load_image('../Pics/ice_cream.png'),
            3: load_image('../Pics/ground.png')
        }
        return pics_table[level]
    def init_y_by_level(self, level):
        y_table = {
            1: get_canvas_height()//1,
            2: get_canvas_height()//2,
            3: get_canvas_height()//1
        }
        return y_table[level]
    def draw(self):
        px = int(self.x) * self.pic.w//get_canvas_width()#그림파일 상 x크기
        # 그림파일 상 y크기
        if self.lev is 1: sy, py = 0, int(self.pic.h)
        elif self.lev is 2: sy, py = 0, int(self.pic.h/2)
        elif self.lev is 3: sy, py = self.pic.h//2, int(self.pic.h)
        # 그림파일의 끝 변수
        lx = self.pic.w - px
        #오른쪽에 그려지는
        self.pic.clip_draw_to_origin(0, sy, px, py, get_canvas_width() - int(self.x), 0, int(self.x), self.y)
        #왼쪽에 그려지는
        self.pic.clip_draw_to_origin(px, sy, lx, py, 0, 0, get_canvas_width() - int(self.x), self.y)

    def update(self):
        if self.l == True:
            self.x = (self.x + self.speed) % get_canvas_width()
        if self.r == True:
            self.x = (self.x - self.speed) % get_canvas_width()

        if self.x < 0 :
            self.x = 0

    def handle_events(self, e):
        if (e.key, e.type) == (SDLK_LEFT, SDL_KEYDOWN):
            self.l = True
        if (e.key, e.type) == (SDLK_RIGHT, SDL_KEYDOWN):
            self.r = True
        if (e.key, e.type) == (SDLK_LEFT, SDL_KEYUP):
            self.l = False
        if (e.key, e.type) == (SDLK_RIGHT, SDL_KEYUP):
            self.r = False

class Parallex:
    def __init__(self):
        self.pp = [Parallex_Pics(1), Parallex_Pics(2), Parallex_Pics(3)]
    def draw(self):
        for p in self.pp:
            p.draw()
    def update(self):
        for p in self.pp:
            p.update()
    def handle_events(self, e):
        for p in self.pp:
            p.handle_events(e)


class Infinite:
    Image = None

    def __init__(self):

        if Infinite.Image == None:
            Infinite.Image = load_image('../Pics/Infinite_billiard.png')

        self.l, self.r, self.u, self.d = False, False, False, False
        self.x, self.y = 0, 0
        self.w, self.h = get_canvas_width(), get_canvas_height()
        self.ix, self.iy = Infinite.Image.w * 2, Infinite.Image.h * 2
        self.ratiox, self.ratioy = Infinite.Image.w / get_canvas_width(), Infinite.Image.h / get_canvas_height()

    def draw(self):

        self.rx = int(self.px * self.ratiox)
        self.ry = int(self.py * self.ratioy)
        self.rw = int(self.ratiox*self.w - self.rx)
        self.rh = int(self.ratioy*self.h - self.ry)

        Infinite.Image.clip_draw_to_origin(0, 0, self.rx, self.ry, self.w - self.px, self.h - self.py, self.px, self.py)
        Infinite.Image.clip_draw_to_origin(self.rx, 0, self.rw, self.ry, 0, self.h - self.py, self.w - self.px, self.py)
        Infinite.Image.clip_draw_to_origin(0, self.ry, self.rx, self.rh, self.w - self.px, 0, self.px, self.h - self.py)
        Infinite.Image.clip_draw_to_origin(self.rx, self.ry, self.rw, self.rh, 0, 0, self.w - self.px, self.h - self.py)

    def update(self):

        if self.l == True:
            self.x -= 5
        if self.r == True:
            self.x += 5
        if self.u == True:
            self.y += 5
        if self.d == True:
            self.y -= 5

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

        self.px = self.x % self.w
        self.py = self.y % self.h

    def handle_events(self, e):
        if (e.key, e.type) == (SDLK_LEFT, SDL_KEYDOWN):
            self.l = True
        if (e.key, e.type) == (SDLK_RIGHT, SDL_KEYDOWN):
            self.r = True
        if (e.key, e.type) == (SDLK_UP, SDL_KEYDOWN):
            self.u = True
        if (e.key, e.type) == (SDLK_DOWN, SDL_KEYDOWN):
            self.d = True
        if (e.key, e.type) == (SDLK_LEFT, SDL_KEYUP):
            self.l = False
        if (e.key, e.type) == (SDLK_RIGHT, SDL_KEYUP):
            self.r = False
        if (e.key, e.type) == (SDLK_UP, SDL_KEYUP):
            self.u = False
        if (e.key, e.type) == (SDLK_DOWN, SDL_KEYUP):
            self.d = False

class Tile:
    Image = None
    Min_height, Max_height = None, None
    Min_width, Max_width = None, None
    def __init__(self):
        if Tile.Image is None:
            Tile.Image = load_image('../Pics/tile_map.png')
        if Tile.Min_height is None:
            Tile.Min_height, Tile.Max_height = 0, get_canvas_height()*2 - (get_canvas_height()*2 % 30)
            Tile.Min_width, Tile.Max_width = 0, get_canvas_width()*2 - (get_canvas_width()*2 % 30)
        self.l, self.r, self.u, self.d = False, False, False, False
        self.x, self.y = 0, 0
        self.default_map_ipos = 102
        f = open('tile.json', 'r')
        dict = json.load(f)
        f.close()
        self.data = dict["layers"][0]["data"]
        self.ipos = dict["layers"][0]["pos"]
    def draw(self):
        print(self.x, self.y)
        sx, sy = self.x//30, self.y//30
        start_point_x = -int(self.x % 30)
        start_point_y = -int(self.y % 30)

        numx, numy = sx, sy
        dix = self.default_map_ipos//100
        diy = self.default_map_ipos % 100
        rx, ry = 0, 0

        while numy < Tile.Max_height//30:
            while numx < Tile.Max_width//30:
                Tile.Image.clip_draw_to_origin(2 + dix*30, 2 + diy*30, 30, 30, rx*30 + start_point_x, ry*30 + start_point_y, 40, 40)
                for i in range(len(self.data)):
                    if self.ipos[i]//100 == numx and self.ipos[i]%100 == numy:
                        Tile.Image.clip_draw_to_origin(2 + self.data[i]//100*30, 2 + self.data[i]%100*30, 30 , 30, rx*30 + start_point_x, ry*30 + start_point_y, 40, 40)
                numx += 1
                rx += 1
            numy += 1
            ry += 1
            rx = 0
            numx = sx


        #print(self.default_map_ipos//100, self.default_map_ipos%100)
    def update(self):
        if self.l == True:
            self.x -= 10
        if self.r == True:
            self.x += 10
        if self.u == True:
            self.y += 10
        if self.d == True:
            self.y -= 10

        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        if self.x > Tile.Max_width - get_canvas_width(): self.x = Tile.Max_width - get_canvas_width()
        if self.y > Tile.Max_height - get_canvas_height(): self.y = Tile.Max_height - get_canvas_height()
    def handle_events(self, e):
        if (e.key, e.type) == (SDLK_LEFT, SDL_KEYDOWN):
            self.l = True
        if (e.key, e.type) == (SDLK_RIGHT, SDL_KEYDOWN):
            self.r = True
        if (e.key, e.type) == (SDLK_UP, SDL_KEYDOWN):
            self.u = True
        if (e.key, e.type) == (SDLK_DOWN, SDL_KEYDOWN):
            self.d = True
        if (e.key, e.type) == (SDLK_LEFT, SDL_KEYUP):
            self.l = False
        if (e.key, e.type) == (SDLK_RIGHT, SDL_KEYUP):
            self.r = False
        if (e.key, e.type) == (SDLK_UP, SDL_KEYUP):
            self.u = False
        if (e.key, e.type) == (SDLK_DOWN, SDL_KEYUP):
            self.d = False
