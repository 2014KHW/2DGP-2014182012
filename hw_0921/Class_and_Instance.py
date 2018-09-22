from pico2d import *
import random

class Boy:
    def __init__(self):
        self.image = load_image('../Pics/run_animation.png')
        self.x, self.y = 0, 90
        self.frame = 0
    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
    def run(self):
        self.x+=2
        self.frame= (self.frame+1) % 8

class Grass:
    def __init__(self):
        self.image = load_image('../Pics/grass.png')
    def draw(self):
        self.image.draw(400, 30)

def handle_events():
    global running
    events = get_events()
    for eve in events:
        if eve.type == SDL_QUIT:
            running = False
        if eve.type == SDL_KEYDOWN:
            if eve.key == SDLK_ESCAPE:
                running = False

open_canvas()

running = True

boy = [Boy() for i in range(20)]
grass = Grass()

while running:
    clear_canvas()
    grass.draw()
    for i in boy:
        i.draw()
        i.run()
    handle_events()
    update_canvas()
    delay(0.03)

close_canvas()