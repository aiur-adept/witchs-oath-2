import random

from constants import (
        MAGIC_MAP_W,
        MAGIC_MAP_H
)
import entities



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

