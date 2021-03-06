from pico2d import *
import game_framework
import menu_state
import score_state
import random
import time
import math
import rectangle
import hero
import enemy
import item
import skill

total_elapse = 0
total_start = time.time()
total_score = 0
total_kills = 0
total_stage = 1j

#상수 선언 부분
stage_start = 20
stage_pass = 10
stop = False
Item_created = False

class fever:
    image_R = None
    image_B = None
    nums = None
    #상수 정의
    def __init__(self):
        self.x, self.y = 400 + 200, 600 - 20 - 20
        self.sx, self.sy = 50, 50
        self.bx, self.by = self.x, self.y
        self.bsx, self.bsy = 20, 20
        self.max_fev = 0
        self.fev = 0
        self.rot_pos = 0
        self.speed = 3
        self.ssx, self.ssy = int(self.sx/2), 0

        if fever.image_B == None:
            fever.image_B = load_image('../Pics/fever_ip.png')
        if fever.image_R == None:
            fever.image_R = load_image('../Pics/fever_pos.png')
        if fever.nums == None:
            fever.nums = load_image('../Pics/nums.png')
    def draw_nums(self):
        tmpnum = self.fev
        if self.fev == 0:
            fever.nums.clip_draw(0, 450, 50, 50, self.bx - self.sx, self.by - self.sy//2, 20, 20)
            return

        cnt = 0
        while tmpnum > 0:
            fever.nums.clip_draw(0, (9 - (tmpnum % 10))*50, 50, 50, self.bx - self.sx - cnt*15, self.by - self.sy//2, 20, 20)
            tmpnum //= 10
            cnt += 1
    def draw(self):
        fever.image_B.clip_draw(0, 0, 200, 200, self.x, self.y, self.sx, self.sy)
        fever.image_R.clip_draw(0, 0, 200, 200, self.bx + self.ssx, self.by + self.ssy, self.bsx, self.bsy)
        self.draw_nums()
    def update(self):
        if self.fev == 0:
            return
        if self.max_fev < self.fev: self.max_fev = self.fev
        rad = self.fev*self.speed/10
        self.rot_pos += rad
        #print('self.rotpos : ',self.rot_pos)
        if self.rot_pos > 360:
            self.rot_pos = 0
            self.fev = max(0, self.fev - 1)
        self.ssx = int(self.sx/2)*math.cos(-self.rot_pos*math.pi/180 + math.pi/2)
        self.ssy = int(self.sy/2)*math.sin(-self.rot_pos*math.pi/180 + math.pi/2)

class phrase:
    image = None
    #상수 정의
    original_pos = 400
    state_stop = 100
    state_move = 10
    def __init__(self, state):
        self.x, self.y = 500, 500
        self.create_time = time.time()
        self.state = phrase.state_move
        if state is stage_start:
            phrase.image = load_image('../Pics/stage_start.png')
        if state is stage_pass:
            phrase.image = load_image('../Pics/stage_pass.png')
    def draw(self, state):
        if state is stage_start:
            phrase.image.clip_draw(0, 0, 426, 58, self.x, self.y)
        if state is stage_pass:
            phrase.image.clip_draw(0, 0, 409, 58, self.x, self.y)
        self.x -= 5
        if self.x < phrase.original_pos:
            self.x = phrase.original_pos

class number:
    number_image = None
    def __init__(self, num):
        self.score = num
        self.draw_list = [0, 0, 0, 0, 0, 0, 0]
        self.change = False
        self.x = 0
        self.y = [450, 450, 450, 450, 450, 450]
        if number.number_image is None:
            number.number_image = load_image('../Pics/nums.png')

    def draw(self):
        for i in range(6):
            number.number_image.clip_draw(self.x, self.y[i], 50, 50, 800 - (i + 1) * 25, 600 - 25)
    def change_num(self, num):
        if self.score == num:
            return

        self.score = num
        tmp_score = num

        for i in range(len(self.draw_list)):
            self.draw_list[i] = tmp_score % 10
            tmp_score //= 10

        return

    def update(self, num):
        self.change_num(num)
        for i in range(len(self.draw_list) - 1):
            self.update_number(i)
    def update_number(self, index):
        if self.y[index] == (9 - self.draw_list[index]) * 50:
            return
        elif self.y[index] > (9 - self.draw_list[index]) * 50:
            self.y[index] -= 3
            if self.y[index] <= (9 - self.draw_list[index]) * 50:
                self.y[index] = (9 - self.draw_list[index]) * 50
        elif self.y[index] < (9 - self.draw_list[index]) * 50:
            self.y[index] += 3
            if self.y[index] >= (9 - self.draw_list[index]) * 50:
                self.y[index] = (9 - self.draw_list[index]) * 50

class shaking:
    def __init__(self):
        self.shake_strength = 3
        self.move = -1
        self.on_shaking = False
        self.by_skill = False
        self.add_shaking = 1
    def shake(self):
        global H, E, ground_x, ground_y
        global skill_inv
        if self.by_skill is True: self.add_shaking = 2
        else: self.add_shaking = 1
        if self.on_shaking is False:
            return
        if self.shake_strength <= 0:
            if self.by_skill is True:
                skill_inv[2].disconnect()
                self.by_skill = False
            self.on_shaking = False
            return

        H[-1].x += self.shake_strength * self.move
        if len(E) is not 0:
            for ene in E:
                ene.x += self.shake_strength * self.move

        ground_x += self.shake_strength * self.move
        ground_y += self.shake_strength * self.move/2

        if self.move is -1:
            self.move = 1
        else:
            self.move = -1
            self.shake_strength -= 1 * self.add_shaking

    def give_shake(self):
        global H, selection, skill_inv
        if self.on_shaking is False and H[-1].state is hero.hero.h_attack[H[-1].attack_type]:
            self.on_shaking = True
            self.shake_strength = 5
        elif selection == 2 and skill_inv[selection].activated == True:
            if self.by_skill == True: return
            self.on_shaking = True
            self.shake_strength = 25
            self.by_skill = True
        else:
            return


def enter():
    global sky, ground, rsky, rground, rev_state, stage_term, stamp, H, E, phase
    global ground_x, ground_y, sky_x, sky_y
    global fev
    global stage_start_time, stage_state
    global E_appear_speed, E_appear_time_ratio, Emax
    global hit
    global shake, up_key_on, down_key_on, left_key_on, right_key_on
    global dash_dir # 1: 상 10: 하 100: 좌 1000: 우
    global cur_score
    global Item, Item_last_create_time, Item_create_time
    global skill_inv, slot
    global selection

    skill.lock = load_image('../Pics/locked.png')
    rev_state = False
    ground_x, ground_y = 200, 100
    sky_x, sky_y = 200, 100
    shake = shaking()
    sky = load_image('../Pics/sky_background.png')
    rsky = load_image('../R_Pics/sky_background.png')
    ground = load_image('../Pics/ground_map.png')
    rground = load_image('../R_Pics/ground_map.png')
    hit = load_image('../Pics/hit_effect.png')
    slot = load_image('../Pics/skill_slot.png')
    stage_term = load_image('../Pics/vacant_bar.png')
    stamp = load_image('../Pics/hero_stamp.png')
    fev = fever()
    skill_inv = [skill.Thunder(random.randint(0 + 150, 800 - 150)), skill.Barrier(), skill.Shout()]
    selection = 0

    E_appear_speed = 0.5 #몬스터 출현 속도
    E_appear_time_ratio = 1 #몬스터 출현 속도 증가량
    Emax = 10 #몬스터 최대 출현 수
    stage_start_time = time.time() #스테이지 시작 시간
    stage_state = stage_start

    up_key_on, down_key_on, left_key_on, right_key_on = False, False, False, False

    H = [hero.hero()]

    E = [enemy.enemy(H[-1], H[-1])]

    Item = []
    Item_last_create_time = time.time()
    Item_create_time = 1

    cur_score = number(0)

    phase = [phrase(stage_state)]

def move_bg_by_hero(h):
    global ground_x, sky_x, ground_y, sky_y
    if h.state == hero.hero.h_jump_ready:return
    if h.go_L is True:
        move_bg_lr(5, -1)
    elif h.go_R is True:
        move_bg_lr(5, +1)
    if h.jump is True:
        if h.ascend is True:
            move_bg_ud(h, +1)
        else:
            move_bg_ud(h, -1)
    else:
        ground_y, sky_y = 100, 100
    if h.dashing is True:
        if h.dash_dir & 1 == 1:
            ground_y = max(0, ground_y - h.dash_dist)
            sky_y = max(0, sky_y - h.dash_dist//2)
        if h.dash_dir & 10 == 10 or h.dash_dir & 10 == 2:
            ground_y += h.dash_dist
            sky_y += h.dash_dist//2
        if h.dash_dir & 100 == 100:
            ground_x = max(0 + 25, ground_x - h.dash_dist)
            sky_x = max(0 + 25, sky_x - h.dash_dist//2)
        if h.dash_dir & 1000 == 1000 or h.dash_dir & 1000 == 992:
            ground_x = min(ground_x + h.dash_dist,  ground.w - 600)
            sky_x = min(sky_x + h.dash_dist//2, sky.w - 400)
    if len(E) is not 0:
        for ene in E:
            if ene.state != enemy.enemy.state_appear:
                ene.y = ground_y + 160
def move_bg_lr(move, dir):
    global ground_x, sky_x
    ground_x = clamp(0, ground_x + move * dir / 5, ground.w - 600)
    sky_x = clamp(0, sky_x + move * dir / 10, sky.w - 400)
    if len(E) is not 0:
        for ene in E:
            ene.x = clamp(0, ene.x + move * dir / 20, sky.w - 400)
def move_bg_ud(h, dir):
    global ground_y, sky_y
    if h.state == hero.hero.h_attack[h.attack_type]:
        ground_y -= 2 * dir / 5
        sky_y -= 2 * dir / 10
        if len(E) is not 0:
            for ene in E:
                ene.y += 2 * dir / 5
                if len(ene.attack_object) is not 0:
                    for ao in ene.attack_object:
                        ao.y += 2 * dir / 5
    else:
        ground_y += (h.va_speed - h.va_a) * -dir * 2 / 5
        sky_y += (h.va_speed - h.va_a) * -dir * 2 / 10
        if len(E) is not 0:
            for ene in E:
                ene.y += (h.va_speed - h.va_a) * -dir * 2 / 5
                if len(ene.attack_object) is not 0:
                    for ao in ene.attack_object:
                        ao.y += (h.va_speed - h.va_a) * -dir * 2 / 5


def exit():
    global sky, ground, rsky, rground, H, E, hit, slot, stage_term, stamp
    del sky, ground, rsky, rground, H, E, hit, slot, stage_term, stamp

def draw():
    global sky, ground, rsky, rground, rev_state, slot, stage_term, stamp, H, E, phase
    global ground_x, ground_y
    global stage_start_time, stage_elapsed_time
    global stage_state
    global stop
    global cur_score
    global skill_inv, selection
    global fev

    if stop is True:
        return

    clear_canvas()
    if rev_state is False:
        sky.clip_draw(int(sky_x), int(sky_y), 400, 450, 400, 300, 800, 600)
        ground.clip_draw(int(ground_x), 0, 600, 200, 400, int(ground_y), 800, 300)
    else:
        rsky.clip_draw(int(sky_x), int(sky_y), 400, 450, 400, 300, 800, 600)
        rground.clip_draw(int(ground_x), 0, 600, 200, 400, int(ground_y), 800, 300)
    slot.clip_draw(0, 0, 125, 125, 75, 600 - 75, 75, 75)
    stage_term.clip_draw(0, 0, 125, 9, 400, 600 - 20, 400, 10)
    for i in range(3):
            skill_inv[i].draw(selection)
    if stage_state is stage_start:
        stamp.clip_draw(0, 0, 19, 16, 400 - 200 * (1 - (stage_elapsed_time - stage_start_time) * 2 / stage_start), 600 - 20, 19, 16)
    else:
        stamp.clip_draw(0, 0, 19, 16, 400 - 200 * (1 - (stage_elapsed_time - stage_start_time) * 2 / stage_pass), 600 - 20, 19, 16)


    if len(E) is not 0:
        for ene in E:
            ene.draw(ground_y + 160)
            if len(ene.attack_object) is not 0:
                for obj in ene.attack_object:
                    if obj.del_sign is False:
                        obj.draw()

    if len(phase) is not 0:
        for ph in phase:
            ph.draw(stage_state)
        if phase[-1].x is phrase.original_pos:
            phase.pop()

    if len(H) is not 0:
        for he in H:
            he.draw()

    if len(Item) is not 0:
        for i in Item:
            i.draw()

    cur_score.draw()
    fev.draw()

    update_canvas()

def handle_events():
    global H, stop, up_key_on, down_key_on, left_key_on, right_key_on, rev_state
    global skill_inv, selection
    global play_sound
    eve = get_events()
    for e in eve:
        if e.type is SDL_QUIT:
            print('quit')
            game_framework.quit()
        if e.key == SDLK_j:
            if H[-1].state is hero.hero.h_stand or H[-1].state is hero.hero.h_move:
                return
            if H[-1].state is hero.hero.h_jump_ready:
                return
            H[-1].attack_type = random.randint(0, 1)
            H[-1].state = hero.hero.h_attack[H[-1].attack_type]
            H[-1].frame = 0
            H[-1].attack_num = (H[-1].attack_num + 1)%10
            if e.type == SDL_KEYDOWN:
                hero.hero.sound_attack.play(1)
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_w):
            up_key_on = True
            down_key_on = False
            if H[-1].jump is True :
                return
            H[-1].change_state(hero.hero.h_jump_ready)
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_s):
            down_key_on = True
            up_key_on = False
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_a):
            H[-1].go_L = True
            if H[-1].state is hero.hero.h_stand:
                H[-1].change_state(hero.hero.h_move)
            left_key_on = True
            right_key_on = False
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_d) :
            H[-1].go_R = True
            if H[-1].state is hero.hero.h_stand:
                H[-1].change_state(hero.hero.h_move)
            right_key_on = True
            left_key_on = False
        if (e.type, e.key) == (SDL_KEYUP, SDLK_w):
            up_key_on = False
            if H[-1].jump is True or H[-1].state != hero.hero.h_jump_ready:
                return
            H[-1].change_state(hero.hero.h_jump)
        if (e.type, e.key) == (SDL_KEYUP, SDLK_s):
            down_key_on = False
        if (e.type, e.key) == (SDL_KEYUP, SDLK_a):
            H[-1].go_L = False
            if (H[-1].go_L, H[-1].go_R) == (False, False):
                if H[-1].state is hero.hero.h_move:
                    H[-1].state = hero.hero.h_stand
                    H[-1].frame = 0
            left_key_on = False
        if (e.type, e.key) == (SDL_KEYUP, SDLK_d) :
            H[-1].go_R = False
            if (H[-1].go_L, H[-1].go_R) == (False, False):
                if H[-1].state is hero.hero.h_move:
                    H[-1].state = hero.hero.h_stand
                    H[-1].frame = 0
            right_key_on = False
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_k):
            H += [hero.hero(H[-1].x, H[-1].y, H[-1].state, H[-1].hp, H[-1].jump, H[-1].ascend, H[-1].attack_effect, \
                  H[-1].attack_type, H[-1].attack_frame, H[-1].go_L, H[-1].go_R, H[-1].look, H[-1].extra_hit_size_x, H[-1].extra_hit_size_y,\
                    H[-1].ate_depress, H[-1].maxheight, H[-1].extra_hit_time, H[-1].change_pics)]
            for he in H:
                if he is not H[-1]: he.overwhelming = True
            H[-2].del_time = time.time()
            H[-1].dash_dist = 30
            H[-1].dashing = True
            H[-1].dash_dir = 0
            H[-1].ascend = False
            if up_key_on is True:
                H[-1].dash_dir |= 1
            if down_key_on is True:
                H[-1].dash_dir |= 10
            if left_key_on is True:
                H[-1].dash_dir |= 100
            if right_key_on is True:
                H[-1].dash_dir |= 1000
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_q):
            tmp = selection
            next = max((selection - 1), 0)
            if tmp == next:selection = 2
            else:selection = next
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_e):
            tmp = selection
            next = min((selection + 1), 2)
            if tmp == next:selection = 0
            else:selection = next
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_p):
            if stop is True:
                stop = False
            else:
                stop = True
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_l):
            skill_inv[selection].handle_events()

