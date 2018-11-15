from pico2d import *

class fixed_bg:
    S_Image = None
    G_Image = None
    def __init__(self, s):
        if fixed_bg.S_Image == None:
            fixed_bg.S_Image = load_image('../Pics/sky_background.png')
        if fixed_bg.G_Image == None:
            fixed_bg.G_Image = load_image('../Pics/ground_map.png')
        self.select = s
        if self.select == 0:
            self.ix, self.iy = (fixed_bg.S_Image.w - get_canvas_width()) // 4, (fixed_bg.S_Image.h - get_canvas_height()) // 4
        else:
            self.ix, self.iy = (fixed_bg.G_Image.w - get_canvas_width()) // 4, (fixed_bg.G_Image.h - get_canvas_height()) // 4
        self.wx, self.hy = get_canvas_width()//2, get_canvas_height()//2
    def draw(self, x, y):
        if self.select == 0:
            fixed_bg.S_Image.clip_draw_to_origin(self.dxmin, self.dymin, self.wx, self.hy, 0, 0, get_canvas_width(), get_canvas_height())
        else:
            fixed_bg.G_Image.clip_draw_to_origin(self.dxmin, self.dymin, self.wx, self.hy, 0, 0, get_canvas_width(), get_canvas_height()//3)
    def update(self, x, y):
        self.dxmin, self.dymin = max(0, int(x) - get_canvas_width()//2), max(0, int(y) - get_canvas_height()//2)
        #self.dxmax, self.dymax = min(fixed_bg.Image.w, x + get_canvas_width()//2), min(fixed_bg.Image.h, y + get_canvas_height()//2)
        #print(self.dxmin, self.dymin)