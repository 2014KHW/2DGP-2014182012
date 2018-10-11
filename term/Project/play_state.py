from pico2d import *
import game_framework
import score_state
import random
import time

#상수 선언 부분
stage_start = 20
stage_pass = 10

class hero:
    image = None
    def __init__(self):
        self.x, self.y = 400, 250
        self.frame = 0
        if hero.image is None:
            hero.image = load_image('../Pics/hero.png')
    def draw(self):
        hero.image.clip_draw(self.frame * 25, 0, 25, 25, self.x, self.y, 50, 50)
        self.frame = (self.frame + 1) % 7

class enemy:
    image = []
    #상수 정의 부분
    state_appear = 10
    state_stand = 20
    def __init__(self):
        self.x, self.y = random.randint(0+50, 800-50), 400
        self.draw_scale_x, self.draw_scale_y = 50, 200
        self.frame = 0
        self.lev = 1
        self.state = enemy.state_appear
        if len(enemy.image) is 0:
            enemy.image += [load_image('../Pics/enemy_level1.png')]
        elif len(enemy.image) is 1:
            enemy.image += [load_image('../Pics/enemy_level2.png')]
        elif len(enemy.image) is 2:
            enemy.image += [load_image('../Pics/enemy_level3.png')]
    def draw(self):
        if self.state is enemy.state_appear:
            enemy.appear(self)
            return

        enemy.image[self.lev - 1].clip_draw(self.frame * 25, 0, 25, 25, self.x, self.y, self.draw_scale_x, self.draw_scale_y)
        self.frame = (self.frame + 1) % 7

    def appear(self):
        enemy.image[self.lev - 1].clip_draw(self.frame * 25, 0, 25, 25, self.x, self.y, self.draw_scale_x, self.draw_scale_y)
        self.y -= 20
        self.draw_scale_y -= 20
        if self.draw_scale_y <= self.draw_scale_x:
            self.draw_scale_y = self.draw_scale_x
        if self.y < 250:
            self.y = 250
            self.state = self.state_stand


def enter():
    global ground, H, E
    global E_appear_speed, stage_interval, stage_start_time, stage_state

    ground = load_image('../Pics/ground_map.png')

    stage_interval = 10 #스테이지 시간간격
    E_appear_speed = 1.5 #몬스터 출현 속도
    stage_start_time = time.time() #스테이지 시작 시간
    stage_state = stage_start

    E = [enemy()]

    H = hero()

def exit():
    global ground, H, E
    del ground, H, E

def draw():
    global ground, H, E
    global stage_state
    ground.clip_draw(300, 0, 500, 200, 400, 100, 800, 300)

    H.draw()

    if len(E) is not 0:
        for ene in E:
            ene.draw()

    update_canvas()

def handle_events():
    eve = get_events()
    for e in eve:
        if e.type is SDL_QUIT:
            game_framework.quit()

def update():
    global E
    global E_appear_speed, stage_start_time, stage_elapsed_time
    global stage_state

    stage_elapsed_time = time.time()
    if stage_state is stage_start:
        if stage_elapsed_time - stage_start_time >= E_appear_speed:
            E_appear_speed += 1.5
            E += [enemy()]
    if stage_state is stage_pass:
        pass
    delay(0.03)

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    import sys
    current_module = sys.modules[__name__]
    open_canvas()
    game_framework.run(current_module)
    close_canvas()