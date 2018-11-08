import time
import random
import hero
import enemy
import rectangle
from pico2d import *

class pill:
    image = None
    ascend_max = 20
    ascend_min = -20
    def __init__(self):
        self.x, self.y = random.randint(0 + 100, 800 - 100), 275
        self.recovery_ratio = 0.4
        self.shake_max = random.randint(10, 20)
        self.shake_min = -random.randint(10, 20)
        self.shake_deg = 0
        self.shake_right = True
        self.up = True
        self.v_deg = 0
        self.a = 0
        self.hit_box = rectangle.rectangle(self.x, self.y, 20, 35)

        self.del_sign = False

        if pill.image == None:
            pill.image = load_image('../Pics/hp_recovery.png')

    def draw(self):
        pill.image.clip_composite_draw(0, 0, 100, 100, self.shake_deg, '', self.x, self.y, 100, 100)

    def update(self, h):
        if self.shake_right is True:
            self.shake_deg += 1
            if self.shake_deg >= self.shake_max:
                self.shake_right = False
                self.shake_max = random.randint(10, 20)
        else:
            self.shake_deg -= 1
            if self.shake_deg <= self.shake_min:
                self.shake_right = True
                self.shake_min = -random.randint(10, 20)

        if self.up is True:
            self.v_deg += 5 + self.a
            if self.v_deg > 0:
                self.a -= 0.3
            else:
                self.a += 0.3
            if self.v_deg >= self.ascend_max:
                self.up = False
        else:
            self.v_deg -= 5 + self.a
            if self.v_deg < 0:
                self.a -= 0.3
            else:
                self.a += 0.3
            self.a -= 0.3
            if self.v_deg <= self.ascend_min:
                self.up = True

        self.init_box()
        self.check_body_with_hero(h)

    def init_box(self):
        self.hit_box = rectangle.rectangle(self.x, self.y, 20, 35)
    def check_body_with_hero(self, h):
        if self.hit_box.check_collide(h.body_box):
            self.give_hill(h)
            self.del_sign = True
    def give_hill(self, h):
        h.hp = min(hero.hero.max_hp, h.hp + hero.hero.max_hp*self.recovery_ratio)
