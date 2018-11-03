from pico2d import *
import game_framework
import json
import play_state
import menu_state

class score:
    def __init__(self):
        self.name = 'empty'
        self.score = 0
        self.kills = 0
        self.time = 0

def enter():
    global s_data, s_file, s_list
    global cur_score

    s_data = []
    s_file = open('score_table.json')
    cur_score = json.load(s_file)

    s_list = []

    print(cur_score)

    for l in cur_score['player']:
        s = score()
        s.name = l['name']
        s.score = l['score']
        s.kills = l['kills']
        s.time = l['time']
        s_list += [s]



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