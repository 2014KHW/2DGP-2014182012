from pico2d import *
import math

def handle_events():
    
    global running
    
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def GO_RIGHT(grass, character, x, y, frame):
    while(x < 800 - 10 and running):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame*100, 0, 100, 100, x, y)
        frame +=1
        frame %=8
        update_canvas()
        x = x+10
        delay(0.05)
        handle_events()
    return x
def GO_UP(grass, character, x, y, frame):
    global running
    while(y<600 - 30 and running):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame += 1
        frame %= 8
        update_canvas()
        y = y + 10
        delay(0.05)
        handle_events()
    return y
def GO_LEFT(grass, character, x, y, frame):
    while(x> 0 + 10 and running):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame += 1
        frame %= 8
        update_canvas()
        x = x - 10
        delay(0.05)
        handle_events()
    return x
def GO_DOWN(grass, character, x, y, frame):
    while(y> 90 and running):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame * 100, 0, 100, 100, x, y)
        frame += 1
        frame %= 8
        update_canvas()
        y = y - 10
        delay(0.05)
        handle_events()
    return y
def DRAW_RECT(grass, character, x, y, frame):


    x=GO_RIGHT(grass, character, x, y, frame)

    y=GO_UP(grass, character, x, y, frame)

    x=GO_LEFT(grass, character, x, y, frame)

    y=GO_DOWN(grass, character, x, y, frame)

def GO_CIRCLE(grass, character, frame, r=160, angle=0):
    PI = 3.14
    x = 0
    while(x < 180 and running):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame * 100, 0, 100, 100, r * math.sin(angle*PI) + 400, r * math.cos(angle*PI) + 300)
        frame += 1
        frame %= 8
        update_canvas()
        angle += 1/90
        x += 1
        delay(0.05)
        handle_events()
    return y

open_canvas()

grass = load_image('../Pics/grass.png')
character = load_image('../Pics/run_animation.png')

x=0
y=90
frame=0
running = True

while running:
    DRAW_RECT(grass, character, x, y, frame)

    y = 90
    x = 400
    # 4번째 인자는 반지름의 길이 이므로, 원운동시 그려지는 원의 크기를 나타냄
    # 5번째 인자는 시작 각도의 크기
    GO_CIRCLE(grass, character, frame, 160, 1)
    x = 0 + 10

close_canvas()
