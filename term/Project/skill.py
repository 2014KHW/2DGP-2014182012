from pico2d import *
import time
import random
import hero

lock = None

class Thunder:
    image = None
    slot = None
    reuse_time = 10
    def __init__(self, x):
        if Thunder.image is None:
            Thunder.image = load_image('../Pics/thunder_drop.png')
        if Thunder.slot is None:
            Thunder.slot = load_image('../Pics/thunder_slot.png')
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
    def draw(self):
        Thunder.slot.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
        if self.locked == True:
            lock.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
        if self.activated == True:
            Thunder.image.clip_draw(self.frame * 25, 0, 25, 200, self.x, 250 + (get_canvas_height() - 250)//2, 150, get_canvas_height() - 200)
    def update(self, h):
        self.frame = (self.frame + 1) % 8
        if self.frame == 0:
            self.x = random.randint(0 + 150, 800 - 150)
            self.cur_drops += 1
        if self.cur_drops > self.drop_times:
            self.disconnect()
    def handle_events(self):
        print('I\'m in')
        if time.time() - self.ft > Thunder.reuse_time:
            self.activate()

class Barrier:
    barrier = None
    attack = None
    slot = None
    lasting_time = 5
    success_reuse_time = 10
    fail_reuse_time = 3
    barrier_size = 60
    def __init__(self):
        if Barrier.barrier is None:
            Barrier.barrier = load_image('../Pics/barrier.png')
        if Barrier.attack is None:
            Barrier.attack = load_image('../Pics/counter_attack.png')
        if Barrier.slot is None:
            Barrier.slot = load_image('../Pics/counter_slot.png')
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
        self.attack_add_time = 0.5
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
    def disconnect(self):
        self.mode = 'disappear'
        self.ft = time.time()
        self.activated = False
    def get_attack(self):
        if time.time() - self.at > self.attack_add_time:
            self.attack += [Barrier_Attack()]
            self.at = time.time()
            self.getting_times += 1
            if self.getting_times == 10:
                self.waiting_kind = 'success'
                self.disconnect()

    def draw(self):
        Barrier.slot.clip_draw(0, 0, 50, 50, 75, 600 - 75, 50, 50)
        if self.locked == True:
            lock.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
        if self.mode == 'ready':
            Barrier.barrier.clip_draw(self.frame * 50, 0, 50, 50, self.x, self.y, Barrier.barrier_size, Barrier.barrier_size)

    def update(self, h, cmod=False):
        self.frame = (self.frame + 1) % 5
        self.x, self.y = h.x, h.y
        if cmod == True and self.mode == 'ready':
            self.mode = 'counter'
        if self.mode == 'ready':
            if time.time() - self.st > Barrier.lasting_time:
                self.st = 0
                self.waiting_kind = 'fail'
                self.disconnect()
        if self.activated is True:
            self.get_attack()
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
    def __init__(self, deg, hx, hy):
        self.speed = 10
        self.deg = deg
        self.curx, self.cury = hx, hy
        self.del_sign = False
        self.frame = 0
    def draw(self):
        if self.del_sign == False:
            Barrier.attack.clip_draw(self.frame * 50, 0, 50, 50, self.curx, self.cury, Barrier_Attack.attack_size, Barrier_Attack.attack_size)
    def update(self):
        self.frame = (self.frame + 1) % 4
        if self.outs():self.del_sign = True
    def outs(self):
        if self.curx < 0 - Barrier_Attack.attack_size//2:return True
        if self.curx > get_canvas_width() + Barrier_Attack.attack_size//2:return True
        if self.cury < 0 - Barrier_Attack.attack_size//2:return True
        if self.cury > get_canvas_height() + Barrier_Attack.attack_size//2: return True
        return False

class Shout:
    shout_size = 100
    reuse_time = 20
    image = None
    def __init__(self):
        if Shout.image == None:
            Shout.image = load_image('../Pics/dragon_shout.png')
        self.w, self.h = Shout.image.w, Shout.image.h
        self.locked = True
        self.activated = False
        self.ft = 0
    def activate(self):
        if self.locked == True: return
        if self.activated == True: return
        if time.time() - self.ft > Shout.reuse_time:
            self.activated = True
    def unlock(self):
        self.locked = False
    def draw(self):
        Shout.image.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
        if self.locked == True:
            lock.clip_draw(0, 0, 100, 100, 75, 600 - 75, 50, 50)
        if self.activated == True:
            Shout.image.clip_draw(0, 0, self.w, self.h, self.x, self.y, Shout.shout_size, Shout.shout_size)
    def update(self, h):
        self.x, self.y = h.x - 25 + 50, h.y - 25 + 50
