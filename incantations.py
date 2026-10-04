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
            for dy in range(-2, 1):
                stdscr.addstr(p[1]-dy, p[0], 
                              symbol*3, curses.color_pair(color)),
        else:
            render_entities(stdscr, state) 
        stdscr.refresh()
        time.sleep(0.1)

def incant_effect(state, p, key):
    # TODO: characteristic effects on game state of each incantation
    pass

def incant(stdscr, state, key):
    # display and animate the incantation before continuing
    animate_incant(stdscr, state, state['player']['position'], key)
    # affect state 
    incant_effect(state, 
                  state['player']['position'], 
                  key)
    

