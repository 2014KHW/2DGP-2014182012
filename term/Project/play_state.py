from pico2d import *
import game_framework
import score_state

def enter():
    pass

def draw():
    pass

def handle_events():
    pass

def update():
    pass

def exit():
    pass

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