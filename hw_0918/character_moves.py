from pico2d import *
import pdb #디버그에 사용되는 모듈

speed = 10

def handle_events():
    global running
    global x, y
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
        elif e.type == SDL_MOUSEMOTION:
            x, y = e.x, 600 - e.y
def follow_cursor():
    global CharactX, CharactY, x, y, speed
    i = 0
    if ( CharactX < x ):
        while (i<speed):
            if(CharactX == x):
                i=speed
                break
            CharactX += 1
            i+=1
    i = 0
    if ( CharactX > x ):
        while (i<speed):
            if(CharactX == x):
                i=speed
                break
            CharactX -= 1
            i+=1
    i = 0
    if ( CharactY < y ):
        while (i<speed):
            if(CharactY == y):
                i=speed
                break
            CharactY += 1
            i+=1
    i = 0
    if ( CharactY > y ):
        while (i < speed):
            if (CharactY == y):
                i=speed
                break
            CharactY -= 1
            i+=1

open_canvas()

grass = load_image('../Pics/grass.png')
character = load_image('../Pics/run_animation.png')

x, y = 800 // 2, 90
CharactX, CharactY = x, y
frame = 0
speed = 10 #스피드 변수 추가
running = True
while running:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 0, 100, 100, CharactX, CharactY)
    follow_cursor() #커서 따라가는 함수 추가
    update_canvas()
    handle_events()
    #커서에 위치해 더이상 움직임이 없을 때 프레임 애니메이션을 중지
    if (CharactX == x and CharactY == y):
        frame = 0
    else:
        frame = (frame + 1) % 8
    delay(0.05)
    
close_canvas()
