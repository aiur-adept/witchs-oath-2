"""
Witch's Oath 2
by Nicole Hunter
Autumn 2026
"""
import random
import constants
import logging

logger = logging.getLogger(__name__)

from constants import (
        MAGIC_MAP_W,
        MAGIC_MAP_H,
        RECTS_PER_MAP,
        ROOM_SCALE,
        MIDDLE_ROOM_DIMENSION,
        MAP_EDGE_CLEAR,
        N_TEMPLE_PIECES
)

from nobles import (
        gen_cardinal_nobles
)

from wiremites import (
        gen_wiremites
)

import entities

from util import (
        random_valid_position
)

# determining which cardinals connect to which other cardinals, and where
# (positions of antechambers as ratios of w,h)
directions = {
    'N': [0.5, 0.0],
    'S': [0.5, 1.0],
    'W': [0.0, 0.5],
    'E': [1.0, 0.5]
}
connection_spec = {
    'C': {
        'N': 'N',
        'S': 'S',
        'W': 'W',
        'E': 'E'
    },
    'N': { 
        'S': 'C'
    },
    'S': { 
        'N': 'C'
    },
    'W': {
        'E': 'C'
    },
    'E': {
        'W': 'C'
    }
}

def in_map(x, y):
    return x >= 0 and x < MAGIC_MAP_W and y >= 0 and y < MAGIC_MAP_H

def spec_to_seed_pos(spec):
    return [
            int(constants.MAGIC_MAP_W * spec[0]),
            int(constants.MAGIC_MAP_H * spec[1]),
    ]

def expand_rect(rect, n):
    for i in range(0, n):
        rect[0] -= 1
        rect[1] -= 1
        rect[2] += 2
        rect[3] += 2
    return rect

def gen_antechambers(cardinal):
    antechambers = []
    for _, connect in enumerate(connection_spec[cardinal]):
        ac_seed_pos = spec_to_seed_pos(directions[connect])
        ac_rect = [ac_seed_pos[0], ac_seed_pos[1], 1, 1]
        antechamber = expand_rect(ac_rect, 3)
        antechambers.append(antechamber)
    return antechambers

def gen_random_rects():
    def rand_rect():
        return [
            random.randint(MAP_EDGE_CLEAR, MAGIC_MAP_W - MAP_EDGE_CLEAR - ROOM_SCALE//2),
            random.randint(MAP_EDGE_CLEAR, MAGIC_MAP_H - MAP_EDGE_CLEAR - ROOM_SCALE//2),
            random.randint(4, ROOM_SCALE),
            random.randint(4, ROOM_SCALE)
        ]
        
    rects = []
    for i in range(0, RECTS_PER_MAP):
        rects.append(rand_rect())
    return rects

def central_point(r):
    return [r[0]+r[2]//2, r[1]+r[3]//2]

def write_hallway(r1, r2, m):
    def room_delta(r1, r2):
        c1 = central_point(r1)
        c2 = central_point(r2)
        dx = c2[0] - c1[0]
        dy = c2[1] - c1[1]
        return [dx, dy]

    d = room_delta(r1, r2)
    src = central_point(r1)
    dest = central_point(r2) 
    p = [src[0], src[1]]
    # iterate horizontal distance 
    for x in range(src[0], src[0]+d[0], (-1 if d[0] < 0 else 1)):
        if in_map(x, p[1]):
            m[p[1]][x] = 0
    # we are now horizontally-aligned
    p[0] = dest[0]
    # iterate vertical distance
    for y in range(src[1], src[1]+d[1], (-1 if d[1] < 0 else 1)):
        if in_map(p[0], y):
            m[y][p[0]] = 0
        

def write_floorplan(rects, m):
    for rect in rects:
        x0 = rect[0]
        y0 = rect[1]
        w = rect[2]
        h = rect[3]
        for j in range(0, h):
            for i in range(0, w):
                if in_map(x0 + i, y0 + j):
                    m[y0 + j][x0 + i] = 0

def gen_map(state):
    state['world']['antechambers'] = {}
    for _, cardinal in enumerate(connection_spec):
        m = state['map'][cardinal]
        middle = [MAGIC_MAP_W//2 - MIDDLE_ROOM_DIMENSION, 
                  MAGIC_MAP_H//2 - MIDDLE_ROOM_DIMENSION, 
                  18, 
                  18]
        acs = gen_antechambers(cardinal) 
        randoms = gen_random_rects() 
        write_floorplan(acs + randoms + [middle], m)
        for ac in acs:
            write_hallway(ac, middle, m)
        for r in randoms:
            write_hallway(r, middle, m)
        for i in range(0, len(randoms)):
            for j in range(i, len(randoms)):
                write_hallway(randoms[i], randoms[j], m)
        state['world']['antechambers'][cardinal] = acs

def spawn_item(state, entity, cardinal):
    pos = random_valid_position(state, cardinal)
    state['map'][cardinal][pos[1]][pos[0]] = entity

def gen_items(state):
    # gen Trss's ring (east)
    spawn_item(state, entities.TRSS_RING, 'E')
    # gen Trss's hat (west)
    spawn_item(state, entities.TRSS_HAT, 'W')
    # gen health bottle (south)
    spawn_item(state, entities.HEALTH_BOTTLE, 'S')
    # gen unknown ring (east)
    spawn_item(state, entities.UNKNOWN_RING, 'E')
    # gen temple pieces
    for i in range(0, N_TEMPLE_PIECES):
        cardinal = random.choice(['N', 'S', 'W', 'E'])
        spawn_item(state, entities.TEMPLE_PIECE, cardinal)

def gen_world(state):
    """
    populate the world with entities
    """
    # set up world scoping
    for _, cardinal in enumerate(connection_spec):
        state['world'][cardinal] = {}
    # generate nobles in central
    gen_cardinal_nobles(state)
    # gen items
    gen_items(state)
    # gen wiremites
    gen_wiremites(state)


