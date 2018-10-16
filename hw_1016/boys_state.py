from pico2d import *
import random
import math
import game_framework
import json

class Boy:
    image = None
    def __init__(self):
        self.x, self.y = random.randint(30, 500), random.randint(90, 500)
        self.frame = random.randint(0, 7)
        self.speed = random.randint(1, 3)
        self.dstnum = 0 #목적지의 index값을 나타냄 (waypoint 좌표 중, x가 Wp인덱스의 짝수, y가 Wp인덱스의 홀수)
        self.state = random.randint(2, 3)
        if Boy.image is None:
            Boy.image = load_image('../Pics/animation_sheet.png')
    def draw(self):
            Boy.image.clip_draw(self.frame * 100, self.state*100, 100, 100, self.x, self.y)

    def run(self):
        global Wp, IDX
        #최대index값이 dstnum보다 작거나, 최대index값이 0이면 리턴
        self.frame = (self.frame+1)%7

        if IDX <= self.dstnum or IDX == 0 :
            if self.state is 0 :
                self.state = 2
            elif self.state is 1:
                self.state = 3
            return

        if (Wp[self.dstnum] < self.x):
            self.state = 0
        elif (Wp[self.dstnum] > self.x):
            self.state = 1
        elif (Wp[self.dstnum] == self.x):
            if self.state is 0 :
                self.state = 2
            elif self.state is 1 :
                self.state = 3

        #목적지와 좌표가 같아진 경우 다음 좌표로 설정(dstnum값 증가)
        if Wp[self.dstnum] == self.x and Wp[self.dstnum+1] == self.y:
            self.dstnum += 2
            return
        #먼저 x또는 y축으로 평행하게 가는 경우를 예외처리
        #y값이 같을 경우 x값만 이동
        if Wp[self.dstnum+1] == self.y :
            if Wp[self.dstnum] < self.x :
                self.x -= self.speed
                if self.x < Wp[self.dstnum] : self.x = Wp[self.dstnum]
                return
            if Wp[self.dstnum] > self.x :
                self.x += self.speed
                if self.x > Wp[self.dstnum] : self.x = Wp[self.dstnum]
                return
        #x값이 같을 경우 y값만 이동
        if Wp[self.dstnum] == self.x:
            if Wp[self.dstnum+1] < self.y :
                self.y -= self.speed
                if self.y < Wp[self.dstnum+1] : self.y = Wp[self.dstnum+1]
                return
            if Wp[self.dstnum+1] > self.y :
                self.y += self.speed
                if self.y > Wp[self.dstnum+1] : self.y = Wp[self.dstnum+1]
                return
        #이제 기울기가 0으로 나눠질 수도, 0이 될 수도 없으므로 나머지를 구현한다.
        else :

            dif_x, dif_y = Wp[self.dstnum] - self.x, Wp[self.dstnum+1] - self.y #마우스 좌표와 현재 좌표값의 차이
            dist = math.sqrt(dif_x**2 + dif_y**2)
            self.x += dif_x * self.speed / dist
            self.y += dif_y * self.speed / dist
            if dif_x < 0 :
                if Wp[self.dstnum] - self.x > 0 : self.x = Wp[self.dstnum]
            else :
                if Wp[self.dstnum] - self.x < 0 : self.x = Wp[self.dstnum]
            if dif_y < 0 :
                if Wp[self.dstnum+1] - self.y > 0 : self.y = Wp[self.dstnum+1]
            else :
                if Wp[self.dstnum+1] - self.y < 0 : self.y = Wp[self.dstnum+1]



class Grass:
    def __init__(self):
        self.image = load_image('../Pics/grass.png')
    def draw(self):
        self.image.draw(400, 30)

def handle_events():
    global running, Wp, IDX
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
            elif eve.button == 3:
                Wp = []
                IDX = 0
                for i in boy:
                    i.dstnum = 0

def enter():
    global IDX, running, Wp, boy, grass

    IDX = 0 #waypoint의 인덱스. 2씩 증가한다. (x좌표를 짝수번째에 저장, y좌표를 홀수 번째에 저장하기때문)
    running = True
    Wp = []
    #boy = [Boy() for i in range(1000)]
    boy = []
    fn = open('boys_data.json')
    data = json.load(fn)
    for e in data['boys']:
        b = Boy()
        b.name = e['name']
        b.x = e['x']
        b.y = e['y']
        b.speed = e['speed']
        boy += [b]
    print(data)

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
            i.run()

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