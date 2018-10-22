from pico2d import *
import random
import math
import game_framework
import json
import time

class Boy:
    image = None
    IDLE = 2
    SLEEP = 102
    RUN = 0
    def __init__(self):
        self.x, self.y = random.randint(30, 500), random.randint(90, 500)
        self.frame = random.randint(0, 7)
        self.speed = random.randint(1, 3)
        self.dstnum = 0 #목적지의 index값을 나타냄 (waypoint 좌표 중, x가 Wp인덱스의 짝수, y가 Wp인덱스의 홀수)
        self.state = Boy.IDLE
        self.dir = random.randint(0, 1)*-2 + 1 #1 또는 -1
        self.stand_time = time.time()
        if Boy.image is None:
            Boy.image = load_image('../Pics/animation_sheet.png')
    def draw(self):
        states = {
            Boy.IDLE : self.draw_idle,
            Boy.RUN : self.draw_run,
            Boy.SLEEP : self.draw_sleep
        }

        states[self.state]()

    def draw_idle(self):
        if self.dir == 1:
            Boy.image.clip_composite_draw(self.frame * 100, self.state * 100, 100, 100, 0, '', self.x, self.y, 100, 100)
        else:
            Boy.image.clip_composite_draw(self.frame * 100, self.state * 100, 100, 100, 0, 'h', self.x, self.y, 100, 100)
    def draw_run(self):
        if self.dir == 1:
            Boy.image.clip_composite_draw(self.frame * 100, self.state * 100, 100, 100, 0, '', self.x, self.y, 100, 100)
        else:
            Boy.image.clip_composite_draw(self.frame * 100, self.state * 100, 100, 100, 0, 'h', self.x, self.y, 100, 100)
    def draw_sleep(self):
        if self.dir == 1:
            Boy.image.clip_composite_draw(self.frame * 100, (self.state-100) * 100, 100, 100, 80, '', self.x, self.y, 100, 100)
        else:
            Boy.image.clip_composite_draw(self.frame * 100, (self.state-100) * 100, 100, 100, -80, 'h', self.x, self.y, 100, 100)

    def update(self):
        states = {
            Boy.IDLE: self.update_idle,
            Boy.RUN: self.update_run,
            Boy.SLEEP: self.update_sleep
        }

        states[self.state]()

    def update_idle(self):
        global time_pass
        elpased_time = time.time()
        if elpased_time - self.stand_time > time_pass:
            print(elpased_time - self.stand_time)
            self.change_state(Boy.SLEEP)
        print(self.dir)
        self.frame = (self.frame + 1) % 8
    def update_run(self):
        global Wp, IDX
        # 최대index값이 dstnum보다 작거나, 최대index값이 0이면 리턴
        self.frame = (self.frame + 1) % 8

        if IDX <= self.dstnum or IDX == 0:
            if self.state is 0:
                self.state = 2
            return

        if (Wp[self.dstnum] < self.x):
            self.dir = 1
        elif (Wp[self.dstnum] > self.x):
            self.dir = -1

        # 목적지와 좌표가 같아진 경우 다음 좌표로 설정(dstnum값 증가)
        if Wp[self.dstnum] == self.x and Wp[self.dstnum + 1] == self.y:
            self.dstnum += 2
            return
        # 먼저 x또는 y축으로 평행하게 가는 경우를 예외처리
        # y값이 같을 경우 x값만 이동
        if Wp[self.dstnum + 1] == self.y:
            if Wp[self.dstnum] < self.x:
                self.x -= self.speed
                if self.x < Wp[self.dstnum]: self.x = Wp[self.dstnum]
                return
            if Wp[self.dstnum] > self.x:
                self.x += self.speed
                if self.x > Wp[self.dstnum]: self.x = Wp[self.dstnum]
                return
        # x값이 같을 경우 y값만 이동
        if Wp[self.dstnum] == self.x:
            if Wp[self.dstnum + 1] < self.y:
                self.y -= self.speed
                if self.y < Wp[self.dstnum + 1]: self.y = Wp[self.dstnum + 1]
                return
            if Wp[self.dstnum + 1] > self.y:
                self.y += self.speed
                if self.y > Wp[self.dstnum + 1]: self.y = Wp[self.dstnum + 1]
                return
        # 이제 기울기가 0으로 나눠질 수도, 0이 될 수도 없으므로 나머지를 구현한다.
        else:

            dif_x, dif_y = Wp[self.dstnum] - self.x, Wp[self.dstnum + 1] - self.y  # 마우스 좌표와 현재 좌표값의 차이
            dist = math.sqrt(dif_x ** 2 + dif_y ** 2)
            self.x += dif_x * self.speed / dist
            self.y += dif_y * self.speed / dist
            if dif_x < 0:
                if Wp[self.dstnum] - self.x > 0: self.x = Wp[self.dstnum]
            else:
                if Wp[self.dstnum] - self.x < 0: self.x = Wp[self.dstnum]
            if dif_y < 0:
                if Wp[self.dstnum + 1] - self.y > 0: self.y = Wp[self.dstnum + 1]
            else:
                if Wp[self.dstnum + 1] - self.y < 0: self.y = Wp[self.dstnum + 1]
    def update_sleep(self):
        pass

    def enter_idle(self):
        global time_pass
        time_pass = 2
        self.stand_time = time.time()
    def enter_run(self):
        pass
    def enter_sleep(self):
        pass

    def exit_idle(self):
        self.frame = 0
    def exit_run(self):
        self.frame = 0
    def exit_sleep(self):
        self.frame = 0

    def change_state(self, state):
        enter = {
            Boy.IDLE: self.enter_idle,
            Boy.RUN: self.enter_run,
            Boy.SLEEP: self.enter_sleep
        }
        exit = {
            Boy.IDLE: self.exit_idle,
            Boy.RUN: self.exit_run,
            Boy.SLEEP: self.exit_sleep
        }

        exit[self.state]()
        enter[state]()
        self.state = state

