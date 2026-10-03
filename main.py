"""
Witch's Oath 2
by Nicole Hunter
Autumn 2026
"""
import curses
import time
import logging

logger = logging.getLogger(__name__)

import os
import sys

from generation import gen_map, gen_world
from constants import (
        INPUT_HYST_S,
        MAGIC_MAP_W, 
        MAGIC_MAP_H
)
import entities

# color fix for windows from
# https://www.reddit.com/r/learnpython/comments/1awa6mj/curses_color_reset_or_curses_foiled_again/
# Force Windows 11 Virtual Terminal (ANSI Color) processing on
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    # -11 is the constant for STD_OUTPUT_HANDLE
    # 7 enables ENABLE_PROCESSED_OUTPUT, ENABLE_WRAP_AT_EOL_OUTPUT, and ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)



def render_map(stdscr, state):
    m = state['map'][state['player']['setting']]
    for y, row in enumerate(m):
        for x, e in enumerate(row):
            stdscr.addstr(y+1, x+1, entities.displays[e])

def render_entities(stdscr, state):
    # render incants
    # TODO
    # render other entities
    # TODO
    # render player
    player = state['player']
    stdscr.addstr(player['position'][1], 
                  player['position'][0], 
                  entities.displays[entities.WITCH],
                  curses.color_pair(2))

def player_movement(state, key):
    if key == curses.KEY_UP:
        state['player']['position'][1] += -1
    elif key == curses.KEY_DOWN:
        state['player']['position'][1] += 1
    elif key == curses.KEY_LEFT:
        state['player']['position'][0] += -1
    elif key == curses.KEY_RIGHT:
        state['player']['position'][0] += 1
    state['player']['position'][0] = max(1, 
                                        min(MAGIC_MAP_W, 
                                        state['player']['position'][0]))
    state['player']['position'][1] = max(1, 
                                        min(MAGIC_MAP_H, 
                                        state['player']['position'][1]))

def player_action(state, key):
    pass

def game(stdscr, state):
    stdscr.clear()
    stdscr.resize(MAGIC_MAP_H+2, MAGIC_MAP_W+2)

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
            player_movement(state, key)
            player_action(state, key)
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
    # set up curses
    stdscr = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    # entrypoint
    entrypoint(stdscr)

if __name__ == '__main__':
    main()
