from pico2d import *
import random
import time
import game_world
from ball import Ball

# Boy State
# IDLE, RUN, SLEEP = range(3)

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, TIME_OUT, SPACE_DOWN, ENTER_DOWN, MOUSE_MOVE = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYDOWN, SDLK_RETURN): ENTER_DOWN,
    (SDL_MOUSEMOTION, None): MOUSE_MOVE,
}

class IdleState:
    @staticmethod
    def enter(boy):
        boy.time = time.time()
    @staticmethod
    def exit(boy):
        pass
    @staticmethod
    def update(boy):
        boy.dist = math.sqrt((boy.mx - boy.x) ** 2 + (boy.my - boy.y) ** 2) / 200
        boy.frame = (boy.frame + 1) % 8
        elapsed = time.time() - boy.time
        if elapsed > 10.0:
            boy.set_state(SleepState)
    @staticmethod
    def draw(boy):
        y = 200 if boy.dir == 0 else 300
        Boy.image.clip_draw(boy.frame * 100, y, 100, 100, boy.x, boy.y)
        Boy.image2.clip_composite_draw(0, 0, 85, 25, boy.rad, '', boy.x, boy.y)

class RunState:
    @staticmethod
    def enter(boy):
        boy.time = time.time()
    @staticmethod
    def exit(boy):
        pass
    @staticmethod
    def update(boy):
        elapsed = time.time() - boy.time
        mag = 2 if elapsed > 2.0 else 1
        # print(mag, elapsed)
        boy.frame = (boy.frame + 1) % 8
        boy.x = max(25, min(boy.x + mag * boy.dx, 775))
    @staticmethod
    def draw(boy):
        y = 0 if boy.dir == 0 else 100
        Boy.image.clip_draw(boy.frame * 100, y, 100, 100, boy.x, boy.y)
        Boy.image2.clip_composite_draw(0, 0, 85, 25, boy.rad, '', boy.x, boy.y)

class SleepState:
    @staticmethod
    def enter(boy):
        boy.time = time.time()
    @staticmethod
    def exit(boy):
        pass
    @staticmethod
    def update(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            y, mx, angle = 300, -25, 3.141592/2
        else:
            y, mx, angle = 200, +25, -3.141592/2
        Boy.image.clip_composite_draw(boy.frame * 100, y, 100, 100, 
            angle, '', boy.x + mx, boy.y - 25, 100, 100)
        Boy.image2.clip_composite_draw(0, 0, 85, 25, boy.rad, '', boy.x, boy.y)

next_state_table = {
    IdleState: { RIGHT_UP: RunState,  LEFT_UP: RunState,  RIGHT_DOWN: RunState,  LEFT_DOWN: RunState, TIME_OUT: SleepState},
    RunState:  { RIGHT_UP: IdleState, LEFT_UP: IdleState, RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState },
    SleepState: { LEFT_DOWN: RunState, RIGHT_DOWN: RunState }
}


class Boy:
    image = None
    image2 = None

    def __init__(self):
        print("Creating..")
        self.x = random.randint(0, 200)
        self.y = random.randint(90, 550)
        self.mx = self.x
        self.my = self.y
        self.rad = math.atan2(self.my - self.y, self.mx - self.x)
        self.dist = math.sqrt((self.mx-self.x)**2 + (self.my - self.y)**2)
        self.y = 90
        self.speed = 3
        self.frame = random.randint(0, 7)
        self.state = None
        self.set_state(IdleState)
        self.dir = 1
        self.dx = 0
        if Boy.image == None:
            Boy.image = load_image('../Pics/animation_sheet.png')
        if Boy.image2 == None:
            Boy.image2 = load_image('../Pics/arrow.png')

    def draw(self):
        self.rad = math.atan2(self.my - self.y, self.mx - self.x)
        self.state.draw(self)

    def update(self):
        self.state.update(self)

    def handle_event(self, e):
        if (e.type, e.key) in key_event_table:
            key_event = key_event_table[(e.type, e.key)]
            if key_event == SPACE_DOWN or key_event == ENTER_DOWN:
                 self.fire_ball(key_event == ENTER_DOWN)
                 if self.state == SleepState:
                     self.set_state(IdleState)
                 return
            if key_event == RIGHT_DOWN:
                self.dx += self.speed
                if self.dx > 0: self.dir = 1
            elif key_event == LEFT_DOWN:
                self.dx -= self.speed
                if self.dx < 0: self.dir = 0
            elif key_event == RIGHT_UP:
                self.dx -= self.speed
                if self.dx < 0: self.dir = 0
            elif key_event == LEFT_UP:
                self.dx += self.speed
                if self.dx > 0: self.dir = 1
            elif key_event == MOUSE_MOVE:
                self.mx = e.x
                self.my = get_canvas_height() - e.y
                print(e.x, get_canvas_height() - e.y)

            self.set_state(IdleState if self.dx == 0 else RunState)
            # print(self.dx, self.dir)
    def set_state(self, state):
        if self.state == state: return

        if self.state and self.state.exit:
            self.state.exit(self)

        self.state = state

        if self.state.enter:
            self.state.enter(self)
    def fire_ball(self, big):
        mag = 1.5 if self.dir == 1 else -1.5
        distance_x = (self.mx - self.x) / 200
        distance_y = (self.my - self.y) / 200
        ballSpeed = (mag * self.speed + self.dx) * distance_x

        ySpeed = 2 * self.speed * distance_y
        if big: ySpeed *= 0.75
        ball = Ball(big, self.x, self.y, ballSpeed, ySpeed)
        game_world.add_object(ball, game_world.layer_obstacle)
