import time
import random
import hero
import enemy
import rectangle
from pico2d import *

name_table = {
    1: 'pill',
    2: 'skull',
    3: 'depress'
}

class item:
    image = []
    ascend_max = 20
    ascend_min = -20
    def __init__(self, num):
        self.init_table = {
            1: self.init_pill,
            2: self.init_skull,
            3: self.init_depress
        }
        #self.name = name_table[num]
        self.kind = num
        self.x, self.y = random.randint(0 + 100, 800 - 100), 250
        self.recovery_ratio = 0.4
        self.shake_max = random.randint(10, 20)
        self.shake_min = -random.randint(10, 20)
        self.shake_deg = 0
        self.shake_right = True
        self.up = True
        self.v_deg = 0
        self.a = 0
        self.hit_box = self.init_box()

        self.del_sign = False

        if len(item.image) is 0:
            item.image += [load_image('../Pics/hp_recovery.png')]
            item.image += [load_image('../Pics/enhance_hero.png')]
            item.image += [load_image('../Pics/weakening_enemy.png')]

    def draw(self):
        item.image[self.kind - 1].clip_composite_draw(0, 0, 100, 100, self.shake_deg, '', self.x, self.y + self.v_deg, 40, 40)

    def update(self, h, e):
        if self.shake_right is True:
            self.shake_deg += 1*math.pi/180
            #print(self.shake_deg, self.shake_max*math.pi/180, self.shake_deg > self.shake_max*math.pi/180)
            if self.shake_deg >= self.shake_max*math.pi/180:
                self.shake_right = False
                self.shake_max = random.randint(10, 20)
        else:
            self.shake_deg -= 1*math.pi/180
            #print(self.shake_deg, self.shake_min*math.pi/180, self.shake_deg < self.shake_min*math.pi/180)
            if self.shake_deg <= self.shake_min*math.pi/180:
                self.shake_right = True
                self.shake_min = -random.randint(10, 20)

        if self.up is True:
            self.v_deg += 2 + self.a
            if self.v_deg > 0:
                self.a -= 0.2
            else:
                self.a += 0.2
            if self.v_deg >= self.ascend_max:
                self.up = False
                self.a = 0
        else:
            self.v_deg -= 2 + self.a
            if self.v_deg < 0:
                self.a -= 0.2
            else:
                self.a += 0.2
            self.a -= 0.3
            if self.v_deg <= self.ascend_min:
                self.up = True
                self.a = 0

        self.init_box()
        self.check_body_with_hero(h, e)

    def init_box(self):
        self.init_table[self.kind]()
    def init_pill(self):
        self.hit_box = rectangle.rectangle(self.x, self.y, 20 / 5, 35 / 5)
    def init_skull(self):
        self.hit_box = rectangle.rectangle(self.x, self.y, 30 / 5, 40 / 5)
    def init_depress(self):
        self.hit_box = rectangle.rectangle(self.x, self.y, 40 / 5, 45 / 5)
    def check_body_with_hero(self, h, e):
        affect_table = {
            1: self.give_hill,
            2: self.give_enhance,
            3: self.give_depress_e
        }
        if self.hit_box.check_collide(h.body_box):
            affect_table[self.kind](h, e)
            self.del_sign = True
    def give_hill(self, h, e):
        h.hp = min(hero.hero.max_hp, h.hp + hero.hero.max_hp*self.recovery_ratio)
    def give_enhance(self, h, e):
        h.damage *= 2
        h.extra_hit_size_x += 10
        h.extra_hit_size_y += 10
        #화면 반전
    def give_depress_e(self, h, e):
        h.ate_depress = True
        if len(e) is not 0:
            for ene in e:
                ene.depress = True
                ene.depress_obj = [enemy.depress(self.x, self.y, 25, 10), enemy.depress(self.x, self.y, 10, 20),
                                     enemy.depress(self.x, self.y, -20, 10)]
                ene.damage = 0

