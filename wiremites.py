import random

from colors import (
        COLORS_Q_INCANT,
        COLORS_W_INCANT,
        COLORS_E_INCANT
)
from util import (
        random_valid_position
)
from dialog import (
        dialog_flow
)
from nobles import (
        RNDRR_ID,
        SNDRR_ID,
        INDRR_ID,
        spawn_rescued_noble
)



wiremites_spec = [
    {
        'name': 'wiremite of emanation',
        'weakness': ord('q'),
        'color': COLORS_Q_INCANT,
        'cardinal': 'N',
        'true_identity': RNDRR_ID,
        'confers': 'saved_rndrr'
    },
    {
        'name': 'wiremite of occultation',
        'weakness': ord('w'),
        'color': COLORS_W_INCANT,
        'cardinal': 'S',
        'true_identity': SNDRR_ID,
        'confers': 'saved_sndrr'
    },
    {
        'name': 'wiremite of annihilation',
        'weakness': ord('e'),
        'color': COLORS_E_INCANT,
        'cardinal': 'W',
        'true_identity': INDRR_ID,
        'confers': 'saved_indrr'
    }
]

def gen_wiremites(state):
    # spawn wiremites in cardinal dungeons
    state['world']['wiremites'] = []
    for spec in wiremites_spec:
        wm = spec.copy()
        wm['position'] = random_valid_position(state, spec['cardinal'])
        state['world']['wiremites'].append(wm)

def random_wiremite_msgs(wm):
    def randomstr():
        s = ''
        for i in range(0, 5): 
            word = ''
            for i in range(0, random.randint(2,6)):
                word += chr(random.randint(ord('a'), ord('z')+1))
            s += word + ' ' 
        return s

    return [f"[you are touched by the {wm['name']}...]",
            'it cries out to you:',
            randomstr(),
            randomstr(),
            randomstr() + '!!!']

def dialog_wiremite(stdscr, state, wm):
    dialog_flow(stdscr, random_wiremite_msgs(wm))
    # warp to random position in cardinal
    randpos = random_valid_position(state, state['player']['setting'])
    state['player']['position'] = randpos

def return_wiremite_to_peace(stdscr, state, wm):
    state['world']['wiremites'].remove(wm)
    spawn_rescued_noble(state, wm['true_identity'])
    dialog_flow(stdscr, [f"[You have returned the {wm['name']} to peace.]"])
    state['player'][wm['confers']] = True
