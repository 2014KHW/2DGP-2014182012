from pico2d import *
import game_framework
import menu_state
import score_state
import random
import time
import math

#상수 선언 부분
stage_start = 10
stage_pass = 1
class rectangle:
    def __init__(self, x, y, size_x, size_y):
        self.x, self.y = x, y
        self.left, self.right, self.top, self.bottom = x-size_x, x+size_x, y+size_y, y-size_y

    def check_collide(self, rect, print_on=True):

        if self.left > rect.right:
            if print_on is True: print('none')
            return False
        if self.right < rect.left:
            if print_on is True: print('none')
            return False
        if self.top < rect.bottom:
            if print_on is True: print('none')
            return False
        if self.bottom > rect.top:
            if print_on is True: print('none')
            return False
        if print_on is True: print('hit!')
        return True

class hero:
    h_image = None
    attack_image = None
    hp_image = None
    #상수 정의
    h_stand = 0
    h_move = 25
    h_jump = 75
    h_attack = [100, 125]
    h_maxheight = 400
    h_minheight = 250
    def __init__(self):
        self.x, self.y = 400, 250
        self.frame = 0
        self.state = hero.h_stand
        self.hp = 100
        #점프 관련 변수
        self.jump = False
        self.ascend = False
        #공격 관련 변수
        self.attack_effect = False
        self.attack_type = random.randint(0, 1)
        self.attack_frame = 0
        self.attack_num = 0
        #이동 관련 변수
        self.go_L = False
        self.go_R = False
        self.look = False
        #히트박스
        self.body_box = rectangle(self.x, self.y-10, 14, 10)
        self.common_attack_box1 = rectangle(self.x + 17, self.y - 11, 17, 33)
        self.common_attack_box2 = rectangle(self.x + 4, self.y - 19, 35, 19)
        if hero.h_image is None:
            hero.h_image = load_image('../Pics/hero.png')
        if hero.attack_image is None:
            hero.attack_image = load_image('../Pics/attack_effect.png')
        if hero.hp_image is None:
            hero.hp_image = load_image('../Pics/hp_bar.png')

    def draw(self):
        states = {
            hero.h_stand: self.draw_stand,
            hero.h_attack[0]: self.draw_attack,
            hero.h_attack[1]: self.draw_attack,
            hero.h_jump: self.draw_jump,
            hero.h_move: self.draw_stand
        }
        if self.look is False:
            hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, 50, 50)
        else:
            hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, 50, 50)

        states[self.state]()

        hero.hp_image.clip_draw(int(125 * (1-self.hp/100)), 0, 125 - int(125 * (1-self.hp/100)), 9, self.x - int(125 * (1-self.hp/100))/2, self.y + 50, 50 - int(125 * (1-self.hp/100))*0.4, 10)
        draw_rectangle(*self.get_bb('body'))
        #draw_rectangle(*self.get_bb('attack1'))
        #draw_rectangle(*self.get_bb('attack2'))


    def draw_stand(self):
        self.frame = (self.frame + 1) % 7
    def draw_attack(self):
        self.frame = (self.frame + 1) % 7
        if self.look is False:
            hero.attack_image.clip_composite_draw(self.frame * 50, self.attack_type * 50, 50, 50, 0, '', self.x + 25, self.y - 12, 75, 75)
        else:
            hero.attack_image.clip_composite_draw(self.frame * 50, self.attack_type * 50, 50, 50, 0, 'h', self.x - 25, self.y - 12, 75, 75)

        if self.attack_effect is True:
            self.attack_frame = (self.attack_frame + 1) % 4
            if self.attack_frame is 0:
                self.attack_effect = False
        if self.jump is True:
            if self.ascend is True:
                self.y += 2
            else:
                self.y -= 2
        if self.frame is 0 or self.y is 250:
            if self.jump is True:
                self.state = hero.h_jump
                if self.ascend is True:
                    self.frame = 0
                else:
                    self.frame = 6
            else:
                self.state = hero.h_stand
    def draw_jump(self):
        if self.ascend is True:
            self.frame = (self.frame + 1) % 7
        else:
            self.frame = 6
    def update(self):
        global E
        if self.state is hero.h_jump:
            if self.ascend is True:
                self.y += 10
            if self.ascend is False:
                self.y -= 5
        if self.go_R is True:
            self.x += 5
            self.look = False
            if self.state is hero.h_stand:
                self.state = hero.h_move
        if self.go_L is True:
            self.x -= 5
            self.look = True
            if self.state is hero.h_stand:
                self.state = hero.h_move
        if self.y < hero.h_minheight:
            self.jump = False
            self.y = hero.h_minheight
            self.state = hero.h_stand
            self.frame = 0
            self.ascend = True
        if self.y > hero.h_maxheight:
            self.y = hero.h_maxheight
            self.ascend = False

        self.init_hit_boxes()
        self.check_hit_attack_with_object()
        self.check_hit_attack_with_enemy()
    def init_hit_boxes(self):
        if self.look is False:
            self.body_box = rectangle(self.x, self.y - 10, 14, 10)
            self.common_attack_box1 = rectangle(self.x + 25, self.y, 25, 20)
            self.common_attack_box2 = rectangle(self.x + 10, self.y - 25, 10, 10)
        else:
            self.body_box = rectangle(self.x, self.y - 10, 14, 10)
            self.common_attack_box1 = rectangle(self.x - 25, self.y, 25, 20)
            self.common_attack_box2 = rectangle(self.x - 10, self.y - 25, 10, 10)
    def get_bb(self, str):
        if str is 'body':
            return self.x - 14, self.y - 20, self.x + 14, self.y
        elif str is 'attack1':
            if self.look is False:
                return self.x, self.y - 20, self.x + 50, self.y + 20
            else:
                return self.x - 50, self.y - 20, self.x, self.y + 20
        elif str is 'attack2':
            if self.look is False:
                return self.x, self.y - 35, self.x + 20, self.y - 15
            else:
                return self.x - 20, self.y - 35, self.x, self.y + 15
    def check_hit_attack_with_object(self):
        global  E
        if self.state is hero.h_attack[self.attack_type]:
            if len(E) is not 0:
                for ene in E:
                    if len(ene.attack_object) is not 0:
                        for obj in ene.attack_object:
                            if obj.attack_num is self.attack_num: continue
                            elif obj.attack_num is (self.attack_num + 1) % 10: continue
                            elif obj.attack_num is (self.attack_num + 2) % 10: continue
                            if self.common_attack_box1.check_collide(obj.body_box):
                                if obj.level is 1:
                                    obj.del_sign = True
                                else:
                                    obj.level -= 1
                                obj.attack_num = (self.attack_num+1)%10
                            elif self.common_attack_box2.check_collide(obj.body_box):
                                if obj.level is 1:
                                    obj.del_sign = True
                                else:
                                    obj.level -= 1
                                obj.attack_num = (self.attack_num+1)%10
                        for num in range(len(ene.attack_object) - 1):
                            if ene.attack_object[num].del_sign is True:
                                ene.attack_object.pop(num)
    def check_hit_attack_with_enemy(self):
        global E
        if self.state is not self.h_attack[self.attack_type]:
            return
        if len(E) is not 0:
            for ene in E:
                if ene.state is enemy.state_appear:
                    continue
                if self.common_attack_box1.check_collide(ene.head_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                    ene.do_not_change_frame = False
                elif self.common_attack_box1.check_collide(ene.body_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                    ene.do_not_change_frame = False
                elif self.common_attack_box1.check_collide(ene.legs_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                    ene.do_not_change_frame = False
                elif self.common_attack_box2.check_collide(ene.head_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                    ene.do_not_change_frame = False
                elif self.common_attack_box2.check_collide(ene.body_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                    ene.do_not_change_frame = False
                elif self.common_attack_box2.check_collide(ene.legs_box):
                    ene.state_changed_time = time.time()
                    ene.state = enemy.state_hit
                    ene.frame, ene.hit_frame = 0, 0
                    ene.do_not_change_hit_frame = False
                    ene.do_not_change_frame = False
class enemy:
    image = []
    hit_effect = None
    #상태 상수 정의 부분
    state_appear = 10
    state_stand = 0
    state_move = 25
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
        self.lev = random.randint(1, 3)
        self.damage = 5*self.lev
        #상태 관련 변수
        self.state = enemy.state_appear
        self.do_not_change_frame = False
        self.do_not_change_hit_frame = False
        self.state_begin_stand_time = 0
        self.state_changed_time = 0
        self.state_elapsed_time = 0
        #공격 관련 변수
        self.attack_time = random.uniform(0.1, 2)
        self.attack_object = []
        #이동 관련 변수
        self.move_time = random.uniform(0.1, 0.5)
        self.stand_time = random.uniform(1, 2)
        self.go_R = False
        self.go_L = False
        self.speed = random.randint(1, 6)
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
            self.update_attack()
        self.draw_hit_effect()

    def update_hitbox(self):
        self.head_box = rectangle(self.x, self.y + 4, 16, 16)
        self.body_box = rectangle(self.x, self.y - 10, 10, 4)
        self.legs_box = rectangle(self.x, self.y - 20, 2, 4)
    def appear(self):
        enemy.image[self.lev - 1].clip_draw(self.frame * 25, 0, 25, 25, self.x, self.y, self.draw_scale_x, self.draw_scale_y)
        self.y -= 20
        self.draw_scale_y -= 20

        self.update_hitbox()

        if self.draw_scale_y <= self.draw_scale_x:
            self.draw_scale_y = self.draw_scale_x
        if self.y < 250:
            self.y = 250
            self.state = enemy.state_stand
            self.state_changed_time = time.time()
            self.state_begin_stand_time = time.time()

    def draw_hit_effect(self):
        if self.state is enemy.state_hit:
            enemy.hit_effect.clip_draw(self.hit_frame * 50, 0, 50, 50, self.x, self.y, 75, 75)
            if self.do_not_change_hit_frame is False:
                self.hit_frame = (self.hit_frame + 1) % 4
            if self.hit_frame is 3:
                self.do_not_change_hit_frame = True

    def update(self):
        states = {
            enemy.state_hit: self.update_hit,
            enemy.state_move: self.update_move,
            enemy.state_stand: self.update_stand,
            enemy.state_attack_ready: self.update_attack_ready,
            enemy.state_attack: self.update_attack
        }

        self.state_elapsed_time = time.time()
        if self.state is not enemy.state_attack and self.state is not enemy.state_appear:
            states[self.state]()

        for num in range(len(self.attack_object) - 1):
            if self.attack_object[num].del_sign is True:
                self.attack_object.pop(num)

        self.update_hitbox()

    def update_hit(self):
        if self.state_elapsed_time - self.state_changed_time >= self.hit_recovery_time:
            self.state = enemy.state_stand
            self.state_changed_time = time.time()
            self.do_not_change_hit_frame = False
            self.do_not_change_frame = False
    def update_move(self):
        if self.go_R is True:
            self.x = min(800, self.x + self.speed)
            if self.x is 800:
                self.go_R = False
                self.go_L = True
        if self.go_L is True:
            self.x = max(0, self.x - self.speed)
            if self.x is 0:
                self.go_L = False
                self.go_R = True
        if self.state_elapsed_time - self.state_changed_time >= self.move_time:
            self.state = enemy.state_stand
            self.go_R = False
            self.go_L = False
            self.frame = 0
            self.state_changed_time = time.time()
            self.state_begin_stand_time = time.time()
    def update_stand(self):
        if self.state_elapsed_time - self.state_changed_time >= self.attack_time:
            self.state = enemy.state_attack_ready
            self.state_changed_time = time.time()
            self.frame = 0
            self.do_not_change_frame = True
        if self.state_elapsed_time - self.state_begin_stand_time >= self.stand_time:
            self.state = enemy.state_move
            self.frame = 0
            if random.randint(0, 1):
                self.go_L = True
            else:
                self.go_R = True
            self.state_changed_time = time.time()
    def update_attack_ready(self):
        global stage_state
        if stage_state is stage_pass:
            self.state = enemy.state_stand
            self.do_not_change_frame = False
            return
        if self.state_elapsed_time - self.state_changed_time >= self.attack_ready_time:
            self.state = enemy.state_attack
            self.state_changed_time = time.time()
            self.do_not_change_frame = False
    def update_attack(self):
        global stage_state
        if stage_state is stage_pass:
            self.state = enemy.state_stand
            self.do_not_change_frame = False
            return
        if self.state is not enemy.state_attack:
            return
        if self.frame is 0:
            self.state = enemy.state_stand
            self.state_changed_time = time.time()
            if self.lev is not 3:
                self.attack_object += [arrow(self.x, self.y, self.lev)]

class arrow:
    image = []
    def __init__(self, og_x, og_y, lev):
        self.x, self.y = og_x, og_y
        self.level = lev
        self.speed = 5
        self.damage = self.level * 5
        self.attack_num = -1
        if H.x < self.x:
            self.opposite = True
        else:
            self.opposite = False

        self.del_sign = False
        self.dif_x = H.x - self.x
        self.dif_y = H.y - self.y
        self.dist = math.sqrt(self.dif_x**2 + self.dif_y**2)
        self.degree = math.atan2(self.dif_y, self.dif_x)
        self.hit_box = rectangle(self.x, self.y, 19, 10)

        if len(arrow.image) is 0:
            arrow.image += [load_image('../Pics/enemy1_attack.png')]
            arrow.image += [load_image('../Pics/enemy2_attack.png')]
    def draw(self):
        arrow.image[self.level - 1].clip_composite_draw(0, 0, 50, 50, self.degree, '', self.x, self.y, 50, 50)
        draw_rectangle(self.x - 19, self.y - 10, self.x + 19, self.y + 10)

    def update(self):
        self.x += self.dif_x * self.speed/self.dist
        self.y += self.dif_y * self.speed/self.dist
        self.hit_box = rectangle(self.x, self.y, 19, 10)
        self.body_box = rectangle(self.x, self.y, 50, 50)
        if self.x > 800 - 25 or self.x < 0 + 25 : self.del_sign = True
        if self.y > 600 - 25 or self.y < 250 : self.del_sign = True

        self.check_hit_attack_with_hero()

    def check_hit_attack_with_hero(self):
        global H
        if self.del_sign is True:
            return
        if self.hit_box.check_collide(H.body_box):
            H.hp -= self.damage
            self.del_sign = True

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
    global sky, ground, slot, stage_term, stamp, H, E, phase
    global stage_start_time, stage_state
    global E_appear_speed, E_appear_time_ratio
    global hit

    sky = load_image('../Pics/sky_background.png')
    ground = load_image('../Pics/ground_map.png')
    hit = load_image('../Pics/hit_effect.png')
    slot = load_image('../Pics/skill_slot.png')
    stage_term = load_image('../Pics/vacant_bar.png')
    stamp = load_image('../Pics/hero_stamp.png')

    E_appear_speed = 1.5 #몬스터 출현 속도
    E_appear_time_ratio = 10#몬스터 출현 속도 증가량
    stage_start_time = time.time() #스테이지 시작 시간
    stage_state = stage_start

    E = [enemy()]

    H = hero()

    phase = [phrase(stage_state)]

def exit():
    global ground, H, E, hit, slot, stage_term, stamp
    del ground, H, E, hit, slot, stage_term, stamp

def draw():
    global sky, ground, slot, stage_term, stamp, H, E, phase
    global stage_start_time, stage_elapsed_time
    global stage_state

    clear_canvas()

    sky.clip_draw(200, 100, 400, 450, 400, 300, 800, 600)
    ground.clip_draw(200, 0, 600, 200, 400, 100, 800, 300)
    slot.clip_draw(0, 0, 125, 125, 50, 600 - 50, 50, 50)
    stage_term.clip_draw(0, 0, 125, 9, 400, 600 - 20, 400, 10)
    stamp.clip_draw(0, 0, 19, 16, 400 - 200 * (1 - (stage_elapsed_time - stage_start_time)*2/stage_start), 600 - 20, 19, 16)


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
            if H.state is hero.h_stand or H.state is hero.h_move:
                return
            H.attack_type = random.randint(0, 1)
            H.state = hero.h_attack[H.attack_type]
            H.frame = 0
            H.attack_num = (H.attack_num + 1)%10
            print(H.attack_num)
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_a):
            H.go_L = True
            if H.state is hero.h_stand:
                H.state = hero.h_move
                H.frame = 0
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_d) :
            H.go_R = True
            if H.state is hero.h_stand:
                H.state = hero.h_move
                H.frame = 0
        if (e.type, e.key) == (SDL_KEYUP, SDLK_a):
            H.go_L = False
            if (H.go_L, H.go_R) == (False, False):
                if H.state is hero.h_move:
                    H.state = hero.h_stand
                    H.frame = 0
        if (e.type, e.key) == (SDL_KEYUP, SDLK_d) :
            H.go_R = False
            if (H.go_L, H.go_R) == (False, False):
                if H.state is hero.h_move:
                    H.state = hero.h_stand
                    H.frame = 0

def update():
    global E
    global E_appear_speed, E_appear_time_ratio, stage_start_time, stage_elapsed_time
    global stage_state, phase

    if len(E) is not 0:
        for ene in E:
            ene.update()
            if len(ene.attack_object) is not 0:
                for obj in ene.attack_object:
                    obj.update()# 적 공격 오브젝트 이동 부분

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

    if stage_state is stage_pass:
        if stage_elapsed_time - stage_start_time >= stage_pass:
            stage_start_time = time.time()
            stage_elapsed_time = time.time()
            stage_state = stage_start
            phase += [phrase(stage_start)]
            E_appear_time_ratio -= 0.1
            E_appear_speed = E_appear_time_ratio

    H.update()

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