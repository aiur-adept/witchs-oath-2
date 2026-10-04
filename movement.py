import curses
import random

from generation import (
        connection_spec
)
from constants import (
        MAGIC_MAP_W, 
        MAGIC_MAP_H
)
from util import (
        in_rect
)
from nobles import (
        dialog_noble
)
import entities
from items import (
        pick_up_item
)
from wiremites import (
        dialog_wiremite
)

def collides_wiremite(state, p):
    if state['player']['setting'] == 'C':
        return None
    cardinal = state['player']['setting']
    wm_result = list(filter(lambda wm: wm['cardinal'] == cardinal, 
                     state['world']['wiremites']))
    if len(wm_result) == 0:
        return
    wm_here = wm_result[0]
    wmpos = wm_here['position']
    if p[0] == wmpos[0] and p[1] == wmpos[1]:
        return wm_here
    return None

def collides_item(state, p):
    cardinal = state['player']['setting']
    candidate = state['map'][cardinal][p[1]][p[0]]
    return candidate if entities.is_item(candidate) else None

def collides_noble(state, p):
    if state['player']['setting'] != 'C':
        return None
    for _, nid in enumerate(state['world']['C']['nobles']):
        npos = state['world']['C']['nobles'][nid]['position']
        if p[0] == npos[0] and p[1] == npos[1]:
            return nid
    return None

def space_free(state, p):
    empty = (state['map'][state['player']['setting']][p[1]][p[0]] == 0)
    return (empty and \
            (collides_noble(state, p) is None) and \
            (collides_wiremite(state, p) is None))

def in_antechamber(state, p):
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

def check_collision(stdscr, state, new_pos):
    # noble collision
    collided_nid = collides_noble(state, new_pos)
    if collided_nid is not None:
        dialog_noble(stdscr, state, collided_nid)
    # item collision
    collided_item = collides_item(state, new_pos)
    if collided_item is not None:
        pick_up_item(stdscr, state, collided_item, new_pos)
    # wiremite collision
    collided_wiremite = collides_wiremite(state, new_pos)
    if collided_wiremite is not None:
        dialog_wiremite(stdscr, state, collided_wiremite)

def player_movement(stdscr, state, key): 
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
    # collide with nobles to talk, wiremites to be hurt
    check_collision(stdscr, state, new_pos)
    # leave to another cardinal
    leave = leave_direction(new_pos)
    in_ac = in_antechamber(state, state['player']['position'])
    if in_ac and leave is not None:
        setting = state['player']['setting']
        state['player']['setting'] = connection_spec[setting][leave]
        state['player']['position'] = pos_enter_from(leave)
        return
    # finally, simply move if no special handling taken
    if space_free(state, new_pos): 
        state['player']['position'] = new_pos

def wiremite_movement(stdscr, state):
    if state['player']['setting'] == 'C':
        return None
    cardinal = state['player']['setting']
    wm_result = list(filter(lambda wm: wm['cardinal'] == cardinal, 
                     state['world']['wiremites']))
    if len(wm_result) == 0:
        return
    wm_here = wm_result[0]
    wmpos = wm_here['position']
    ppos = state['player']['position']
    dx = 1 if wmpos[0] < ppos[0] else (-1 if wmpos[0] > ppos[0] else 0)
    dy = 1 if wmpos[1] < ppos[1] else (-1 if wmpos[1] > ppos[1] else 0)
    choice = random.randint(0,2)
    if choice == 0:
        wm_here['position'][0] += dx
    else:
        wm_here['position'][1] += dy
