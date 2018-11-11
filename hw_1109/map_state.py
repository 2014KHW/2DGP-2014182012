from pico2d import *
import game_framework
import game_world
from bg import Tile as b_ground

def enter():
    global bgp
    bgp = b_ground()
    game_world.add_object(bgp, 0)

def exit():
    game_world.clear()

def draw():
    clear_canvas()
    game_world.draw()
    update_canvas()

def handle_events():
    global bgp
    for e in get_events():
        if e.type == SDL_QUIT:
            game_framework.quit()
        else:
            bgp.handle_events(e)

def update():
    game_world.update()
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