def take_additional(max_fever):
    global skill_inv, H, E
    if skill_inv[0].locked == True and max_fever >= 5:
        skill_inv[0].unlock()
    if skill_inv[1].locked == True and max_fever >= 10:
        skill_inv[1].unlock()
    if skill_inv[2].locked == True and max_fever >= 15:
        skill_inv[2].unlock()

    H[-1].extra_damage = max_fever//2
    if len(E) is not 0:
        for e in E:
            e.speed = min(e.max_speed, e.max_speed - max_fever/10)

def update():
    global E, H, rev_state, fev
    global E_appear_speed, E_appear_time_ratio, Emax, stage_start_time, stage_elapsed_time
    global total_start, total_elapse, total_score, total_kills, total_stage
    global stage_state, phase
    global stage_term, stamp
    global shake
    global stop
    global cur_score, up_key_on
    global Item, Item_last_create_time, Item_create_time, Item_created
    global skill_inv, selection

    if stop is True:
        if len(H) is not 0:
            for he in H:
                he.time_set()
        if len(E) is not 0:
            for ene in E:
                ene.time_set()
        time_storage = stage_elapsed_time - stage_start_time
        stage_elapsed_time = time.time()
        total_start = stage_elapsed_time - total_elapse
        stage_start_time = stage_elapsed_time - time_storage
        time_storage = stage_elapsed_time - Item_last_create_time
        Item_last_create_time = stage_elapsed_time - time_storage
        return
    #업데이트 부분
    fev.update()
    for i in range(3):
        if skill_inv[i].locked == False and skill_inv[i].activated:
            skill_inv[i].update(H[-1], E, ground_y)
    if len(E) is not 0:
        for ene in E:
            ene.update(stage_state, H[-1])
            if len(H) is not 0:
                for h in H:
                    if h.del_sign is False:
                        ene.dst_attack = h
                        break
            if len(ene.attack_object) is not 0:
                for obj in ene.attack_object:
                    obj.update(ene)# 적 공격 오브젝트 이동 부분
    if len(Item) is not 0:
        for i in Item:
            i.update(H[-1], E, ground_y + 160)

    #del_sign에의한 삭제부분
    for i in range(len(E)):
        if E[i].del_sign is True:
            if E[i].state_elapsed_time - E[i].state_changed_time > 2:
                total_kills += 1
                total_score += E[i].lev * 100
                fev.fev += 1
                fev.rot_pos = 0
                E.pop(i)
                break

    if len(H) is not 0:
        if H[-1].hp < 0:
            score_state.score_storage = total_score
            score_state.kills_storage = total_kills
            game_framework.change_state(score_state)
            return
        for num in range(len(H)):
            if H[num - 1].del_sign is True:
                H.pop(num - 1)
                break
    if len(Item) is not 0:
        for i in range(len(Item)):
            if Item[i].del_sign is True:
                Item.pop(i)
                break
    take_additional(fev.max_fev)

    cur_score.update(total_score)

    stage_elapsed_time = time.time()
    if stage_state is stage_start:
        if stage_elapsed_time - stage_start_time >= E_appear_speed and len(E) < Emax:
            E_appear_speed += E_appear_time_ratio
            E += [enemy.enemy(H[-1], H[-1])]
        if stage_elapsed_time - stage_start_time >= stage_start:
            stage_start_time = time.time()
            stage_elapsed_time = time.time()
            stage_state = stage_pass
            phase += [phrase(stage_pass)]
            stage_term = load_image('../Pics/vacant_bar2.png')
            stamp = load_image('../Pics/enemy_stamp.png')
        if stage_elapsed_time - Item_last_create_time > Item_create_time and Item_created is False:
            Item_created = True
            Item += [item.item(random.randint(1, 3))]
            Item_last_create_time = time.time()

    if stage_state is stage_pass:
        if stage_elapsed_time - stage_start_time >= stage_pass:
            stage_start_time = time.time()
            stage_elapsed_time = time.time()
            stage_state = stage_start
            phase += [phrase(stage_start)]
            E_appear_time_ratio -= 0.05
            E_appear_speed = E_appear_time_ratio
            stage_term = load_image('../Pics/vacant_bar.png')
            stamp = load_image('../Pics/hero_stamp.png')
            H[-1].hp += 5
            H[-1].max_hp += 5
            enemy.enemy.max_hp *= 1.5
            Emax += 10
            total_stage += 1
            Item_last_create_time = time.time()
            Item_create_time = random.randint(0, stage_start)
            Item_created = False

    total_elapse = stage_elapsed_time - total_start
    total_score += H[-1].update(E)
    print('heroY, heroMinheight : ', H[-1].y, ground_y)
    hero.hero.h_minheight = ground_y + 150
    move_bg_by_hero(H[-1])
    rev_state = H[-1].change_pics
    shake.give_shake()
    shake.shake()

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