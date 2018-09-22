from pico2d import *
import random
import math
import pdb

class Boy:
    def __init__(self):
        self.image = load_image('../Pics/run_animation.png')
        self.x, self.y = random.uniform(30, 500), random.uniform(90, 500)
        self.frame = random.randint(0, 7)
        self.speed = random.randint(1, 3)
    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
    def run(self):
        global Mx, My
        if Mx == self.x and My == self.y:
            return
        #먼저 x또는 y축으로 평행하게 가는 경우를 예외처리
        #y값이 같을 경우 x값만 이동
        if My == self.y :
            if Mx < self.x :
                self.x -= self.speed
                if self.x < Mx : self.x = Mx
                return
            if Mx > self.x :
                self.x += self.speed
                if self.x > Mx : self.x = Mx
                return
        #x값이 같을 경우 y값만 이동
        if Mx == self.x:
            if My < self.y :
                self.y -= self.speed
                if self.y < My : self.y = My
                return
            if My > self.y :
                self.y += self.speed
                if self.y > My : self.y = My
                return
        #이제 기울기가 0으로 나눠질 수도, 0이 될 수도 없으므로 나머지를 구현한다.
        else :
            dif_x, dif_y = Mx - self.x, My - self.y  #마우스 좌표와 현재 좌표값의 차이
            dist = math.sqrt(dif_x**2 + dif_y**2)
            self.x += dif_x * self.speed / dist
            self.y += dif_y * self.speed / dist



class Grass:
    def __init__(self):
        self.image = load_image('../Pics/grass.png')
    def draw(self):
        self.image.draw(400, 30)

def handle_events():
    global running, Mx, My
    events = get_events()
    for eve in events:
        if eve.type == SDL_QUIT:
            running = False
        elif eve.type == SDL_KEYDOWN:
            if eve.key == SDLK_ESCAPE:
                running = False
        elif eve.type == SDL_MOUSEMOTION:
            Mx, My = eve.x, 600 - eve.y

open_canvas()
Mx, My =100, 100
running = True

boy = [Boy() for i in range(20)]
grass = Grass()

while running:
    handle_events()
    clear_canvas()
    grass.draw()
    for i in boy:
        i.draw()
        i.run()
    update_canvas()
    delay(0.01)

close_canvas()