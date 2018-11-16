from pico2d import *

SIW, SIH = 1022, 616
GIW, GIH = 1000, 200
SKYW, SKYH = 5000, 1000
GRNDW, GRNDH = 2500, 500

bgt = {
            1: SKYW, 2: SKYH,
            3: GRNDW, 4: GRNDH
        }

class fixed_bg:
    def __init__(self, d, img):
        self.image = img
        self.IW, self.IH = self.image.w, self.image.h
        self.divide_y = d
        #self.ix, self.iy = (self.IW - get_canvas_width()) // 4, (self.IH - get_canvas_height()) // 4
        self.wx, self.hy = self.IW*get_canvas_width()//bgt[self.divide_y], self.IH*get_canvas_height()//bgt[self.divide_y+1]
    def draw(self, x, y):
        if self.divide_y == 3:
            self.image.clip_draw_to_origin(self.dxmin, self.dymin, self.dxmax, self.dymax, 0,
                                           0, min(get_canvas_width(), self.xx),
                                           get_canvas_height() // self.divide_y - self.dymin)
        else:
            self.image.clip_draw_to_origin(self.dxmin, self.dymin , self.wx, self.hy, 0,
                                           0, get_canvas_width(),
                                           get_canvas_height() // self.divide_y)
    def update(self, x, y):
        self.xx = self.image.w * 2 - x
        #print('self.xx : ', self.xx, 'h.wx : ', x)
        self.dxmin, self.dymin = clamp(0, (int(x) - get_canvas_width() // 2), 600), max(0, (int(y) - get_canvas_height() // 2))
        self.dxmax, self.dymax = min(get_canvas_width()//2, self.image.w), min(get_canvas_height()//2, self.image.h)