import time
import random
import enemy
import rectangle
import play_state
from pico2d import *

class hero:
    h_image = None
    attack_image = None
    hp_image = None
    blur_image = None
    #상수 정의
    h_stand = 0
    h_move = 25
    h_jump = 75
    h_attack = [100, 125]
    h_maxheight = 400
    h_minheight = 250
    def __init__(self, px=400, py=250, pstate=h_stand, curhp=100, jmp=False, ascnd=False, attck_effect=False,\
                 attck_type=random.randint(0,1), attck_frame=0, gol=False, gor=False, look=False):
        self.x, self.y = px, py
        self.frame = 0
        self.state = pstate
        self.damage = 5
        self.hp = curhp
        self.overwhelming = False #무적
        self.del_time = 0
        #점프 관련 변수
        self.jump = jmp
        self.ascend = ascnd
        #공격 관련 변수
        self.attack_effect = attck_effect
        self.attack_type = attck_type
        self.attack_frame = attck_frame
        self.attack_num = 0
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
        if hero.h_image is None:
            hero.h_image = load_image('../Pics/hero.png')
        if hero.attack_image is None:
            hero.attack_image = load_image('../Pics/attack_effect.png')
        if hero.hp_image is None:
            hero.hp_image = load_image('../Pics/hp_bar.png')
        if hero.blur_image is None:
            hero.blur_image = load_image('../Pics/for_blur.png')

    def draw(self):
        states = {
            hero.h_stand: self.draw_stand,
            hero.h_attack[0]: self.draw_attack,
            hero.h_attack[1]: self.draw_attack,
            hero.h_jump: self.draw_jump,
            hero.h_move: self.draw_stand
        }

        states[self.state]()

        if self.overwhelming is False:
            hero.hp_image.clip_draw(int(125 * (1 - self.hp / 100)), 0, 125 - int(125 * (1 - self.hp / 100)), 9,\
                                    self.x - int(125 * (1 - self.hp / 100)) / 2, self.y + 50,\
                                    100 - int(125 * (1 - self.hp / 100)) * 0.8, 20)
            draw_rectangle(*self.get_bb('body'))
            #draw_rectangle(*self.get_bb('attack1'))
            #draw_rectangle(*self.get_bb('attack2'))
        else:
            elapsed_time = time.time()
            if elapsed_time - self.del_time > 0.3:
                self.del_sign = True


    def draw_stand(self):

        if self.overwhelming is False:
            if self.look is False:
                hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, 50, 50)
            else:
                hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, 50, 50)

            self.frame = (self.frame + 1) % 7
        else:
            if self.look is False:
                hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state*2 + 10, 30, 30, 0, '', self.x, self.y, 60, 60)
            else:
                hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state*2 + 10, 30, 30, 0, 'h', self.x, self.y, 60, 60)
    def draw_attack(self):

        if clamp(0, self.frame, 2):
            if self.look is False:
                hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state*2 + 10, 30, 30, 0, '', self.x, self.y, 60, 60)
            else:
                hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state*2 + 10, 30, 30, 0, 'h', self.x, self.y, 60, 60)
        else:
            if self.look is False:
                hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, 50, 50)
            else:
                hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, 50, 50)

        if self.overwhelming is False:
            self.frame = (self.frame + 1) % 7

        if self.look is False:
            hero.attack_image.clip_composite_draw(self.frame * 50, self.attack_type * 50, 50, 50, 0, '', self.x + 25, self.y - 12, 75, 75)
        else:
            hero.attack_image.clip_composite_draw(self.frame * 50, self.attack_type * 50, 50, 50, 0, 'h', self.x - 25, self.y - 12, 75, 75)

        if self.attack_effect is True:
            self.attack_frame = (self.attack_frame + 1) % 4
            if self.attack_frame is 0:
                self.attack_effect = False
        if self.jump is True and self.overwhelming is False:
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
        if self.overwhelming is False:
            if self.look is False:
                hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, '', self.x, self.y, 50, 50)
            else:
                hero.h_image.clip_composite_draw(self.frame * 25, self.state, 25, 25, 0, 'h', self.x, self.y, 50, 50)

            if self.ascend is True:
                self.frame = (self.frame + 1) % 7
            else:
                self.frame = 6
        else:
            if self.look is False:
                hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state*2 + 10, 30, 30, 0, '', self.x, self.y, 60, 60)
            else:
                hero.blur_image.clip_composite_draw(self.frame * 50 + 10, self.state*2 + 10, 30, 30, 0, 'h', self.x, self.y, 60, 60)

    def update(self, E):
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
            if self.dashing is False and self.jump is True:
                self.y = hero.h_maxheight
            self.ascend = False

        if self.overwhelming is False:
            self.init_hit_boxes()
            self.update_dash()
        score = self.check_hit_attack_with_object(E)
        self.check_hit_attack_with_enemy(E)
        return score
    def init_hit_boxes(self):
        if self.look is False:
            self.body_box = rectangle.rectangle(self.x, self.y - 10, 14, 10)
            self.common_attack_box1 = rectangle.rectangle(self.x + 25, self.y, 25, 20)
            self.common_attack_box2 = rectangle.rectangle(self.x + 10, self.y - 25, 10, 10)
        else:
            self.body_box = rectangle.rectangle(self.x, self.y - 10, 14, 10)
            self.common_attack_box1 = rectangle.rectangle(self.x - 25, self.y, 25, 20)
            self.common_attack_box2 = rectangle.rectangle(self.x - 10, self.y - 25, 10, 10)
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
                                if obj.level is 1:
                                    obj.del_sign = True
                                    score += 10
                                else:
                                    obj.level -= 1
                                    score += 50
                                obj.attack_num = (self.attack_num+1)%10
                            elif self.common_attack_box2.check_collide(obj.body_box):
                                if obj.level is 1:
                                    obj.del_sign = True
                                    score += 10
                                else:
                                    obj.level -= 1
                                    score += 50
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
                if self.common_attack_box1.check_collide(ene.head_box):
                    ene.change_state(enemy.enemy.state_hit)
                elif self.common_attack_box1.check_collide(ene.body_box):
                    ene.change_state(enemy.enemy.state_hit)
                elif self.common_attack_box1.check_collide(ene.legs_box):
                    ene.change_state(enemy.enemy.state_hit)
                elif self.common_attack_box2.check_collide(ene.head_box):
                    ene.change_state(enemy.enemy.state_hit)
                elif self.common_attack_box2.check_collide(ene.body_box):
                    ene.change_state(enemy.enemy.state_hit)
                elif self.common_attack_box2.check_collide(ene.legs_box):
                    ene.change_state(enemy.enemy.state_hit)
    def time_set(self):
        pass
    def update_dash(self):
        if self.dashing is False:
            return
        if self.jump is False:
            self.dash_dist = 0
            return
        print(self.dash_dir & 10)
        if self.dash_dir & 1 == 1:
            self.y += self.dash_dist
        if self.dash_dir & 10 == 10 or self.dash_dir & 10 == 2 :
            self.y = max(self.y - self.dash_dist, 250)
        if self.dash_dir & 100 == 100:
            self.x -= self.dash_dist
        if self.dash_dir & 1000 == 1000 or self.dash_dir & 1000 == 992:
            self.x += self.dash_dist

        if self.dash_dist is not 0:
            self.dash_dist = max(self.dash_dist - 10, 0)