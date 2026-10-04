from colors import (
        COLORS_Q_INCANT,
        COLORS_W_INCANT,
        COLORS_E_INCANT
)
from util import (
    random_valid_position
)

wiremites_spec = [
    {
        'name': 'wiremite of emanation',
        'weakness': ord('q'),
        'color': COLORS_Q_INCANT,
        'cardinal': 'N'
    },
    {
        'name': 'wiremite of occultation',
        'weakness': ord('w'),
        'color': COLORS_W_INCANT,
        'cardinal': 'W'
    },
    {
        'name': 'wiremite of annihilation',
        'weakness': ord('e'),
        'color': COLORS_E_INCANT,
        'cardinal': 'S'
    }
]

def gen_wiremites(state):
    # spawn wiremites in cardinal dungeons
    state['world']['wiremites'] = []
    for spec in wiremites_spec:
        wm = spec.copy()
        wm['position'] = random_valid_position(state, spec['cardinal'])
        state['world']['wiremites'].append(wm)

