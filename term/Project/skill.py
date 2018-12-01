from pico2d import *
import time
import random
import hero
import enemy
import rectangle

lock = None

class Thunder:
    image = None
    slot = None
    sound = None
    reuse_time = 2
    def __init__(self, x):
        if Thunder.image is None:
            Thunder.image = load_image('../Pics/thunder_drop.png')
        if Thunder.slot is None:
            Thunder.slot = load_image('../Pics/thunder_slot.png')
        if Thunder.sound is None:
            Thunder.sound = load_music('../sounds/thunder.mp3')
            Thunder.sound.set_volume(50)
        self.locked = True
        self.activated = False
        self.x = x
        self.drop_times = 10
        self.cur_drops = 1
        self.frame = 0
        self.ft = 0
        self.w = Thunder.image.w
        self.h = Thunder.image.h
    def activate(self):
        if self.activated == True: return
        if self.locked == True: return
        if time.time() - self.ft > Thunder.reuse_time:
            self.activated = True
    def disconnect(self):
        self.activated = False
        self.cur_drops = 0
        self.ft = time.time()
    def unlock(self):
        self.locked = False
    def draw(self, s):
        if s == 0:
            Thunder.slot.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
            if self.locked == True:
                lock.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
        if self.activated == True:
            Thunder.image.clip_draw(self.frame * 25, 0, 25, 200, self.x, self.gy + (get_canvas_height() - self.gy + 120)//2, 150, get_canvas_height() - self.gy - 120)
    def update(self, h, e, g):
        self.frame = (self.frame + 1) % 8
        self.gy = g
        if self.frame == 0:
            self.x = random.randint(0 + 150, 800 - 150)
            self.cur_drops += 1
            Thunder.sound.play(1)
        if self.cur_drops > self.drop_times:
            self.disconnect()
        if self.frame > 3:
            self.damage = (h.damage + h.extra_damage) * 2
            self.hit_box = rectangle.rectangle(self.x, self.gy + (get_canvas_height() - self.gy + 120)//2, 50, (get_canvas_height() - self.gy - 120) / 2)
            self.hits(e)
    def hits(self, e):
        for ene in e:
            if ene.del_sign == True: continue
            if ene.skill_hit_num != self.cur_drops and self.hit_box.check_collide(ene.head_box):
                ene.skill_hit_num = self.cur_drops
                ene.change_state(enemy.enemy.state_hit)
                self.give_damage(ene)
            elif ene.skill_hit_num != self.cur_drops and self.hit_box.check_collide(ene.body_box):
                ene.skill_hit_num = self.cur_drops
                ene.change_state(enemy.enemy.state_hit)
                self.give_damage(ene)
            elif ene.skill_hit_num != self.cur_drops and self.hit_box.check_collide(ene.legs_box):
                ene.skill_hit_num = self.cur_drops
                ene.change_state(enemy.enemy.state_hit)
                self.give_damage(ene)
    def give_damage(self, e):
        e.hp -= self.damage
        if e.hp < 0:
            e.change_state(enemy.enemy.state_die[e.lev - 1])

    def handle_events(self):
        print('I\'m in')
        if time.time() - self.ft > Thunder.reuse_time:
            self.activate()

class Barrier:
    barrier = None
    attack = None
    slot = None
    sound = None
    lasting_time = 5
    success_reuse_time = 5
    fail_reuse_time = 3
    barrier_size = 120
    def __init__(self):
        if Barrier.barrier is None:
            Barrier.barrier = load_image('../Pics/barrier.png')
        if Barrier.attack is None:
            Barrier.attack = load_image('../Pics/counter_attack.png')
        if Barrier.slot is None:
            Barrier.slot = load_image('../Pics/counter_slot.png')
        if Barrier.sound is None:
            Barrier.sound = load_music('../sounds/flying_sword.mp3')
            Barrier.sound.set_volume(50)
        self.locked = True
        self.ft = 0 #발동이 막 끝난시간 ( 쿨타임 )
        self.st = 0 #발동을 시작한 시간 (지속시간)
        self.frame = 0
        self.w = Barrier.barrier.w
        self.h = Barrier.barrier.h

        self.activated = False
        self.waiting_kind = 'first'
        self.at = 0 #발동 후 공격 시간의 간격을 재는 변수
        self.getting_times = 0
        self.attack_add_time = 0.1
        self.attacks = []
        self.mode = 'disappear'
    def unlock(self):
        self.locked = False
    def activate(self):
        self.mode = 'ready'
        self.st = time.time()
        self.activated = True
        self.at = time.time()
        self.getting_times = 0
        self.waiting_kind = 'first'
    def disconnect(self):
        self.mode = 'disappear'
        self.ft = time.time()
        self.activated = False
    def get_attack(self):
        if self.mode != 'counter': return
        if self.waiting_kind == 'success': return
        if time.time() - self.at > self.attack_add_time:
            self.attacks += [Barrier_Attack(self.attack_deg + math.pi + random.randint(-10, 10)*math.pi/180, self.x, self.y, self.getting_times)]
            self.at = time.time()
            self.getting_times += 1
            Barrier.sound.play(1)
            if self.getting_times == 10:
                self.waiting_kind = 'success'

    def draw(self, s):
        if s == 1:
            Barrier.slot.clip_draw(0, 0, 50, 50, 75, 600 - 75, 50, 50)
            if self.locked == True:
                lock.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
        if self.mode == 'ready':
            if self.h_look == False:
                Barrier.barrier.clip_draw(self.frame * 50, 0, 50, 50, self.x + 10, self.y,
                                          Barrier.barrier_size - self.frame * 2.5, Barrier.barrier_size - self.frame * 2.5)
            else:
                Barrier.barrier.clip_composite_draw(self.frame * 50, 0, 50, 50, 0, 'h', self.x - 10, self.y,
                                          Barrier.barrier_size - self.frame * 2.5, Barrier.barrier_size - self.frame * 2.5)
        if self.mode == 'counter':
            if len(self.attacks) == 0: return
            for ats in self.attacks:
                ats.draw()
    def update_attacks(self, h, e, g):
        if len(self.attacks) == 0: return
        for ats in self.attacks:
            ats.update(h, e, g)
        for ats in range(len(self.attacks)):
            if self.attacks[ats - 1].del_sign is True: self.attacks.pop(ats - 1)
            break
    def update(self, h, e, g):
        self.frame = (self.frame + 1) % 5
        self.x, self.y = h.x, h.y
        self.h_look = h.look
        self.update_attacks(h, e, g)
        if self.mode == 'ready':
            if time.time() - self.st > Barrier.lasting_time:
                self.st = 0
                self.waiting_kind = 'fail'
                self.disconnect()
            self.hit_box = rectangle.rectangle(self.x, self.y, Barrier.barrier_size - self.frame * 2.5, Barrier.barrier_size - self.frame * 2.5)
            if self.activated:self.hits(e)
        if self.mode == 'counter':
            print('I\'m counter!')
            self.get_attack()
        if self.waiting_kind == 'success' and len(self.attacks) == 0:
            if self.mode == 'counter':self.disconnect()

    def hits(self, e):
        if len(e) == 0: return
        for ene in e:
            if len(ene.attack_object) == 0 : continue
            for ao in range(len(ene.attack_object)):
                if ene.attack_object[ao - 1].del_sign is True: continue
                if self.hit_box.check_collide(ene.attack_object[ao - 1].body_box):
                    ene.attack_object[ao - 1].del_sign = True
                    if len(self.attacks) is 0:
                        self.attack_deg = ene.attack_object[ao - 1].degree
                        self.mode = 'counter'
    def handle_events(self):
        if self.waiting_kind == 'success':
            if time.time() - self.ft > Barrier.success_reuse_time:
                self.activate()
        elif self.waiting_kind == 'fail':
            if time.time() - self.ft > Barrier.fail_reuse_time:
                self.activate()
        else:
            self.activate()

class Barrier_Attack:
    attack_size = 70
    def __init__(self, deg, hx, hy, num):
        self.speed = 15
        self.deg = deg
        self.curx, self.cury = hx, hy
        self.del_sign = False
        self.frame = 0
        self.num = num
    def draw(self):
        if self.del_sign == False:
            Barrier.attack.clip_draw(self.frame * 50, 0, 50, 50, self.curx, self.cury, Barrier_Attack.attack_size, Barrier_Attack.attack_size)
    def update(self, h, e, g):
        self.frame = (self.frame + 1) % 4
        self.curx += self.speed * math.cos(self.deg)
        self.cury += self.speed * math.sin(self.deg)
        self.damage = 3 * (h.extra_damage + 1)
        self.hit_box = rectangle.rectangle(self.curx, self.cury, Barrier_Attack.attack_size - 5, Barrier_Attack.attack_size - 5)
        if self.outs():
            print('delete pch')
            self.del_sign = True
        if len(e) == 0: return
        for ene in e:
            if ene.del_sign is True: continue
            if self.hit_box.check_collide(ene.head_box):
                ene.skill_hit_num = self.num
                ene.change_state(enemy.enemy.state_hit)
                self.give_damage(ene)
            elif self.hit_box.check_collide(ene.body_box):
                ene.skill_hit_num = self.num
                ene.change_state(enemy.enemy.state_hit)
                self.give_damage(ene)
            elif self.hit_box.check_collide(ene.legs_box):
                ene.skill_hit_num = self.num
                ene.change_state(enemy.enemy.state_hit)
                self.give_damage(ene)

    def give_damage(self, e):
        e.hp -= self.damage
        if e.hp < 0:
            e.change_state(enemy.enemy.state_die[e.lev - 1])

    def outs(self):
        if self.curx < 0 - Barrier_Attack.attack_size//2:return True
        if self.curx > get_canvas_width() + Barrier_Attack.attack_size//2:return True
        if self.cury < 0 - Barrier_Attack.attack_size//2:return True
        if self.cury > get_canvas_height() + Barrier_Attack.attack_size//2: return True
        return False

class Shout:
    shout_size = 150
    reuse_time = 30
    image = None
    sound = None
    def __init__(self):
        if Shout.image == None:
            Shout.image = load_image('../Pics/dragon_shout.png')
        if Shout.sound == None:
            Shout.sound = load_music('../sounds/dragon_shout.mp3')
            Shout.sound.set_volume(60)
        self.w, self.h = Shout.image.w, Shout.image.h
        self.locked = True
        self.activated = False
        self.ft = 0
    def activate(self):
        if self.locked == True: return
        if self.activated == True: return
        if time.time() - self.ft > Shout.reuse_time:
            self.activated = True
            Shout.sound.play(1)
    def disconnect(self):
        if self.activated == False: return
        self.ft = time.time()
        self.activated = False
    def unlock(self):
        self.locked = False
    def draw(self, s):
        if s == 2:
            Shout.image.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
            if self.locked == True:
                lock.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
        if self.activated == True:
            if self.h_look:
                Shout.image.clip_composite_draw(0, 0, self.w, self.h, 0, 'h', self.x, self.y, Shout.shout_size, Shout.shout_size)
            else:
                Shout.image.clip_composite_draw(0, 0, self.w, self.h, 0, '', self.x, self.y, Shout.shout_size, Shout.shout_size)
    def update(self, h, e, g):
        self.h_look = h.look
        if self.h_look:
            self.x, self.y = h.x + 25 - 50, h.y - 25 + 50
        else:
            self.x, self.y = h.x - 25 + 50, h.y - 25 + 50

        if self.activated == True:
            if len(e) is 0: return
            for ene in e:
                self.give_damage(ene)
    def give_damage(self, e):
        e.hp = -1
        e.change_state(enemy.enemy.state_die[e.lev - 1])

    def handle_events(self):
        if time.time() - self.ft > Shout.reuse_time:
            self.activate()
