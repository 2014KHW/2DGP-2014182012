import time
import random
import rectangle
import play_state
import hero
import math
from pico2d import *

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
        self.damage = 5 * self.lev
        self.hp = 10 * self.lev
        #상태 관련 변수
        self.state = enemy.state_appear
        self.do_not_change_frame = False
        self.do_not_change_hit_frame = False
        self.state_begin_stand_time = 0
        self.state_changed_time = 0
        self.state_elapsed_time = 0
        self.time_storage = 0
        self.look = False
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
        self.head_box = rectangle.rectangle(self.x, self.y + 4, 16, 16)
        self.body_box = rectangle.rectangle(self.x, self.y - 10, 10, 4)
        self.legs_box = rectangle.rectangle(self.x, self.y - 20, 2, 4)
        self.hit_num = -1
        self.knock_back_range = 5
        if len(enemy.image) is 0:
            enemy.image += [load_image('../Pics/enemy_level1.png')]
            enemy.image += [load_image('../Pics/enemy_level2.png')]
            enemy.image += [load_image('../Pics/enemy_level3.png')]
        if enemy.hit_effect is None:
            enemy.hit_effect = load_image('../Pics/hit_effect.png')
    def change_looking(self, H):
        if self.state is enemy.state_hit:
            return
        if self.x >= H.x:
            self.look = False
        else:
            self.look = True
    def change_state(self, state, H):
        global he
        he = H
        enter = {
            enemy.state_hit: self.enter_hit,
            enemy.state_move: self.enter_move,
            enemy.state_stand: self.enter_stand,
            enemy.state_attack_ready: self.enter_attack_ready,
            enemy.state_attack: self.enter_attack
        }
        exit =  {
            enemy.state_hit: self.exit_hit,
            enemy.state_move: self.exit_move,
            enemy.state_stand: self.exit_stand,
            enemy.state_attack_ready: self.exit_attack_ready,
            enemy.state_attack: self.exit_attack
        }

        exit[self.state]
        self.state = state
        enter[state]

    def enter_stand(self):
        pass
    def enter_move(self):
        pass
    def enter_attack_ready(self):
        pass
    def enter_attack(self):
        pass
    def enter_hit(self):
        global he
        self.state_changed_time = time.time()
        self.state = enemy.enemy.state_hit
        self.knock_back_range = 5
        self.frame, self.hit_frame = 0, 0
        self.do_not_change_hit_frame = False
        self.do_not_change_frame = False
        self.hit_num = (he.attack_num + 1) % 10

    def exit_stand(self):
        pass
    def exit_move(self):
        pass
    def exit_attack_ready(self):
        pass
    def exit_attack(self):
        pass
    def exit_hit(self):
        pass

    def draw(self):
        if self.state is enemy.state_appear:
            enemy.appear(self)
            return

        if self.look is True:
            enemy.image[self.lev - 1].clip_draw(self.frame * 25, self.state%5000, 25, 25, self.x, self.y, self.draw_scale_x, self.draw_scale_y)
        else:
            enemy.image[self.lev - 1].clip_composite_draw(self.frame * 25, self.state % 5000, 25, 25, 0, 'h', self.x, self.y, self.draw_scale_x, self.draw_scale_y)
        if self.do_not_change_frame is not True:
            self.frame = (self.frame + 1) % 7
            self.update_attack()
        self.draw_hit_effect()

    def update_hitbox(self):
        self.head_box = rectangle.rectangle(self.x, self.y + 4, 16, 16)
        self.body_box = rectangle.rectangle(self.x, self.y - 10, 10, 4)
        self.legs_box = rectangle.rectangle(self.x, self.y - 20, 2, 4)
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

    def update(self, H, cur_state):
        global stage_state, he
        he = H
        stage_state = cur_state
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
        self.change_looking(H)

    def update_hit(self):
        self.knock_back()
        if self.state_elapsed_time - self.state_changed_time >= self.hit_recovery_time:
            self.state = enemy.state_stand
            self.state_changed_time = time.time()
            self.do_not_change_hit_frame = False
            self.do_not_change_frame = False
    def knock_back(self):
        if self.knock_back_range is 0:
            return
        self.x -= self.knock_back_range
        self.knock_back_range -= 1

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
        global stage_state
        if self.state_elapsed_time - self.state_changed_time >= self.attack_time and stage_state is play_state.stage_start:
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
        if stage_state is play_state.stage_pass:
            self.state = enemy.state_stand
            self.do_not_change_frame = False
            return
        if self.state_elapsed_time - self.state_changed_time >= self.attack_ready_time:
            self.state = enemy.state_attack
            self.state_changed_time = time.time()
            self.do_not_change_frame = False
    def update_attack(self):
        global stage_state, he
        if stage_state is play_state.stage_pass:
            self.do_not_change_frame = False
            return
        if self.state is not enemy.state_attack:
            return
        if self.frame is 0:
            self.state = enemy.state_stand
            self.state_changed_time = time.time()
            if self.lev is not 3:
                self.attack_object += [arrow(self.x, self.y, self.lev, he)]
    def time_set(self):
        time_storage = self.state_elapsed_time - self.state_changed_time
        self.state_elapsed_time = time.time()
        self.state_changed_time = self.state_elapsed_time - time_storage
        time_storage = self.state_elapsed_time - self.state_begin_stand_time
        self.state_elapsed_time = time.time()
        self.state_begin_stand_time = self.state_elapsed_time - time_storage

class arrow:
    image = []
    def __init__(self, og_x, og_y, lev, H):
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
        self.hit_box = rectangle.rectangle(self.x, self.y, 19, 10)

        if len(arrow.image) is 0:
            arrow.image += [load_image('../Pics/enemy1_attack.png')]
            arrow.image += [load_image('../Pics/enemy2_attack.png')]
    def draw(self):
        arrow.image[self.level - 1].clip_composite_draw(0, 0, 50, 50, self.degree, '', self.x, self.y, 50, 50)
        draw_rectangle(self.x - 19, self.y - 10, self.x + 19, self.y + 10)

    def update(self):
        self.x += self.dif_x * self.speed/self.dist
        self.y += self.dif_y * self.speed/self.dist
        self.hit_box = rectangle.rectangle(self.x, self.y, 19, 10)
        self.body_box = rectangle.rectangle(self.x, self.y, 50, 50)
        if self.x > 800 - 25 or self.x < 0 + 25 : self.del_sign = True
        if self.y > 600 - 25 or self.y < 250 : self.del_sign = True

        self.check_hit_attack_with_hero()

    def check_hit_attack_with_hero(self):
        global he
        if self.del_sign is True:
            return
        if self.hit_box.check_collide(he.body_box):
            he.hp -= self.damage
            self.del_sign = True
