from pico2d import *
import game_framework
import json
from collections import OrderedDict
import play_state
import menu_state

class score:
    alphabet = None
    number = None
    table = None
    alphabet_table = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,\
        'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15,\
        'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25
    }
    def __init__(self, order_num = 0):
        self.name = 'empty'
        self.new_record = False
        self.score = 0
        self.kills = 0
        self.x, self.y = 400, (5 - order_num) * 120
        if score.alphabet == None:
            score.alphabet = load_image('../Pics/alphabet.png')
        if score.table == None:
            score.table = load_image('../Pics/score_status.png')
        if score.number == None:
            score.number = load_image('../Pics/nums_opposite.png')

    def draw(self):
        score.table.clip_draw(0, 60, 400, 60, self.x, self.y - 60, 800, 120)
        self.draw_name()
        self.draw_score()
        self.draw_kills()
    def draw_name(self):
        for i in range(len(self.name)):
            score.alphabet.clip_draw(score.alphabet_table[self.name[i]]*25, 0, 24, 25, self.x +(i - len(self.name)/2 )*25, self.y - 30)
    def draw_score(self):
        num = 10
        o_score = self.score
        for i in range(self.len(self.score)):
            draw_num = o_score % num
            score.number.clip_draw(0, (9 - draw_num) * 50, 50, 50, self.x + (self.len(self.score)/2 - i - 1) * 25, self.y - 30 - 30, 25, 25)
            o_score //= num
    def draw_kills(self):
        num = 10
        o_kill = self.kills
        for i in range(self.len(self.kills)):
            draw_num = o_kill % num
            score.number.clip_draw(0, (9 - draw_num) * 50, 50, 50, self.x + (self.len(self.kills) / 2 - i - 1) * 25,
                                   self.y - 30 - 30 - 30, 25, 25)
            o_kill //= num
    def len(self, n):
        o_score = n
        length = 1
        num = 10
        while o_score // num != 0:
            num *= 10
            length += 1
        return length

def rearrange_list(left, right):
    global s_data, s_list

    i , j , pivot = left, right - 1, right

    if left < right:
        while i < j:
            if s_list[i].score >= s_list[pivot].score:
                i += 1
            elif s_list[j].score <= s_list[pivot].score:
                j -= 1
            else:
                swap_score(s_list[i], s_list[j])
                i += 1

        if s_list[pivot].score > s_list[i].score:
            swap_score(s_list[i], s_list[pivot])
            pivot = i
        else:
            swap_score(s_list[i + 1], s_list[pivot])
            pivot = i + 1

        rearrange_list(left, pivot - 1)
        rearrange_list(pivot, right)

def swap_score(dst, src):
    tmp = score()
    init_score(tmp, dst)
    init_score(dst, src)
    init_score(src, tmp)
    del tmp

def init_score(dst, src):
    dst.score = src.score
    dst.kills = src.kills

def store_data():
    global s_data, cur_score

    s_data = OrderedDict()
    s_data = cur_score

    with open('score_table.json', 'w') as f:
        json.dump(s_data, f, ensure_ascii=False, indent="\t")


def enter():
    global s_data, s_file, s_list
    global cur_score

    s_data = {}
    s_file = open('score_table.json', 'r')
    cur_score = json.load(s_file)
    s_file.close()

    s_list = []

    print(cur_score)

    num = 0
    for l in cur_score['player']:
        s = score(num)
        s.name = l['name']
        s.score = l['score']
        s.kills = l['kills']
        s.time = l['time']
        s_list += [s]
        num += 1

    for i in s_list:
        print(i.score)

    rearrange_list(0, len(s_list) - 1)

    for i in s_list:
        print(i.score)

def exit():
    global s_data, s_file, s_list
    global cur_score



    s_file.close()
    del s_list
    del s_data

def draw():
    global s_list

    clear_canvas()

    for l in s_list:
        l.draw()

    update_canvas()

def handle_events():
    pass

def update():
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