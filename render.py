import curses

import entities
from colors import (
        COLORS_NOBLES,
        COLORS_PLAYER
)

def render_map(stdscr, state):
    curses.color_pair(0)
    m = state['map'][state['player']['setting']]
    for y, row in enumerate(m):
        for x, e in enumerate(row):
            stdscr.addstr(y+1, x+1, entities.displays[e])

def render_world_entities(stdscr, state):
    cardinal = state['player']['setting']
    w = state['world']
    # render other entities
    # TODO
    # special-symbol central nobles
    if cardinal == 'C':
        for _, nid in enumerate(w['C']['nobles']):
            noble = w['C']['nobles'][nid]
            stdscr.addstr(noble['position'][1]+1,
                          noble['position'][0]+1,
                          noble['symbol'],
                          curses.color_pair(COLORS_NOBLES))


def render_entities(stdscr, state):
    render_world_entities(stdscr, state)
    # render player
    player = state['player']
    stdscr.addstr(player['position'][1]+1, 
                  player['position'][0]+1, 
                  entities.displays[entities.WITCH],
                  curses.color_pair(COLORS_PLAYER))

