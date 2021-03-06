import time
import random
import rectangle
import play_state
import hero
import math
from pico2d import *

class enemy:
    image = []
    sound = []
    hit_effect = None
    depress_effect = None
    Rimage = []
    Rhit_effect = None
    Rdepress_effect = None
    #기타 상수
    max_hp = 10
    size = 75
    #상태 상수 정의 부분
    state_appear = 10
    state_stand = 0
    state_move = 25
    state_attack = 50
    state_attack_ready = 5050
    state_hit = 75
    state_die = [100, 125, 100]
    #시간 상수 정의 부분
    attack_ready_time = 1
    hit_recovery_time = 1.5
    def __init__(self, dst_hero, last_hero):
        self.x, self.y = random.randint(0+50, 800-50), 400
        self.draw_scale_x, self.draw_scale_y = enemy.size, enemy.size + 150
        self.frame = 0
        self.hit_frame = 0
        self.lev = random.randint(1, 3)
        self.damage = 5 * self.lev
        self.hp = enemy.max_hp * self.lev
        #상태 관련 변수
        self.state = enemy.state_appear
        self.do_not_change_frame = False
        self.do_not_change_hit_frame = False
        self.state_begin_stand_time = 0
        self.state_changed_time = 0
        self.state_elapsed_time = 0
        self.time_storage = 0
        self.from_attack = False
        self.look = False
        self.del_sign = False
        self.depress = True
        self.change_pics = False
        #약화 상태 변수
        self.depress_obj = []
        #공격 관련 변수
        self.attack_time = random.uniform(0.1, 2)
        self.attack_object = []
        self.dst_attack = dst_hero
        self.last_dst_attack = last_hero
        #이동 관련 변수
        self.move_time = random.uniform(0.1, 0.5)
        self.stand_time = random.uniform(1, 2)
        self.go_R = False
        self.go_L = False
        self.speed = random.randint(5, 10)
        self.max_speed = self.speed
        #히트박스
        self.head_box = rectangle.rectangle(self.x, self.y + 4, 16, 16)
        self.body_box = rectangle.rectangle(self.x, self.y - 10, 10, 4)
        self.legs_box = rectangle.rectangle(self.x, self.y - 20, 2, 4)
        self.hit_num = -1
        self.skill_hit_num = -1
        self.knock_back_range = 5
        if len(enemy.image) is 0:
            enemy.image += [load_image('../Pics/enemy_level1.png')]
            enemy.image += [load_image('../Pics/enemy_level2.png')]
            enemy.image += [load_image('../Pics/enemy_level3.png')]
            enemy.Rimage += [load_image('../R_Pics/enemy_level1.png')]
            enemy.Rimage += [load_image('../R_Pics/enemy_level2.png')]
            enemy.Rimage += [load_image('../R_Pics/enemy_level3.png')]
        if len(enemy.sound) is 0:
            enemy.sound += [load_music('../sounds/level1_dead.mp3')]
            enemy.sound += [load_music('../sounds/level2_dead.mp3')]
            enemy.sound += [load_music('../sounds/level3_dead.mp3')]
        if enemy.hit_effect is None:
            enemy.hit_effect = load_image('../Pics/hit_effect.png')
            enemy.Rhit_effect = load_image('../R_Pics/hit_effect.png')
        if enemy.depress_effect is None:
            enemy.depress_effect = load_image('../Pics/weak_icon.png')
            enemy.Rdepress_effect = load_image('../R_Pics/weak_icon.png')
    def change_looking(self):
        if self.state is enemy.state_hit:
            return
        if self.x >= self.dst_attack.x:
            self.look = False
        else:
            self.look = True
    def change_state(self, state):
        if self.state == enemy.state_appear:
            return
        enter = {
            enemy.state_hit: self.enter_hit,
            enemy.state_move: self.enter_move,
            enemy.state_stand: self.enter_stand,
            enemy.state_attack_ready: self.enter_attack_ready,
            enemy.state_attack: self.enter_attack,
            enemy.state_die[self.lev - 1]: self.enter_die
        }
        exit = {
            enemy.state_hit: self.exit_hit,
            enemy.state_move: self.exit_move,
            enemy.state_stand: self.exit_stand,
            enemy.state_attack_ready: self.exit_attack_ready,
            enemy.state_attack: self.exit_attack,
            enemy.state_die[self.lev - 1]: self.exit_die
        }

        exit[self.state]()
        self.state = state
        enter[state]()

    def enter_stand(self):
        self.state = enemy.state_stand
        self.go_R = False
        self.go_L = False
        self.frame = 0
        self.state_changed_time = time.time()
        if self.from_attack is False:
            self.state_begin_stand_time = time.time()
        self.from_attack = False
    def enter_move(self):
        self.state = enemy.state_move
        self.frame = 0
        if random.randint(0, 1):
            self.go_L = True
            self.go_R = False
        else:
            self.go_L = False
            self.go_R = True
        self.state_changed_time = time.time()
    def enter_attack_ready(self):
        self.state = enemy.state_attack_ready
        self.state_changed_time = time.time()
        self.frame = 0
        self.do_not_change_frame = True
    def enter_attack(self):
        self.state_changed_time = time.time()
    def enter_hit(self):
        self.state_changed_time = time.time()
        self.state = enemy.state_hit
        self.knock_back_range = 5
        self.frame, self.hit_frame = 0, 0
        self.do_not_change_hit_frame = False
        self.do_not_change_frame = False
        self.hit_num = (self.last_dst_attack.attack_num + 1) % 10
    def enter_die(self):
        self.frame = 0
        self.del_sign = True
    def exit_stand(self):
        self.from_attack = False
    def exit_move(self):
        self.from_attack = False
    def exit_attack_ready(self):
        self.do_not_change_frame = False
    def exit_attack(self):
        self.from_attack = True
    def exit_hit(self):
        self.from_attack = False
    def exit_die(self):
        self.from_attack = False
    def draw(self, gy):
        if self.state is enemy.state_appear:
            enemy.appear(self, gy)
            return

        if len(self.depress_obj) is not 0:
            for d in self.depress_obj:
                d.draw(self.look)

        if self.change_pics is False:
            if self.look is True:
                enemy.image[self.lev - 1].clip_draw(self.frame * 25, self.state % 5000, 25, 25, self.x, self.y,
                                                    self.draw_scale_x, self.draw_scale_y)
            else:
                enemy.image[self.lev - 1].clip_composite_draw(self.frame * 25, self.state % 5000, 25, 25, 0, 'h',
                                                              self.x, self.y, self.draw_scale_x, self.draw_scale_y)
        else:
            if self.look is True:
                enemy.Rimage[self.lev - 1].clip_draw(self.frame * 25, self.state % 5000, 25, 25, self.x, self.y,
                                                    self.draw_scale_x, self.draw_scale_y)
            else:
                enemy.Rimage[self.lev - 1].clip_composite_draw(self.frame * 25, self.state % 5000, 25, 25, 0, 'h',
                                                              self.x, self.y, self.draw_scale_x, self.draw_scale_y)

        if self.do_not_change_frame is False:
            self.frame = (self.frame + 1) % 7

        self.draw_hit_effect()

    def update_hitbox(self):
        self.head_box = rectangle.rectangle(self.x, self.y + 4, 16, 16)
        self.body_box = rectangle.rectangle(self.x, self.y - 10, 10, 4)
        self.legs_box = rectangle.rectangle(self.x, self.y - 20, 2, 4)
    def appear(self, gy):
        if self.change_pics is False:
            enemy.image[self.lev - 1].clip_draw(self.frame * 25, 0, 25, 25, self.x, self.y, self.draw_scale_x,
                                                self.draw_scale_y)
        else:
            enemy.Rimage[self.lev - 1].clip_draw(self.frame * 25, 0, 25, 25, self.x, self.y, self.draw_scale_x,
                                                self.draw_scale_y)
        self.y -= 20
        self.draw_scale_y -= 20

        self.update_hitbox()

        if self.draw_scale_y <= self.draw_scale_x:
            self.draw_scale_y = self.draw_scale_x
        if self.y < gy:
            self.y = gy
            self.draw_scale_y = self.draw_scale_x
            self.state = enemy.state_stand
            self.state_changed_time = time.time()
            self.state_begin_stand_time = time.time()

    def draw_hit_effect(self):
        if self.state is enemy.state_hit:
            if self.change_pics is False:
                enemy.hit_effect.clip_draw(self.hit_frame * 50, 0, 50, 50, self.x, self.y, enemy.size * 3//2, enemy.size * 3//2)
            else:
                enemy.Rhit_effect.clip_draw(self.hit_frame * 50, 0, 50, 50, self.x, self.y, enemy.size * 3//2, enemy.size * 3//2)
            if self.do_not_change_hit_frame is False:
                self.hit_frame = (self.hit_frame + 1) % 4
            if self.hit_frame is 3:
                self.do_not_change_hit_frame = True

    def update(self, cur_state, last_hero):
        global stage_state
        stage_state = cur_state
        update = {
            enemy.state_hit: self.update_hit,
            enemy.state_move: self.update_move,
            enemy.state_stand: self.update_stand,
            enemy.state_attack_ready: self.update_attack_ready,
            enemy.state_attack: self.update_attack,
            enemy.state_die[self.lev - 1]: self.update_die
        }
        self.change_pics = last_hero.change_pics
        if self.depress is False:
            self.depress_obj = []
            self.damage = 5 * self.lev

        if len(self.depress_obj) is not 0:
            for d in self.depress_obj:
                d.update(self)

        self.state_elapsed_time = time.time()
        if self.state is not enemy.state_appear:
            update[self.state]()

        for num in range(len(self.attack_object) - 1):
            if self.attack_object[num].del_sign is True:
                self.attack_object.pop(num)

        if self.del_sign is True:
            return

        for ao in range(len(self.attack_object)):
            self.attack_object[ao - 1].last_dst_attack = last_hero

        self.update_hitbox()
        self.change_looking()

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
        if self.dst_attack.x > self.x:
            self.x = max(0, self.x - self.knock_back_range)
        else:
            self.x = min(self.x + self.knock_back_range, 800)
        self.knock_back_range -= 1

    def update_move(self):
        #print(self.go_L, self.go_R)
        if self.go_R is True:
            self.x = min(830, self.x + self.speed)
            if self.x is 830:
                self.go_R = False
                self.go_L = True
        if self.go_L is True:
            self.x = max(-30, self.x - self.speed)
            if self.x is -30:
                self.go_L = False
                self.go_R = True
        if self.state_elapsed_time - self.state_changed_time >= self.move_time:
            self.change_state(enemy.state_stand)
    def update_stand(self):
        global stage_state
        if self.state_elapsed_time - self.state_changed_time >= self.attack_time and stage_state is play_state.stage_start:
            self.change_state(enemy.state_attack_ready)
        if self.state_elapsed_time - self.state_begin_stand_time >= self.stand_time:
            self.change_state(enemy.state_move)
    def update_attack_ready(self):
        global stage_state
        if stage_state is play_state.stage_pass:
            self.change_state(enemy.state_stand)
            return
        if self.state_elapsed_time - self.state_changed_time >= self.attack_ready_time:
            self.change_state(enemy.state_attack)
    def update_attack(self):
        global stage_state
        if stage_state is play_state.stage_pass:
            self.change_state(enemy.state_stand)
            return
        if self.frame is 6:
            self.attack_object += [arrow(self.x, self.y, self.lev, self.dst_attack, self.last_dst_attack, self.change_pics)]
            self.change_state(enemy.state_stand)

    def update_die(self):
        if self.frame is 6 and self.do_not_change_frame is False:
            self.do_not_change_frame = True
            self.state_changed_time = time.time()
            return

        if self.do_not_change_frame is True:
            self.state_elapsed_time = time.time()

    def time_set(self):
        time_storage = self.state_elapsed_time - self.state_changed_time
        self.state_elapsed_time = time.time()
        self.state_changed_time = self.state_elapsed_time - time_storage
        time_storage = self.state_elapsed_time - self.state_begin_stand_time
        self.state_elapsed_time = time.time()
        self.state_begin_stand_time = self.state_elapsed_time - time_storage

class arrow:
    image = []
    Rimage = []
    def __init__(self, og_x, og_y, lev, dst_hero, last_dst_hero, cp):
        self.x, self.y = og_x, og_y
        self.level = lev
        self.life = lev
        self.speed = 10
        self.frame = 0
        self.attack_num = -1
        self.dst_attack = dst_hero
        self.last_dst_attack = last_dst_hero
        if self.dst_attack.x < self.x:
            self.opposite = True
        else:
            self.opposite = False

        self.del_sign = False
        self.dif_x = self.dst_attack.x - self.x
        self.dif_y = self.dst_attack.y - self.y
        self.dist = math.sqrt(self.dif_x**2 + self.dif_y**2)
        self.degree = math.atan2(self.dif_y, self.dif_x)
        self.hit_box = rectangle.rectangle(self.x, self.y, 19*3/2, 10*3/2)
        self.change_pics = cp

        if len(arrow.image) is 0:
            arrow.image += [load_image('../Pics/enemy1_attack.png')]
            arrow.image += [load_image('../Pics/enemy2_attack.png')]
            arrow.image += [load_image('../Pics/enemy3_attack.png')]
            arrow.Rimage += [load_image('../R_Pics/enemy1_attack.png')]
            arrow.Rimage += [load_image('../R_Pics/enemy2_attack.png')]
    def draw(self):
        if self.level != 3:
            if self.change_pics is False:
                arrow.image[self.level - 1].clip_composite_draw(0, 0, 50, 50, self.degree, '', self.x, self.y, 50, 50)
            else:
                arrow.Rimage[self.level - 1].clip_composite_draw(0, 0, 50, 50, self.degree, '', self.x, self.y, 50, 50)
        else:
            arrow.image[2].clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y, 50, 50)
        draw_rectangle(self.x - 19, self.y - 10, self.x + 19, self.y + 10)

    def update(self, e):
        if self.dist == 0:
            self.check_hit_attack_with_hero(e)
            return
        self.frame = (self.frame + 1) % 5
        self.x += self.dif_x * self.speed/self.dist
        self.y += self.dif_y * self.speed/self.dist
        self.hit_box = rectangle.rectangle(self.x, self.y, 19*3/2, 10*3/2)
        self.body_box = rectangle.rectangle(self.x, self.y, 50*3/2, 50*3/2)
        if self.x > 800 - 25 or self.x < 0 + 25 : self.del_sign = True
        if self.y > 600 - 25 or self.y < e.y - 25 : self.del_sign = True

        self.check_hit_attack_with_hero(e)

    def check_hit_attack_with_hero(self, e):
        if self.del_sign is True:
            return
        if self.last_dst_attack.state is hero.hero.h_stand:
            return
        if self.last_dst_attack.state is hero.hero.h_move:
            return
        if self.last_dst_attack.state is hero.hero.h_jump_ready:
            return
        if self.hit_box.check_collide(self.last_dst_attack.body_box):
            self.last_dst_attack.hp -= e.damage
            self.last_dst_attack.hit += [hero.hit(self.degree, self.last_dst_attack, self.change_pics)]
            self.del_sign = True

class depress:
    def __init__(self, x, y, dir_x, dir_y, rev):
        self.x, self.y = x, y
        self.gap_e_x, self.gap_e_y = dir_x, dir_y
        self.deg = random.randint(0, 359)
        self.change_pics = rev
    def draw(self, look):
        if self.change_pics is False:
            if look is True:
                enemy.depress_effect.clip_composite_draw(0, 0, 50, 50, self.deg, '', self.x + self.gap_e_x,
                                                         self.y + self.gap_e_y, 50, 50)
            else:
                enemy.depress_effect.clip_composite_draw(0, 0, 50, 50, self.deg, '', self.x - self.gap_e_x,
                                                         self.y + self.gap_e_y, 50, 50)
        else:
            if look is True:
                enemy.Rdepress_effect.clip_composite_draw(0, 0, 50, 50, self.deg, '', self.x + self.gap_e_x,
                                                         self.y + self.gap_e_y, 50, 50)
            else:
                enemy.Rdepress_effect.clip_composite_draw(0, 0, 50, 50, self.deg, '', self.x - self.gap_e_x,
                                                         self.y + self.gap_e_y, 50, 50)
    def update(self, e):
        self.change_pics = e.change_pics
        self.deg = (self.deg + 1) % 360
        self.x, self.y = e.x, e.y