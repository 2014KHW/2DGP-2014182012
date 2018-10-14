from pico2d import *
import game_framework
import score_state
import random
import time
import math

#상수 선언 부분
stage_start = 25
stage_pass = 1

class rectangle:
    def __init__(self, x, y, size_x, size_y):
        self.x, self.y = x, y
        self.left, self.right, self.top, self.bottom = x-size_x, x+size_x, y+size_y, y-size_y

    def check_collide(self, rect):
        if self.left >= rect.left and self.left <= rect.right:
            if self.top >= rect.bottom and self.top <= rect.top: return True
            elif self.bottom >= rect.bottom and self.bottom <= rect.top: return True
        elif self.right >= rect.left and self.right <= rect.right:
            if self.top >= rect.bottom and self.top <= rect.top: return True
            elif self.bottom >= rect.bottom and self.bottom <= rect.top: return True
        elif rect.left >= self.left and rect.left <= self.right:
            if rect.top >= self.bottom and rect.top <= self.top: return True
            elif rect.bottom >= self.bottom and rect.bottom <= self.top: return True
        elif rect.right >= self.left and rect.right <= self.right:
            if rect.top >= self.bottom and rect.top <= self.top: return True
            elif rect.bottom >= self.bottom and rect.bottom <= self.top: return True
        else: return False

class hero:
    h_image = None
    attack_image = None
    #상수 정의
    h_stand = 0
    h_jump = 75
    h_attack = [100, 125]
    h_maxheight = 400
    h_minheight = 250
    def __init__(self):
        self.x, self.y = 400, 250
        self.frame = 0
        self.state = hero.h_stand
        #점프 관련 변수
        self.jump = False
        self.ascend = False
        #공격 관련 변수
        self.attack_effect = False
        self.attack_type = random.randint(0, 1)
        self.attack_frame = 0
        #히트박스
        self.body_box = rectangle(self.x, self.y-10, 14, 10)
        self.common_attack_box1 = rectangle(self.x + 17, self.y - 11, 17, 33)
        self.common_attack_box2 = rectangle(self.x + 4, self.y - 19, 35, 19)
        if hero.h_image is None:
            hero.h_image = load_image('../Pics/hero.png')
        if hero.attack_image is None:
            hero.attack_image = load_image('../Pics/attack_effect.png')

    def draw(self):
        hero.h_image.clip_draw(self.frame * 25, self.state, 25, 25, self.x, self.y, 50, 50)
        if self.state is hero.h_stand:
            self.frame = (self.frame + 1) % 7
        if self.state is hero.h_jump:
            if self.ascend is True:
                self.frame = (self.frame + 1) % 7
            else:
                self.frame = 6
        if self.state is hero.h_attack[self.attack_type]:
            hero.attack_image.clip_draw(self.frame * 50, self.attack_type * 50, 50, 50, self.x + 25, self.y - 12, 75, 75)
            self.frame = (self.frame + 1) % 7
            if self.attack_effect is True:
                self.attack_frame = (self.frame + 1) % 4
                if self.attack_frame is 0:
                    self.attack_effect = False
            if self.frame is 0:
                if self.jump is True:
                    self.state = hero.h_jump
                    if self.ascend is True:
                        self.frame = 0
                    else:
                        self.frame = 6
                else:
                    self.state = hero.h_stand
    def act(self):
        if self.state is hero.h_jump:
            if self.ascend is True:
                self.y += 10
            if self.ascend is False:
                self.y -= 5
        self.body_box = rectangle(self.x, self.y - 5, 7, 5)
        self.common_attack_box1 = rectangle(self.x, self.y, 50, 50)
        self.common_attack_box2 = rectangle(self.x, self.y, 50, 50)

