from pico2d import *
import game_framework
import score_state

def enter():
    global ground
    ground = load_image('../Pics/ground_map.png')

def exit():
    global ground
    del ground

def draw():
    global ground
    ground.clip_draw(300, 0, 500, 200, 400, 100, 800, 300)

def handle_events():
    eve = get_events()
    for e in eve:
        if e.type is SDL_QUIT:
            game_framework.quit()

def update():
    update_canvas()
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