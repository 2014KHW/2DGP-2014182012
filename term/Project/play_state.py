from pico2d import *
import game_framework
import score_state

class hero:
    image = None
    def __init__(self):
        self.x, self.y = 400, 250
        self.frame = 0
        if hero.image is None:
            hero.image = load_image('../Pics/hero.png')
    def draw(self):
        hero.image.clip_draw(self.frame * 25, 0, 25, 25, self.x, self.y, 50, 50)
        self.frame = (self.frame + 1) % 7


def enter():
    global ground, H
    ground = load_image('../Pics/ground_map.png')
    H = hero()

def exit():
    global ground, H
    del ground, H

def draw():
    global ground, H
    ground.clip_draw(300, 0, 500, 200, 400, 100, 800, 300)
    H.draw()
    update_canvas()

def handle_events():
    eve = get_events()
    for e in eve:
        if e.type is SDL_QUIT:
            game_framework.quit()

def update():
    delay(0.03)

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    import sys
    current_module = sys.modules[__name__]
    open_canvas()
    game_framework.run(current_module)
    close_canvas()