from pico2d import *
import game_framework
import menu_state
import score_state
import random
import time
import math
import rectangle
import hero
import enemy

total_elapse = 0
total_start = time.time()
total_score = 0

#상수 선언 부분
stage_start = 20
stage_pass = 10
stop = False

class phrase:
    image = None
    #상수 정의
    original_pos = 400
    state_stop = 100
    state_move = 10
    def __init__(self, state):
        self.x, self.y = 500, 500
        self.create_time = time.time()
        self.state = phrase.state_move
        if state is stage_start:
            phrase.image = load_image('../Pics/stage_start.png')
        if state is stage_pass:
            phrase.image = load_image('../Pics/stage_pass.png')

    def draw(self, state):
        if state is stage_start:
            phrase.image.clip_draw(0, 0, 426, 58, self.x, self.y)
        if state is stage_pass:
            phrase.image.clip_draw(0, 0, 409, 58, self.x, self.y)
        self.x -= 5
        if self.x < phrase.original_pos:
            self.x = phrase.original_pos

class shaking:
    def __init__(self):
        self.shake_strength = 3
        self.move = -1
        self.on_shaking = False
    def shake(self):
        global H, E, ground_x, ground_y

        if self.on_shaking is False:
            return
        if self.shake_strength is 0:
            self.on_shaking = False
            return

        H[-1].x += self.shake_strength * self.move
        if len(E) is not 0:
            for ene in E:
                ene.x += self.shake_strength * self.move

        ground_x += self.shake_strength * self.move
        ground_y += self.shake_strength * self.move/2

        if self.move is -1:
            self.move = 1
        else:
            self.move = -1
            self.shake_strength -= 1

    def give_shake(self):
        global H
        if self.on_shaking is False and H[-1].state is hero.hero.h_attack[H[-1].attack_type]:
            self.on_shaking = True
            self.shake_strength = 5
        else:
            return


def enter():
    global sky, ground, slot, stage_term, stamp, H, E, phase, ground_x, ground_y
    global stage_start_time, stage_state
    global E_appear_speed, E_appear_time_ratio
    global hit
    global shake

    ground_x, ground_y = 400, 100
    shake = shaking()
    sky = load_image('../Pics/sky_background.png')
    ground = load_image('../Pics/ground_map.png')
    hit = load_image('../Pics/hit_effect.png')
    slot = load_image('../Pics/skill_slot.png')
    stage_term = load_image('../Pics/vacant_bar.png')
    stamp = load_image('../Pics/hero_stamp.png')

    E_appear_speed = 2 #몬스터 출현 속도
    E_appear_time_ratio = 5#몬스터 출현 속도 증가량
    stage_start_time = time.time() #스테이지 시작 시간
    stage_state = stage_start

    E = [enemy.enemy()]

    H = [hero.hero()]

    phase = [phrase(stage_state)]

def exit():
    global ground, H, E, hit, slot, stage_term, stamp
    del ground, H, E, hit, slot, stage_term, stamp

def draw():
    global sky, ground, slot, stage_term, stamp, H, E, phase
    global ground_x, ground_y
    global stage_start_time, stage_elapsed_time
    global stage_state
    global stop

    if stop is True:
        return

    clear_canvas()

    sky.clip_draw(200, 100, 400, 450, 400, 300, 800, 600)
    ground.clip_draw(200, 0, 600, 200, ground_x, ground_y, 800, 300)
    slot.clip_draw(0, 0, 125, 125, 50, 600 - 50, 50, 50)
    stage_term.clip_draw(0, 0, 125, 9, 400, 600 - 20, 400, 10)
    if stage_state is stage_start:
        stamp.clip_draw(0, 0, 19, 16, 400 - 200 * (1 - (stage_elapsed_time - stage_start_time) * 2 / stage_start), 600 - 20, 19, 16)
    else:
        stamp.clip_draw(0, 0, 19, 16, 400 - 200 * (1 - (stage_elapsed_time - stage_start_time) * 2 / stage_pass), 600 - 20, 19, 16)


    if len(E) is not 0:
        for ene in E:
            ene.draw()
            if len(ene.attack_object) is not 0:
                for obj in ene.attack_object:
                    if obj.del_sign is False:
                        obj.draw()

    if len(phase) is not 0:
        for ph in phase:
            ph.draw(stage_state)
        if phase[-1].x is phrase.original_pos:
            phase.pop()

    if len(H) is not 0:
        for he in H:
            he.draw()

    update_canvas()

