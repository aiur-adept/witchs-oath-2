"""
Witch's Oath 2
by Nicole Hunter
Autumn 2026
"""
import curses
import time

import locale
locale.setlocale(locale.LC_ALL, '') 

import logging
logger = logging.getLogger(__name__)

import os
import sys

from generation import (
        connection_spec,
        gen_map, 
        gen_world
)
from constants import (
        INPUT_HYST_S,
        MAGIC_MAP_W, 
        MAGIC_MAP_H
)
import entities
from nobles import (
        dialog_noble
)
from util import (
        in_rect
)
from colors import init_colors
from incantations import incant
from render import (
        render_map,
        render_entities
)

# color fix for windows from
# https://www.reddit.com/r/learnpython/comments/1awa6mj/curses_color_reset_or_curses_foiled_again/
# Force Windows 11 Virtual Terminal (ANSI Color) processing on
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    # -11 is the constant for STD_OUTPUT_HANDLE
    # 7 enables ENABLE_PROCESSED_OUTPUT, ENABLE_WRAP_AT_EOL_OUTPUT, and ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)



def player_movement(stdscr, state, key):
    def collides_noble(p):
        if state['player']['setting'] != 'C':
            return None
        for _, nid in enumerate(state['world']['nobles']):
            npos = state['world']['nobles'][nid]['position']
            if p[0] == npos[0] and p[1] == npos[1]:
                return nid
        return None
    def space_free(p):
        empty = (state['map'][state['player']['setting']][p[1]][p[0]] == 0)
        return (empty and (collides_noble(p) is None))
    def in_antechamber(p):
        setting = state['player']['setting']
        for ac in state['world']['antechambers'][setting]:
            if in_rect(p, ac):
                return True
        return False
    def leave_direction(new_pos):
        if new_pos[1] <= 0:
            return 'N'
        elif new_pos[1] >= MAGIC_MAP_H-1:
            return 'S'
        elif new_pos[0] <= 0:
            return 'W'
        elif new_pos[0] >= MAGIC_MAP_W-1:
            return 'E'
        else:
            return None
    def pos_enter_from(leave):
        if leave == 'N':
            return [MAGIC_MAP_W//2, MAGIC_MAP_H-1]
        elif leave == 'S':
            return [MAGIC_MAP_W//2, 0]
        elif leave == 'W':
            return [MAGIC_MAP_W-1, MAGIC_MAP_H//2]
        elif leave == 'E':
            return [0, MAGIC_MAP_H//2]

    # calculate new position
    new_pos = [state['player']['position'][0], 
               state['player']['position'][1]]
    if key == curses.KEY_UP:
        new_pos[1] += -1
    elif key == curses.KEY_DOWN:
        new_pos[1] += 1
    elif key == curses.KEY_LEFT:
        new_pos[0] += -1
    elif key == curses.KEY_RIGHT:
        new_pos[0] += 1
    new_pos[0] = max(0, min(MAGIC_MAP_W - 1, new_pos[0]))
    new_pos[1] = max(0, min(MAGIC_MAP_H - 1, new_pos[1]))
    # collide with nobles to talk
    collided_nid = collides_noble(new_pos)
    if collided_nid is not None:
        dialog_noble(stdscr, state, collided_nid)
    # leave to another map
    leave = leave_direction(new_pos)
    in_ac = in_antechamber(state['player']['position'])
    if in_ac and leave is not None:
        setting = state['player']['setting']
        state['player']['setting'] = connection_spec[setting][leave]
        state['player']['position'] = pos_enter_from(leave)
        return
    # finally, simply move if no special handling taken
    if space_free(new_pos): 
        state['player']['position'] = new_pos

def player_action(stdscr, state, key):
    if key in [ord('q'), ord('w'), ord('e')]:
        incant(stdscr, state, key)

def init_state(state):
    state['player'] = {
            'position': [MAGIC_MAP_W//2, MAGIC_MAP_H//2],
            'setting': 'C'
    }
    state['world'] = {}
    state['map'] = {
        'C': [[1] * MAGIC_MAP_W for _ in range(MAGIC_MAP_H)],
        'N': [[1] * MAGIC_MAP_W for _ in range(MAGIC_MAP_H)],
        'S': [[1] * MAGIC_MAP_W for _ in range(MAGIC_MAP_H)],
        'W': [[1] * MAGIC_MAP_W for _ in range(MAGIC_MAP_H)],
        'E': [[1] * MAGIC_MAP_W for _ in range(MAGIC_MAP_H)]
    }
    gen_map(state)
    gen_world(state)

def game(stdscr, state):
    stdscr.clear()
    stdscr.resize(MAGIC_MAP_H+2, MAGIC_MAP_W+2)

    init_state(state)

    last_input_time = 0
    last_input = -1
    while True:
        # render world
        stdscr.box('|', '-')
        render_map(stdscr, state)
        render_entities(stdscr, state)
        stdscr.refresh()

        # get input
        key = stdscr.getch()
        current_time = time.time()
        if current_time - last_input_time >= INPUT_HYST_S:
            if last_input != -1 and key == -1:
                key = last_input
            player_movement(stdscr, state, key)
            player_action(stdscr, state, key)
            last_input_time = current_time
            last_input = -1
        else:
            last_input = key

    return postgame, state

def postgame(stdscr, state):
    return None, state

def about(stdscr, state):
    stdscr.clear()
    stdscr.addstr(0, 0, "--- ABOUT WITCH'S OATH 2 ---", curses.A_UNDERLINE)
    about_str = """
    Witch's Oath 2 is a game meant to be played in a single 
    sitting using a terminal and the arrow keys plus Q, W, E (Incantation 
    keys). 

    The story of the game is that of a Witch on a pilgrimage
    through four decaying wastelands to rebuild a temple created before the
    proliferation of the dreaded wiremites. She will encounter monstrous 
    Dangers, decaying souls trapped in bodies that have become wiremite 
    hives, whom she may to return to peace using Incantations. 
    She will meet Nobles and Birds along the way who will aid her. 
    It is possible to find Rings as well. Each playthrough will be shuffled,
    as a deck of cards.

    The game represents a radical break in developmental philosophy from
    Witch's Oath, the digital card game by the same author, making use of
    only traditional, handcrafted coding methods guided by stackoverflow 
    and documentation. Although the game took longer to produce and
    is less flashy, the author hoped to regain her soul.

    Press any key to return to main menu.
    """
    for i, line in enumerate(about_str.split('\n')):
        stdscr.addstr(i+1, 0, line)
    stdscr.refresh()
    stdscr.getch()
    return main_menu, state
   
def main_menu(stdscr, state):
    options = ["Start Game", "About", "Exit"]
    selected_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "--- WITCH'S OATH 2 ---", curses.A_UNDERLINE)

        for i, option in enumerate(options):
            if i == selected_row:
                # Highlight the selected item
                stdscr.addstr(i + 2, 2, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 2, f"  {option}")

        stdscr.refresh()

        # Read user key input
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(options) - 1:
            selected_row += 1
        elif key in [10, 13]: # Enter Key codes
            stdscr.refresh()
            if selected_row == 0: # Start Game option
                return game, state
            elif selected_row == 1: # About option
                return about, state
            elif selected_row == 2: # Exit option
                return None, state

def entrypoint(stdscr):
    # Hide the blinking cursor
    curses.curs_set(0)
    # Enable special keyboard inputs (like arrow keys)
    stdscr.keypad(True)

    # define colors
    init_colors()

    # game state
    state = {}
    next_scene, state = main_menu(stdscr, state)
    # main loop
    while True:
       next_next_scene, state = next_scene(stdscr, state)
       next_scene = next_next_scene
       if next_scene == None:
           break

def main():
    # set up logging
    logging.basicConfig(filename='WO.log', level=logging.INFO) 
    # entrypoint
    curses.wrapper(entrypoint)

if __name__ == '__main__':
    main()