class enemy:
    image = []
    hit_effect = None
    #상태 상수 정의 부분
    state_appear = 10
    state_stand = 0
    state_attack = 50
    state_attack_ready = 5050
    state_hit = 75
    #시간 상수 정의 부분
    attack_ready_time = 1
    hit_recovery_time = 1.5
    def __init__(self):
        self.x, self.y = random.randint(0+50, 800-50), 400
        self.draw_scale_x, self.draw_scale_y = 50, 200
        self.frame = 0
        self.hit_frame = 0
        self.lev = 1
        #상태 관련 변수
        self.state = enemy.state_appear
        self.do_not_change_frame = False
        self.do_not_change_hit_frame = False
        self.state_changed_time = 0
        self.state_elapsed_time = 0
        #공격 관련 변수
        self.attack_time = random.uniform(0.1, 2)
        self.attack_object = []
        #히트박스
        self.head_box = rectangle(self.x, self.y + 4, 16, 16)
        self.body_box = rectangle(self.x, self.y - 10, 10, 4)
        self.legs_box = rectangle(self.x, self.y - 20, 2, 4)
        if len(enemy.image) is 0:
            enemy.image += [load_image('../Pics/enemy_level1.png')]
            enemy.image += [load_image('../Pics/enemy_level2.png')]
            enemy.image += [load_image('../Pics/enemy_level3.png')]
        if enemy.hit_effect is None:
            enemy.hit_effect = load_image('../Pics/hit_effect.png')
    def draw(self):
        if self.state is enemy.state_appear:
            enemy.appear(self)
            return

        enemy.image[self.lev - 1].clip_draw(self.frame * 25, self.state%5000, 25, 25, self.x, self.y, self.draw_scale_x, self.draw_scale_y)
        if self.do_not_change_frame is not True:
            self.frame = (self.frame + 1) % 7
        if self.frame is 0:
            if self.state is enemy.state_attack:
                self.state = enemy.state_stand
                self.state_changed_time = time.time()
                self.attack_object += [arrow(self.x, self.y, self.lev)]
        if self.state is enemy.state_hit:
            enemy.hit_effect.clip_draw(self.hit_frame * 50, 0, 50, 50, self.x, self.y, 75, 75)
            if self.do_not_change_hit_frame is not True:
                self.hit_frame = (self.hit_frame + 1) % 4
            if self.hit_frame is 3:
                self.do_not_change_hit_frame = True



    def appear(self):
        enemy.image[self.lev - 1].clip_draw(self.frame * 25, 0, 25, 25, self.x, self.y, self.draw_scale_x, self.draw_scale_y)
        self.y -= 20
        self.draw_scale_y -= 20
        self.head_box = rectangle(self.x, self.y + 4, 16, 16)
        self.body_box = rectangle(self.x, self.y - 10, 10, 4)
        self.legs_box = rectangle(self.x, self.y - 20, 2, 4)
        if self.draw_scale_y <= self.draw_scale_x:
            self.draw_scale_y = self.draw_scale_x
        if self.y < 250:
            self.y = 250
            self.state = enemy.state_stand
            self.state_changed_time = time.time()

class arrow:
    image = []
    def __init__(self, og_x, og_y, lev):
        self.x, self.y = og_x, og_y
        self.level = lev
        self.speed = 5
        if H.x < self.x:
            self.opposite = True
        else:
            self.opposite = False

        self.del_sign = False
        self.dif_x = H.x - self.x
        self.dif_y = H.y - self.y
        self.dist = math.sqrt(self.dif_x**2 + self.dif_y**2)
        self.degree = math.atan2(self.dif_y, self.dif_x)
        self.hit_box = rectangle(self.x, self.y, 19, 4)
        if len(arrow.image) is 0:
            arrow.image += [load_image('../Pics/enemy1_attack.png')]
            arrow.image += [load_image('../Pics/enemy2_attack.png')]
    def draw(self):
        arrow.image[self.level - 1].clip_composite_draw(0, 0, 50, 50, self.degree, '', self.x, self.y, 50, 50)

    def update(self):
        self.x += self.dif_x * self.speed/self.dist
        self.y += self.dif_y * self.speed/self.dist
        self.hit_box = rectangle(self.x, self.y, 19, 4)
        if self.x > 800 - 25 or self.x < 0 + 25 : self.del_sign = True
        if self.y > 600 - 25 or self.y < 250 : self.del_sign = True

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

def enter():
    global ground, H, E, phase
    global stage_interval, stage_start_time, stage_state
    global E_appear_speed, E_appear_time_ratio
    global hit

    ground = load_image('../Pics/ground_map.png')
    hit = load_image('../Pics/hit_effect.png')

    stage_interval = 10 #스테이지 시간간격
    E_appear_speed = 1.5 #몬스터 출현 속도
    E_appear_time_ratio = 1.5#몬스터 출현 속도 증가량
    stage_start_time = time.time() #스테이지 시작 시간
    stage_state = stage_start

    E = [enemy()]

    H = hero()

    phase = [phrase(stage_state)]

