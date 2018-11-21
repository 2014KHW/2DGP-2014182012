from pico2d import *

class Thunder:
    image = None
    def __init__(self, x):
        if Thunder.image is None:
            Thunder.image = load_image('../Pics/thunder_drop.png')
        self.x = x
        self.drop_times = 10
        self.frame = 0
        self.w = Thunder.image.w
        self.h = Thunder.image.h
    def draw(self):
        Thunder.image.clip_draw(self.frame * 50, 0, 50, 200, self.x, 250 + self.h//2, 100, get_canvas_height() - 250)
    def update(self):
        self.frame = (self.frame + 1) % 8

class Barrier:
    pass

class Allkill:
    pass