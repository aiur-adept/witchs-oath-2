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
        logger.info(f'ac_seed_pos: {ac_seed_pos}')
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

def connect_rooms(rects):
    return rects

def write_floorplan(rects, m):
    def in_map(x, y):
        return x >= 0 and x < MAGIC_MAP_W and y >= 0 and y < MAGIC_MAP_H

    for rect in rects:
        x0 = rect[0]
        y0 = rect[1]
        w = rect[2]
        h = rect[3]
        logger.info(f'writing rect {rect}')
        for j in range(0, h):
            for i in range(0, w):
                if in_map(x0 + i, y0 + j):
                    m[y0 + j][x0 + i] = 0

def gen_map(state):
    """
    build the rooms the world is made of; inspired by method from:
    https://www.reddit.com/r/roguelikedev/comments/552hd5/comment/d870l0v/ 
    """
    for _, cardinal in enumerate(connection_spec):
        m = state['map'][cardinal]
        logger.info(f'===floorplan in {cardinal}...')
        rects = gen_antechambers(cardinal) + gen_random_rects()
        logger.info('rects:')
        logger.info(rects)
        rects_final = connect_rooms(rects)
        write_floorplan(rects_final, m)
        logger.info('---/floorplan')

def gen_world(state):
    """
    populate the world with entities
    """
    pass