def exit():
    global ground, H, E
    del ground, H, E

def draw():
    global ground, H, E, phase
    global stage_state

    clear_canvas()

    ground.clip_draw(300, 0, 500, 200, 400, 100, 800, 300)

    if len(E) is not 0:
        for ene in E:
            ene.draw()
            if len(ene.attack_object) is not 0:
                for obj in ene.attack_object:
                    obj.draw()

    if len(phase) is not 0:
        for ph in phase:
            ph.draw(stage_state)
        if phase[-1].x is phrase.original_pos:
            phase.pop()

    H.act()
    H.draw()

    update_canvas()

def handle_events():
    global H
    eve = get_events()
    for e in eve:
        if e.type is SDL_QUIT:
            print('quit')
            game_framework.quit()
        if e.key is SDLK_w:
            if H.jump is True :
                return
            H.jump = True
            H.state = hero.h_jump
            H.frame = 0
        if e.key is SDLK_j:
            if H.state is hero.h_stand:
                return
            H.attack_type = random.randint(0, 1)
            H.state = hero.h_attack[H.attack_type]
            H.frame = 0

def update():
    global E
    global E_appear_speed, E_appear_time_ratio, stage_start_time, stage_elapsed_time
    global stage_state, phase

    if len(E) is not 0:
        for ene in E:
            if len(ene.attack_object) is not 0:
                for obj in ene.attack_object:
                    obj.update()# 적 공격 오브젝트 이동 부분
                    if obj.hit_box.check_collide(H.body_box):
                        print('hit!')
                for num in range(len(ene.attack_object) - 1):
                    if ene.attack_object[num].del_sign is True:
                        ene.attack_object.pop(num)
            if H.state is hero.h_attack[H.attack_type]: #플레이어 공격 충돌 체크
                if ene.state is enemy.state_appear:
                    break
                if H.common_attack_box1.check_collide(ene.head_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                elif H.common_attack_box1.check_collide(ene.body_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                elif H.common_attack_box1.check_collide(ene.legs_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                elif H.common_attack_box2.check_collide(ene.head_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                elif H.common_attack_box2.check_collide(ene.body_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                elif H.common_attack_box2.check_collide(ene.legs_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False

    stage_elapsed_time = time.time()
    if stage_state is stage_start:
        if stage_elapsed_time - stage_start_time >= E_appear_speed:
            E_appear_speed += E_appear_time_ratio
            E += [enemy()]
        if stage_elapsed_time - stage_start_time >= stage_start:
            stage_start_time = time.time()
            stage_elapsed_time = time.time()
            stage_state = stage_pass
            phase += [phrase(stage_pass)]
        if len(E) is not 0: #적 공격 모션으로 전환해주는 부분
            for ene in E:
                ene.state_elapsed_time = time.time()
                if ene.state is enemy.state_stand:
                    if ene.state_elapsed_time - ene.state_changed_time >= ene.attack_time:
                        ene.state = enemy.state_attack_ready
                        ene.state_changed_time = time.time()
                        ene.frame = 0
                        ene.do_not_change_frame = True
                elif ene.state is enemy.state_attack_ready:
                    if ene.state_elapsed_time - ene.state_changed_time >= ene.attack_ready_time:
                        ene.state = enemy.state_attack
                        ene.state_changed_time = time.time()
                        ene.do_not_change_frame = False
                elif ene.state is enemy.state_hit:
                    if ene.state_elapsed_time - ene.state_changed_time >= ene.hit_recovery_time:
                        ene.state = enemy.state_stand
                        ene.state_changed_time = time.time()
                        ene.do_not_change_hit_frame = False

    if stage_state is stage_pass:
        if stage_elapsed_time - stage_start_time >= stage_pass:
            stage_start_time = time.time()
            stage_elapsed_time = time.time()
            stage_state = stage_start
            phase += [phrase(stage_start)]
            E_appear_time_ratio -= 0.1
            E_appear_speed = E_appear_time_ratio

    if H.jump is True:
        if H.y < hero.h_minheight:
            H.jump = False
            H.y = hero.h_minheight
            H.state = hero.h_stand
            H.frame = 0
            H.ascend = True
        if H.y > hero.h_maxheight:
            H.y = hero.h_maxheight
            H.ascend = False

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