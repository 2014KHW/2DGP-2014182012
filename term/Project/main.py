import menu_state
import play_state
import score_state
import game_framework
from pico2d import *

open_canvas()
game_framework.run(menu_state)
close_canvas()