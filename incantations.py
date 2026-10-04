import curses
import time

from entities import (
        displays,
        Q_INCANT,
        W_INCANT,
        E_INCANT
)
from colors import (
        COLORS_Q_INCANT,
        COLORS_W_INCANT,
        COLORS_E_INCANT
)
from render import (
        render_entities
)
from wiremites import (
        return_wiremite_to_peace
)


incant_map = {
    ord('q'): {
        'symbol': displays[Q_INCANT],
        'color': COLORS_Q_INCANT
    },
    ord('w'): {
        'symbol': displays[W_INCANT],
        'color': COLORS_W_INCANT
    },
    ord('e'): {
        'symbol': displays[E_INCANT],
        'color': COLORS_E_INCANT
    },
}

def animate_incant(stdscr, state, p, key):
    symbol = incant_map[key]['symbol']
    color = incant_map[key]['color']
    for i in range(0, 6):
        if (i % 2) == 0:
            for dy in range(-3, 2):
                stdscr.addstr(p[1]-dy, p[0]-1, 
                              symbol*5, curses.color_pair(color)),
        else:
            render_entities(stdscr, state) 
        stdscr.refresh()
        time.sleep(0.1)

def incant_effect(stdscr, state, p, key):
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
    dx = abs(wmpos[0] - ppos[0])
    dy = abs(wmpos[1] - ppos[1])
    if (dx <= 2 or dy <= 2) and wm_here['weakness'] == key:
        return_wiremite_to_peace(stdscr, state, wm_here) 

def incant(stdscr, state, key):
    # display and animate the incantation before continuing
    animate_incant(stdscr, state, state['player']['position'], key)
    # affect state 
    incant_effect(stdscr, state, 
                  state['player']['position'], 
                  key)
    

