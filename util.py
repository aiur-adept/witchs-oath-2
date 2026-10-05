import random

from constants import (
        MAGIC_MAP_W,
        MAGIC_MAP_H
)
import entities
from nobles import (
        TRSS_ID
)



def in_rect(p, r):
    return p[0] >= r[0] and \
            p[0] < (r[0] + r[2]) and \
            p[1] >= r[1] and \
            p[1] < (r[1] + r[3])

# NOTE: this is inefficient for sure, we ought to cache this per cardinal...
def random_valid_position(state, cardinal):
    # gen list of valid positions
    valid_positions = []
    for y in range(10, MAGIC_MAP_H-10):
        for x in range(10, MAGIC_MAP_W-10):
            if state['map'][cardinal][y][x] == entities.EMPTY_SPACE:
                valid_positions.append([x, y])
    # pick one randomly
    return random.choice(valid_positions)

def near_trss(state):
    trss = state['world']['C']['nobles'][TRSS_ID]
    tp = trss['position']
    witch = state['player']
    p = witch['position']
    dy = abs(tp[1] - p[1])
    dx = abs(tp[0] - p[0])
    return (dx <= 4 and dy <= 4)
