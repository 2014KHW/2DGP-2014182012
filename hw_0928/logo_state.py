import game_framework
import title_state
from pico2d import *

clock = 0

def handle_events():
    eve = get_events()
    for e in eve:
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.quit()

def enter():
    global logo
    open_canvas()
    logo = load_image('../Pics/kpu_credit.png')

def draw():
    global logo
    clear_canvas()
    logo.draw(400, 300)
    update_canvas()

def update():
    global clock
    if clock > 1 :
        game_framework.push_state(title_state)
    delay(0.05)
    clock += 0.05

def exit():
    close_canvas()

def pause():
    pass

def resume():
    global clock
    clock = 0
    delay(0.03)
