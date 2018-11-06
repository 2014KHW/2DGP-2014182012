from pico2d import *
import game_framework
import json
import time
from collections import OrderedDict
import play_state
import menu_state

none_decided = False

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
        self.decided = False
        self.new = False
        self.no_written = True
        self.order = order_num
        self.x, self.y = 400, (5 - self.order) * 120
        if score.alphabet == None:
            score.alphabet = load_image('../Pics/alphabet.png')
        if score.table == None:
            score.table = load_image('../Pics/score_status.png')
        if score.number == None:
            score.number = load_image('../Pics/nums_opposite.png')

    def draw(self):
        if self.new is True:
            score.table.clip_draw(0, 0, 400, 60, self.x, self.y - 60, 800, 120)
        else:
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
    def set_order(self, num):
        self.order = num;
        self.y = (5 - self.order) * 120
    def put(self, char):
        if len(self.name) > 10:
            return
        if self.no_written == True:
            self.name = char
            self.no_written = False
        else:
            self.name = self.name + char

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

def swap_score(dst, src, sort = True):
    tmp = score()
    init_score(tmp, dst, sort)
    init_score(dst, src, sort)
    init_score(src, tmp, sort)
    del tmp

def init_score(dst, src, sort = True):
    dst.score = src.score
    dst.kills = src.kills
    dst.name = src.name
    dst.new = src.new
    if sort is True:
        dst.order = src.order
        dst.set_order(dst.order)
    dst.no_written = src.no_written

def get_new():
    global s_list
    for i in range(len(s_list)):
        if s_list[i].new is True:
            return s_list[i]

def store_data():
    global s_data, cur_score

    update_score_list()

    s_data = OrderedDict()
    s_data = cur_score

    with open('score_table.json', 'w') as f:
        json.dump(s_data, f, ensure_ascii=False, indent="\t")

def update_score_list():
    global cur_score, s_list

    for i in range(len(s_list)):
        cur_score['player'][i]['name'] = s_list[i].name
        cur_score['player'][i]['score'] = s_list[i].score
        cur_score['player'][i]['kills'] = s_list[i].kills

def enter():
    global s_data, s_file, s_list
    global cur_score
    global recent_score

    s_data = {}
    s_file = open('score_table.json', 'r')
    cur_score = json.load(s_file)

    recent_score = score()
    recent_score.new = True
    recent_score.score = play_state.total_score
    recent_score.kills = play_state.total_kills
    recent_score.name = "new"

    s_file.close()

    s_list = []

    print(cur_score)

    num = 0
    for l in cur_score['player']:
        s = score(num)
        s.name = l['name']
        s.score = l['score']
        s.kills = l['kills']
        s.no_written = False
        s.new = False
        s_list += [s]
        num += 1

    rearrange_list(0, len(s_list) - 1)

    compare_and_put_score()

def compare_and_put_score():
    global recent_score, s_list

    for i in range(len(s_list)):
        if recent_score.score >= s_list[i].score:
            print(recent_score.score, s_list[i].score)
            move_list(i)
            return

def move_list(num):
    global s_list, recent_score

    i = num
    #3부터 들어가지않고 무조건 0이됨
    while i < len(s_list):
        print(i)
        swap_score(recent_score, s_list[i], False)
        i += 1

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
    global decide_time
    eve = get_events()
    for e in eve:
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_RETURN):
            decide_name()
            decide_time = time.time()
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_BACKSPACE):
            n = get_new()
            n.name = n.name[0 : len(n.name) - 1]
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(menu_state)
        elif e.type == SDL_QUIT:
            store_data()
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            n = get_new()
            if n is None:
                return
            if e.key == SDLK_a:
                n.put('a')
            elif e.key == SDLK_b:
                n.put('b')
            elif e.key == SDLK_c:
                n.put('c')
            elif e.key == SDLK_d:
                n.put('d')
            elif e.key == SDLK_e:
                n.put('e')
            elif e.key == SDLK_f:
                n.put('f')
            elif e.key == SDLK_g:
                n.put('g')
            elif e.key == SDLK_h:
                n.put('h')
            elif e.key == SDLK_i:
                n.put('i')
            elif e.key == SDLK_j:
                n.put('j')
            elif e.key == SDLK_k:
                n.put('k')
            elif e.key == SDLK_l:
                n.put('l')
            elif e.key == SDLK_m:
                n.put('m')
            elif e.key == SDLK_n:
                n.put('n')
            elif e.key == SDLK_o:
                n.put('o')
            elif e.key == SDLK_p:
                n.put('p')
            elif e.key == SDLK_q:
                n.put('q')
            elif e.key == SDLK_r:
                n.put('r')
            elif e.key == SDLK_s:
                n.put('s')
            elif e.key == SDLK_t:
                n.put('t')
            elif e.key == SDLK_u:
                n.put('u')
            elif e.key == SDLK_v:
                n.put('v')
            elif e.key == SDLK_w:
                n.put('w')
            elif e.key == SDLK_x:
                n.put('x')
            elif e.key == SDLK_y:
                n.put('y')
            elif e.key == SDLK_z:
                n.put('z')

def decide_name():
    global none_decided

    n = get_new()
    if n == None:
        none_decided = True
        return
    if n.decided == True:
        return
    n.decided = True

def update():
    global decide_time
    global none_decided

    n = get_new()
    if n == None:
        if none_decided is False:
            pass
        elif time.time() - decide_time > 0.5:
            store_data()
            game_framework.change_state(menu_state)
    elif n.decided == True and decide_time is not 0:
        print('in')
        if time.time() - decide_time > 0.5:
            store_data()
            game_framework.change_state(menu_state)

    delay(0.03)

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    import sys
    current_module = sys.modules[__name__]
    open_canvas()
    play_state.total_score = 12300
    play_state.total_kills = 310
    game_framework.run(current_module)
    close_canvas()