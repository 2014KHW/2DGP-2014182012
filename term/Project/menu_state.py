from pico2d import *
import game_framework
import play_state

def enter():
    global sky, ground, button_list, select_cursor, frame, cur_selection
    sky = load_image('../Pics/sky_background.png')
    ground = load_image('../Pics/ground_map.png')
    button_list = load_image('../Pics/button_list.png')
    select_cursor = load_image('../Pics/select_leaf.png')
    cur_selection = -1
    frame = 0

def exit():
    global sky, ground, button_list, select_cursor
    del sky, ground, button_list, select_cursor

def draw():
    global sky, ground, button_list, select_cursor, frame, cur_selection
    sky.clip_draw(200, 100, 400, 450, 400, 300, 800, 600)
    ground.clip_draw(200, 0, 600, 200, 400, 100, 800, 300)
    button_list.clip_draw(0, 0, 100, 25, 400, 300 - 50, 200, 50)
    button_list.clip_draw(0, 25, 100, 25, 400, 300, 200, 50)
    button_list.clip_draw(0, 50, 100, 25, 400, 300 + 50, 200, 50)
    select_cursor.clip_draw(frame * 40, 0, 40, 24, 400 + 120, 300 + 50 * cur_selection, 80, 48)

def handle_events():
    global cur_selection
    eve = get_events()
    for e in eve:
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_UP:
                cur_selection = min(cur_selection + 1, 1)
            elif e.key == SDLK_DOWN:
                cur_selection = max(cur_selection - 1, -1)
            elif e.key == SDLK_RETURN:
                if cur_selection is 0:
                    pass
                    #game_framework.change_state(score_state)
                elif cur_selection is 1:
                    game_framework.change_state(play_state)
                elif cur_selection is -1:
                    game_framework.quit()

def update():
    global frame
    frame = (frame + 1) % 5
    update_canvas()
    delay(0.05)

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