class Grass:
    def __init__(self):
        self.image = load_image('../Pics/grass.png')
    def draw(self):
        self.image.draw(400, 30)

def handle_events():
    global running, Wp, IDX, boy
    events = get_events()
    for eve in events:
        if eve.type == SDL_QUIT:
            print('I\'m called boys quit')
            game_framework.quit()
        elif eve.type == SDL_KEYDOWN:
            if eve.key == SDLK_ESCAPE:
                game_framework.pop_state()
        elif eve.type == SDL_MOUSEBUTTONDOWN:
            if eve.button == 1:
                Wp += [eve.x, 600 - eve.y]
                IDX += 2
                for e in boy:
                    e.change_state(Boy.RUN)
            elif eve.button == 3:
                Wp = []
                IDX = 0
                for i in boy:
                    i.dstnum = 0
                    i.change_state(Boy.IDLE)

def enter():
    global IDX, running, Wp, boy, grass

    IDX = 0 #waypoint의 인덱스. 2씩 증가한다. (x좌표를 짝수번째에 저장, y좌표를 홀수 번째에 저장하기때문)
    running = True
    Wp = []
    boy = [Boy() for i in range(4)]

    for e in boy:
        e.change_state(Boy.IDLE)

    grass = Grass()

def draw():
    global running, grass, boy
    if running:
        clear_canvas()
        grass.draw()

        for i in boy:
            i.draw()
        update_canvas()

def update():
    global running, boy
    if running:
        for i in boy:
            i.update()

        delay(0.03)

def exit():
    pass

def pause():
    global running
    running = False

def resume():
    global running
    running = True

if __name__ == '__main__':
    import sys
    current_module = sys.modules[__name__]
    open_canvas()
    game_framework.run(current_module)
    close_canvas()