import time
import random
import enemy
import rectangle
import play_state
from pico2d import *

tmp_score = 0

class hero:
    sound_attack = None
    h_image = None
    h_size = 75
    hp_pos = 75
    attack_image = None
    hp_image = None
    blur_image = None
    hit_image = None
    Rh_image = None
    Rattack_image = None
    Rhp_image = None
    Rblur_image = None
    Rhit_image = None
    #상수 정의
    h_stand = 0
    h_move = 25
    h_jump_ready = 50
    h_jump = 75
    h_attack_size = 100
    h_attack = [100, 125]
    h_minheight = 250
    max_hp = 100
    h_item_exist_time = 5
    h_opposite_time = 5
    def __init__(self, px=400, py=225 + h_size//2, pstate=h_stand, curhp=100, jmp=False, ascnd=True, attck_effect=False,\
                 attck_type=random.randint(0,1), attck_frame=0, gol=False, gor=False, look=False,
                 size_attack_x=0, size_attack_y=0, eat=False, mh=0, cht=0, chp=False):
        self.x, self.y = px, py
        self.frame = 0
        self.state = pstate
        self.damage = 5
        self.extra_damage = 0
        self.hp = curhp
        self.overwhelming = False #무적
        self.del_time = 0
        self.ate_depress = eat
        self.ate_begin_time = 0
        #점프 관련 변수
        self.jump = jmp
        self.maxheight = mh
        self.quake_body = 0
        self.quake_right = False
        self.ascend = ascnd
        self.jump_ready_time = 0
        self.stand_begin_time = time.time()
        self.va_speed = 0
        self.va_a = 0
        #공격 관련 변수
        self.attack_effect = attck_effect
        self.attack_type = attck_type
        self.attack_frame = attck_frame
        self.attack_num = 0
        self.extra_hit_size_x, self.extra_hit_size_y = size_attack_x, size_attack_y
        self.extra_hit_time = cht
        self.change_pics = chp
        #이동 관련 변수
        self.go_L = gol
        self.go_R = gor
        self.look = look
        self.dashing = False
        self.dash_dist = 0
        self.dash_dir = 0
        self.del_sign = False
        #히트박스
        self.body_box = rectangle.rectangle(self.x, self.y-10, 14, 10)
        self.common_attack_box1 = rectangle.rectangle(self.x + 17, self.y - 11, 17, 33)
        self.common_attack_box2 = rectangle.rectangle(self.x + 4, self.y - 19, 35, 19)
        self.hit = []
        if hero.h_image is None:
            hero.h_image = load_image('../Pics/hero.png')
            hero.Rh_image = load_image('../R_Pics/hero.png')
        if hero.attack_image is None:
            hero.attack_image = load_image('../Pics/attack_effect.png')
            hero.Rattack_image = load_image('../R_Pics/attack_effect.png')
        if hero.hp_image is None:
            hero.hp_image = load_image('../Pics/hp_bar.png')
            hero.Rhp_image = load_image('../R_Pics/hp_bar.png')
        if hero.blur_image is None:
            hero.blur_image = load_image('../Pics/for_blur.png')
            hero.Rblur_image = load_image('../R_Pics/for_blur.png')
        if hero.hit_image is None:
            hero.hit_image = load_image('../Pics/hero_hit.png')
            hero.Rhit_image = load_image('../R_Pics/hero_hit.png')
        if hero.sound_attack is None:
            hero.sound_attack = load_music('../sounds/sword_swing_short.mp3')
            hero.sound_attack.set_volume(50)

    def draw(self):
        states = {
            hero.h_stand: self.draw_stand,
            hero.h_attack[0]: self.draw_attack,
            hero.h_attack[1]: self.draw_attack,
            hero.h_jump_ready: self.draw_jump_ready,
            hero.h_jump: self.draw_jump,
            hero.h_move: self.draw_stand,
        }
        states[self.state]()

        if len(self.hit) is not 0:
            for h in range(len(self.hit)):
                self.hit[h].draw()

        if self.overwhelming is False:
            if self.change_pics is False:
                hero.hp_image.clip_draw(int(125 * (1 - self.hp / hero.max_hp)), 0,
                                        125 - int(125 * (1 - self.hp / hero.max_hp)), 9, \
                                        self.x - int(125 * (1 - self.hp / hero.max_hp)) / 2, self.y + hero.hp_pos, \
                                        100 - int(125 * (1 - self.hp / hero.max_hp)) * 0.8, 20)
            else:
                hero.Rhp_image.clip_draw(int(125 * (1 - self.hp / hero.max_hp)), 0,
                                        125 - int(125 * (1 - self.hp / hero.max_hp)), 9, \
                                        self.x - int(125 * (1 - self.hp / hero.max_hp)) / 2, self.y + hero.hp_pos, \
                                        100 - int(125 * (1 - self.hp / hero.max_hp)) * 0.8, 20)
            draw_rectangle(*self.get_bb('body'))
            #draw_rectangle(*self.get_bb('attack1'))
            #draw_rectangle(*self.get_bb('attack2'))
        else:
            elapsed_time = time.time()
            if elapsed_time - self.del_time > 0.3:
                self.del_sign = True


    def draw_stand(self):

        if self.change_pics is False:
            if self.overwhelming is False:
                if self.look is False:
                    hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, hero.h_size, hero.h_size)
                else:
                    hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, hero.h_size,
                                                     hero.h_size)

                self.frame = (self.frame + 1) % 7
            else:
                if self.look is False:
                    hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, '',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
                else:
                    hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, 'h',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
        else:
            if self.overwhelming is False:
                if self.look is False:
                    hero.Rh_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, hero.h_size, hero.h_size)
                else:
                    hero.Rh_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, hero.h_size,
                                                      hero.h_size)

                self.frame = (self.frame + 1) % 7
            else:
                if self.look is False:
                    hero.Rblur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, '',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
                else:
                    hero.Rblur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, 'h',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
    def draw_attack(self):

        if self.change_pics is False:
            if clamp(0, self.frame, 2):
                if self.look is False:
                    hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, '',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
                else:
                    hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, 'h',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
            else:
                if self.look is False:
                    hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, hero.h_size, hero.h_size)
                else:
                    hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, hero.h_size,
                                                     hero.h_size)

            if self.overwhelming is False:
                self.frame = (self.frame + 1) % 7

            if self.look is False:
                hero.attack_image.clip_composite_draw(self.frame * 50, self.attack_type * 50, 50, 50, 0, '',
                                                      self.x + 25, self.y - 12, hero.h_attack_size + self.extra_hit_size_x,
                                                      hero.h_attack_size + self.extra_hit_size_y)
            else:
                hero.attack_image.clip_composite_draw(self.frame * 50, self.attack_type * 50, 50, 50, 0, 'h',
                                                      self.x - 25, self.y - 12, hero.h_attack_size + self.extra_hit_size_x,
                                                      hero.h_attack_size + self.extra_hit_size_y)
        else:
            if clamp(0, self.frame, 2):
                if self.look is False:
                    hero.Rblur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, '',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
                else:
                    hero.Rblur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, 'h',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
            else:
                if self.look is False:
                    hero.Rh_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, hero.h_size, hero.h_size)
                else:
                    hero.Rh_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, hero.h_size,
                                                      hero.h_size)

            if self.overwhelming is False:
                self.frame = (self.frame + 1) % 7

            if self.look is False:
                hero.Rattack_image.clip_composite_draw(self.frame * 50, self.attack_type * 50, 50, 50, 0, '',
                                                      self.x + 25, self.y - 12, 75 + self.extra_hit_size_x,
                                                      75 + self.extra_hit_size_y)
            else:
                hero.Rattack_image.clip_composite_draw(self.frame * 50, self.attack_type * 50, 50, 50, 0, 'h',
                                                      self.x - 25, self.y - 12, hero.h_attack_size + self.extra_hit_size_x,
                                                       hero.h_attack_size + self.extra_hit_size_y)

        if self.attack_effect is True:
            self.attack_frame = (self.attack_frame + 1) % 4
            if self.attack_frame is 0:
                self.attack_effect = False

        if self.frame is 0 or self.y is 250:
            if self.jump is True:
                self.state = hero.h_jump
                if self.ascend is True:
                    self.frame = 0
                else:
                    self.frame = 6
            else:
                self.state = hero.h_stand
    def draw_jump_ready(self):
        if self.change_pics is False:
            if self.overwhelming is False:
                if self.look is False:
                    hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '',
                                                     self.x + self.quake_body, self.y, hero.h_size, hero.h_size)
                else:
                    hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h',
                                                     self.x + self.quake_body, self.y, hero.h_size, hero.h_size)

                self.frame = (self.frame + 1) % 7
            else:
                if self.look is False:
                    hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, '',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
                else:
                    hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, 'h',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
        else:
            if self.overwhelming is False:
                if self.look is False:
                    hero.Rh_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '',
                                                     self.x + self.quake_body, self.y, hero.h_size, hero.h_size)
                else:
                    hero.Rh_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h',
                                                     self.x + self.quake_body, self.y, hero.h_size, hero.h_size)

                self.frame = (self.frame + 1) % 7
            else:
                if self.look is False:
                    hero.Rblur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, '',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
                else:
                    hero.Rblur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, 'h',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
    def draw_jump(self):
        if self.change_pics is False:
            if self.overwhelming is False:
                if self.look is False:
                    hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, hero.h_size, hero.h_size)
                else:
                    hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, hero.h_size,
                                                     hero.h_size)

                if self.ascend is True:
                    self.frame = (self.frame + 1) % 7
                    if self.va_speed < self.va_a:
                        self.ascend = False
                else:
                    self.frame = 6
            else:
                if self.look is False:
                    hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, '',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
                else:
                    hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, 'h',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
        else:
            if self.overwhelming is False:
                if self.look is False:
                    hero.Rh_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, hero.h_size, hero.h_size)
                else:
                    hero.Rh_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, hero.h_size,
                                                      hero.h_size)

                if self.ascend is True:
                    self.frame = (self.frame + 1) % 7
                    if self.va_speed < self.va_a:
                        self.ascend = False
                else:
                    self.frame = 6
            else:
                if self.look is False:
                    hero.Rblur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, '',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)
                else:
                    hero.Rblur_image.clip_composite_draw(self.frame * 50 + 10, self.state * 2 + 10, 30, 30, 0, 'h',
                                                        self.x, self.y, hero.h_size * 6/5, hero.h_size * 6/5)

    def check_max_min_height(self):
        if self.y < hero.h_minheight:
            self.jump = False
            self.y = 260
            self.change_state(hero.h_stand)
            self.ascend = True
        if self.y > self.maxheight:
            if self.dashing is False and self.jump is True and self.ascend is True:
                self.y = self.maxheight
            self.ascend = False
        #print('self.y : ', self.y, 'self.ascend : ', self.ascend)
    def update(self, E):
        global enemies, tmp_score

        update = {
            hero.h_stand: self.update_stand,
            hero.h_move: self.update_move,
            hero.h_attack[0]: self.update_attack,
            hero.h_attack[1]: self.update_attack,
            hero.h_jump_ready: self.update_jump_ready,
            hero.h_jump: self.update_jump
        }
        enemies = E

        if self.ate_depress is True and self.ate_begin_time is 0:
            self.ate_begin_time = time.time()
        elif self.ate_depress is False:
            self.ate_begin_time = 0
            if len(E) is not 0:
                for e in E:
                    e.depress = False

        if self.ate_depress is True and time.time() - self.ate_begin_time > hero.h_item_exist_time:
            self.ate_depress = False
        if self.extra_hit_time is not 0 and time.time() - self.extra_hit_time > hero.h_opposite_time:
            self.extra_hit_size_x, self.extra_hit_size_y = 0, 0
            self.extra_hit_time = 0
            self.change_pics = False

        update[self.state]()

        if self.overwhelming is False:
            self.update_dash()
            self.init_hit_boxes()

            if len(self.hit) is not 0:
                for h in range(len(self.hit)):
                    if self.hit[h - 1].del_sign is True:
                        self.hit.pop(h - 1)
                        break
                    self.hit[h - 1].update(self)

        return tmp_score
    def update_stand(self):
        global va_speed_size
        if self.go_R is True:
            self.change_state(hero.h_move)
        if self.go_L is True:
            self.change_state(hero.h_move)
        if time.time() - self.stand_begin_time > 5:
            va_speed_size = 0.5
            self.va_a = 5
            self.va_speed = 15
            self.maxheight = 400
            self.change_state(hero.h_jump)
    def update_move(self):
        self.move_lr()
    def update_attack(self):
        global enemies, tmp_score
        tmp_score = self.check_hit_attack_with_object(enemies)
        if self.dashing is True:
            self.change_state(hero.h_jump)
            return tmp_score

        self.move_ud()
        self.move_lr()
        self.check_hit_attack_with_enemy(enemies)
        return tmp_score
    def update_jump_ready(self):
        if self.quake_body > 0:
            self.quake_body -= 1
            self.quake_body =- self.quake_body
        elif self.quake_body < 0:
            self.quake_body = -self.quake_body
        self.maxheight = min(self.maxheight + 10, get_canvas_height() - hero.h_size//2)
        self.va_speed  = min(self.va_speed + self.va_speed*0.1, 30)
    def update_jump(self):
        self.move_ud(False)
        self.move_lr()
        self.check_max_min_height()

    def move_lr(self):
        if self.go_R is True:
            self.x = min(self.x + 5, get_canvas_width() - hero.h_size//2)
            self.look = False
        if self.go_L is True:
            self.x = max(self.x - 5, 0 + hero.h_size // 2)
            self.look = True
    def move_ud(self, No_gravity=True):
        if No_gravity:
            global va_speed_size
            if self.ascend is True:
                self.y += 2
            else:
                self.y -= 2
        else:
            if self.ascend is True:
                self.y += self.va_speed - self.va_a
                self.va_a += va_speed_size

            if self.ascend is False:
                self.y -= self.va_speed - self.va_a
                self.va_a -= va_speed_size
        self.check_max_min_height()

    def change_state(self, state):
        enter = {
            hero.h_move: self.enter_move,
            hero.h_stand: self.enter_stand,
            hero.h_attack[0]: self.enter_attack,
            hero.h_attack[1]: self.enter_attack,
            hero.h_jump_ready: self.enter_jump_ready,
            hero.h_jump: self.enter_jump
        }
        exit =  {
            hero.h_move: self.exit_move,
            hero.h_stand: self.exit_stand,
            hero.h_attack[0]: self.exit_attack,
            hero.h_attack[1]: self.exit_attack,
            hero.h_jump_ready: self.exit_jump_ready,
            hero.h_jump: self.exit_jump
        }


        exit[self.state]()
        self.state = state
        enter[state]()
    def enter_move(self):
        self.frame = 0
    def enter_stand(self):
        self.frame = 0
        self.stand_begin_time = time.time()
    def enter_attack(self):
        self.dashing = False
        self.frame = 0
    def enter_jump_ready(self):
        self.frame = 0
        self.va_speed = 5
        self.va_a = 0
        self.quake_body = 10
        self.maxheight = 250 + 50
    def enter_jump(self):
        self.jump_ready_time = 0
        self.ascend = True
        self.jump = True
        self.frame = 0
    def exit_move(self):
        pass
    def exit_stand(self):
        pass
    def exit_attack(self):
        pass
    def exit_jump_ready(self):
        global va_speed_size

        va_speed_size = self.va_speed ** 2 / self.maxheight

    def exit_jump(self):
        global va_speed_size
        va_speed_size = 0

    def init_hit_boxes(self):
        if self.look is False:
            self.body_box = rectangle.rectangle(self.x, self.y - 10, 14, 10)
            self.common_attack_box1 = rectangle.rectangle(self.x + hero.h_size//2, self.y, hero.h_size//2 + self.extra_hit_size_x//2, hero.h_size*4//5 + self.extra_hit_size_y//2)
            self.common_attack_box2 = rectangle.rectangle(self.x + hero.h_size*2//5, self.y - hero.h_size//2, hero.h_size*2//5 + self.extra_hit_size_x//2, hero.h_size*2//5 + self.extra_hit_size_y//2)
        else:
            self.body_box = rectangle.rectangle(self.x, self.y - 10, 14, 10)
            self.common_attack_box1 = rectangle.rectangle(self.x - hero.h_size//2, self.y, hero.h_size//2 + self.extra_hit_size_x//2, hero.h_size*4//5 + self.extra_hit_size_y//2)
            self.common_attack_box2 = rectangle.rectangle(self.x - hero.h_size*2//5, self.y - hero.h_size//2, hero.h_size*2//5 + self.extra_hit_size_x//2, hero.h_size*2//5 + self.extra_hit_size_y//2)
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
    def check_hit_attack_with_object(self, E):
        score = 0
        if self.state is hero.h_attack[self.attack_type]:
            if len(E) is not 0:
                for ene in E:
                    if len(ene.attack_object) is not 0:
                        for obj in ene.attack_object:
                            if obj.attack_num is self.attack_num: continue
                            elif obj.attack_num is (self.attack_num + 1) % 10: continue
                            elif obj.attack_num is (self.attack_num + 2) % 10: continue
                            if self.common_attack_box1.check_collide(obj.body_box):
                                if obj.life is 1:
                                    obj.del_sign = True
                                    score += 10
                                else:
                                    obj.life -= 1
                                    score += 10
                                obj.attack_num = (self.attack_num+1)%10
                            elif self.common_attack_box2.check_collide(obj.body_box):
                                if obj.life is 1:
                                    obj.del_sign = True
                                    score += 10
                                else:
                                    obj.life -= 1
                                    score += 10
                                obj.attack_num = (self.attack_num+1)%10
                        for num in range(len(ene.attack_object) - 1):
                            if ene.attack_object[num].del_sign is True:
                                ene.attack_object.pop(num)
        return score

    def check_hit_attack_with_enemy(self, E):
        if self.state is not self.h_attack[self.attack_type]:
            return
        if len(E) is not 0:
            for ene in E:
                if ene.state is enemy.enemy.state_appear:
                    continue
                if ene.hit_num is self.attack_num:
                    continue
                if ene.del_sign is True:
                    continue
                if self.common_attack_box1.check_collide(ene.head_box):
                    ene.change_state(enemy.enemy.state_hit)
                    self.give_damage(ene)
                elif self.common_attack_box1.check_collide(ene.body_box):
                    ene.change_state(enemy.enemy.state_hit)
                    self.give_damage(ene)
                elif self.common_attack_box1.check_collide(ene.legs_box):
                    ene.change_state(enemy.enemy.state_hit)
                    self.give_damage(ene)
                elif self.common_attack_box2.check_collide(ene.head_box):
                    ene.change_state(enemy.enemy.state_hit)
                    self.give_damage(ene)
                elif self.common_attack_box2.check_collide(ene.body_box):
                    ene.change_state(enemy.enemy.state_hit)
                    self.give_damage(ene)
                elif self.common_attack_box2.check_collide(ene.legs_box):
                    ene.change_state(enemy.enemy.state_hit)
                    self.give_damage(ene)

    def give_damage(self, e):
        e.hp -= self.damage + self.extra_damage
        if e.hp < 0:
            e.change_state(enemy.enemy.state_die[e.lev - 1])

    def time_set(self):
        pass
    def update_dash(self):
        if self.dashing is False:
            return
        self.ascend = False
        if self.jump is False or self.dash_dist is 0:
            self.dash_dist = 0
            self.dashing = False
            return
        if self.dash_dir & 1 == 1:
            self.y = min(self.y + self.dash_dist, get_canvas_height() - hero.h_size//2)
        if self.dash_dir & 10 == 10 or self.dash_dir & 10 == 2:
            self.y = max(self.y - self.dash_dist, 250)
        if self.dash_dir & 100 == 100:
            self.x = max(0 + 25, self.x - self.dash_dist)
        if self.dash_dir & 1000 == 1000 or self.dash_dir & 1000 == 992:
            self.x = min(self.x + self.dash_dist, 800 - 25)

        if self.dash_dist > 0:
            self.dash_dist = max(self.dash_dist - 10, 0)

class hit:
    hit_over_time = 2
    def __init__(self, deg, h, rev):
        self.deg = deg + 3.14
        self.rad = math.pi * (deg + 180) / 180
        self.x = h.x + 5 * math.cos(self.rad)
        self.y = h.y + 5 * math.sin(self.rad)
        self.hit_frame = 0
        self.hit_begin_time = time.time()
        self.del_sign = False
        self.change_pics = rev
    def draw(self):
        if self.del_sign is True:
            return
        if self.change_pics is False:
            hero.hit_image.clip_composite_draw(self.hit_frame * 50, 0, 50, 50, \
                                               self.deg, '', \
                                               self.x + 10 * math.cos(self.deg), self.y + 10 * math.sin(self.deg), 40, 40)
        else:
            hero.Rhit_image.clip_composite_draw(self.hit_frame * 50, 0, 50, 50, \
                                               self.deg, '', \
                                               self.x + 10 * math.cos(self.deg), self.y + 10 * math.sin(self.deg), 40, 40)
    def update(self, h):
        self.change_pics = h.change_pics
        self.x = h.x + 30 * math.cos(self.deg)
        self.y = h.y + 30 * math.sin(self.deg)
        if self.del_sign is True:
            return
        self.hit_frame = (self.hit_frame + 1) % 4
        if time.time() - self.hit_begin_time > hit.hit_over_time:
            self.del_sign = True