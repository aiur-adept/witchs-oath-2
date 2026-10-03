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
        ROOM_SCALE
)

# determining which maps connect to which other maps, and where
# (positions of antechambers as ratios of w,h)
connection_spec = {
    'C': {
        'N': [0.5, 0.0],
        'S': [0.5, 1.0],
        'W': [0.0, 0.5],
        'E': [1.0, 0.5]
    },
    'N': { 
        'C': [0.5, 1.0],
    },
    'S': { 
        'C': [0.5, 0.0],
    },
    'W': {
        'C': [1.0, 0.5]
    },
    'E': {
        'C': [0.0, 0.5],
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
        ac_seed_pos = spec_to_seed_pos(connection_spec[cardinal][connect])
        ac_rect = [ac_seed_pos[0], ac_seed_pos[1], 1, 1]
        antechamber = expand_rect(ac_rect, 3)
        antechambers.append(antechamber)
    return antechambers

def gen_random_rects():
    def rand_rect():
        return [
            random.randint(0, MAGIC_MAP_W),
            random.randint(0, MAGIC_MAP_H),
            random.randint(4, ROOM_SCALE),
            random.randint(4, ROOM_SCALE)
        ]
        
    rects = []
    for i in range(0, RECTS_PER_MAP):
        rects.append(rand_rect())
    return rects


def write_hallways(rects, m):
    def central_point(r):
        return [r[0]+r[2]//2, r[1]+r[3]//2]
    def room_delta(r1, r2):
        c1 = central_point(r1)
        c2 = central_point(r2)
        dx = c2[0] - c1[0]
        dy = c2[1] - c1[1]
        return [dx, dy]
    def write_L_connector(r1, r2):
        d = room_delta(r1, r2)
        src = central_point(r1)
        dest = central_point(r2) 
        p = src
        # iterate horizontal distance 
        for x in range(r1[0], r1[0]+d[0], (-1 if d[0] < 0 else 1)):
            if in_map(p[0] + x, p[1]):
                m[p[1]][x] = 0
        # we are now horizontally-aligned
        p[0] = dest[0]
        # iterate vertical distance
        for y in range(r1[1], r1[1]+d[1], (-1 if d[1] < 0 else 1)):
            if in_map(p[0], p[1]+y):
                m[y][p[0]] = 0
    for i in range(0, len(rects)):
        for j in range(i+1, len(rects)):
            write_L_connector(rects[i], rects[j])
        

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
    for _, cardinal in enumerate(connection_spec):
        m = state['map'][cardinal]
        central_room = [MAGIC_MAP_W//2-9, MAGIC_MAP_H//2-9, 18, 18]
        rects = gen_antechambers(cardinal) + gen_random_rects() + [central_room]
        write_floorplan(rects, m)
        write_hallways(rects, m)

def gen_world(state):
    """
    populate the world with entities
    """
    pass