def handle_events():
    global H, stop
    eve = get_events()
    for e in eve:
        if e.type is SDL_QUIT:
            print('quit')
            game_framework.quit()
        if e.key is SDLK_w:
            if H[-1].jump is True :
                return
            H[-1].jump = True
            H[-1].state = hero.hero.h_jump
            H[-1].frame = 0
        if e.key is SDLK_j:
            if H[-1].state is hero.hero.h_stand or H[-1].state is hero.hero.h_move:
                return
            H[-1].attack_type = random.randint(0, 1)
            H[-1].state = hero.hero.h_attack[H[-1].attack_type]
            H[-1].frame = 0
            H[-1].attack_num = (H[-1].attack_num + 1)%10
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_a):
            H[-1].go_L = True
            if H[-1].state is hero.hero.h_stand:
                H[-1].state = hero.hero.h_move
                H[-1].frame = 0
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_d) :
            H[-1].go_R = True
            if H[-1].state is hero.hero.h_stand:
                H[-1].state = hero.hero.h_move
                H[-1].frame = 0
        if (e.type, e.key) == (SDL_KEYUP, SDLK_a):
            H[-1].go_L = False
            if (H[-1].go_L, H[-1].go_R) == (False, False):
                if H[-1].state is hero.hero.h_move:
                    H[-1].state = hero.hero.h_stand
                    H[-1].frame = 0
        if (e.type, e.key) == (SDL_KEYUP, SDLK_d) :
            H[-1].go_R = False
            if (H[-1].go_L, H[-1].go_R) == (False, False):
                if H[-1].state is hero.hero.h_move:
                    H[-1].state = hero.hero.h_stand
                    H[-1].frame = 0
        if (e.type, e.key) == (SDL_KEYUP, SDLK_k):
            H += [hero.hero(H[-1].x, H[-1].y, H[-1].state, H[-1].hp, H[-1].jump, H[-1].ascend, H[-1].attack_effect, \
                  H[-1].attack_type, H[-1].attack_frame, H[-1].go_L, H[-1].go_R, H[-1].look)]

        if (e.type, e.key) == (SDL_KEYUP, SDLK_p):
            if stop is True:
                stop = False
            else:
                stop = True


def update():
    global E, H
    global E_appear_speed, E_appear_time_ratio, stage_start_time, stage_elapsed_time
    global total_start, total_elapse, total_score
    global stage_state, phase
    global stage_term, stamp
    global shake
    global stop

    if stop is True:
        if len(H) is not 0:
            for he in H:
                he.time_set()
        if len(E) is not 0:
            for ene in E:
                ene.time_set()
        time_storage = stage_elapsed_time - stage_start_time
        stage_elapsed_time = time.time()
        total_start = stage_elapsed_time - total_elapse
        stage_start_time = stage_elapsed_time - time_storage
        return

    if len(E) is not 0:
        for ene in E:
            ene.update(H[0], stage_state)
            if len(ene.attack_object) is not 0:
                for obj in ene.attack_object:
                    obj.update()# 적 공격 오브젝트 이동 부분

    stage_elapsed_time = time.time()
    if stage_state is stage_start:
        if stage_elapsed_time - stage_start_time >= E_appear_speed:
            E_appear_speed += E_appear_time_ratio
            E += [enemy.enemy()]
        if stage_elapsed_time - stage_start_time >= stage_start:
            stage_start_time = time.time()
            stage_elapsed_time = time.time()
            stage_state = stage_pass
            phase += [phrase(stage_pass)]
            stage_term = load_image('../Pics/vacant_bar2.png')
            stamp = load_image('../Pics/enemy_stamp.png')

    if stage_state is stage_pass:
        if stage_elapsed_time - stage_start_time >= stage_pass:
            stage_start_time = time.time()
            stage_elapsed_time = time.time()
            stage_state = stage_start
            phase += [phrase(stage_start)]
            E_appear_time_ratio -= 0.1
            E_appear_speed = E_appear_time_ratio
            stage_term = load_image('../Pics/vacant_bar.png')
            stamp = load_image('../Pics/hero_stamp.png')


    total_elapse = stage_elapsed_time - total_start
    print(H[-1])
    total_score += H[-1].update(E)
    shake.give_shake()
    shake.shake()

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