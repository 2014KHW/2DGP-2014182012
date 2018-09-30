import game_framework
import boys_state
from pico2d import *

def handle_events():
    eve = get_events()
    for e in eve:
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                print('I\'m called title')
                game_framework.quit()
            if e.key == SDLK_SPACE:
                game_framework.push_state(boys_state)

def enter():
    global title
    title = load_image('../Pics/title.png')

def draw():
    global title
    clear_canvas()
    title.draw(400, 300)
    update_canvas()

def update():
    pass

def exit():
    pass

def pause():
    pass

def resume():
    pass