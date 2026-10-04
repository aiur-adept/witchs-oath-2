from dialog import (
        dialog_flow 
)
from constants import (
        MAGIC_MAP_W,
        MAGIC_MAP_H,
        MIDDLE_ROOM_DIMENSION,
        N_TEMPLE_PIECES
)



# cardinal 4 nobles
QMRSK_ID = 0
WMRSK_ID = 1
EMRSK_ID = 2
TRSS_ID  = 3
# rescuable nobles
RNDRR_ID = 4
SNDRR_ID = 5
INDRR_ID = 6

rescuable_noble_spec = {
    RNDRR_ID: {
        'name': 'Rndrr, Noble of Incantation',
        'symbol': 'R',
        'position': [
            MAGIC_MAP_W//2,
            MAGIC_MAP_H//2 - MIDDLE_ROOM_DIMENSION//2 - 1,
        ]
    },
    SNDRR_ID: {
        'name': 'Sndrr, Noble of Incantation',
        'symbol': 'S',
        'position': [
            MAGIC_MAP_W//2,
            MAGIC_MAP_H//2 + MIDDLE_ROOM_DIMENSION//2 + 1
        ]
    },
    INDRR_ID: {
        'name': 'Indrr, Noble of Incantation',
        'symbol': 'I',
        'position': [
            MAGIC_MAP_W//2 - MIDDLE_ROOM_DIMENSION//2 - 1,
            MAGIC_MAP_H//2
        ]
    }
}

qmrsk_plea = [
    "[You look upon Qmrsk, Scion of Emanation, a man of candlelight]",
    "[Qmrsk speaks to you, his voice as a flickering of light]",
    "Emanation was the school of light, creation, and boundless hope.",
    "And it was with the Kindled Flame that we helped create them,",
    "The wiremites...",
    "It is said that the school of emanation partakes of each other.",
    "Do not be so quick to judge, Traveller.",
    "The incantation [Q], ah yes, I learned it long ago...",
    "It will return them to peace. My friend for instance...",
    "But I shall say no more."
]
qmrsk_thanks = [
    "[You look upon Qmrsk, Scion of Emanation, a man of candlelight]",
    "[Qmrsk speaks to you, his voice as a flickering of light]",
    "Many illuminations to you, Traveller. My friend is returned.",
    "I can ask for no more. I wish only that you may also...",
    "I shall say no more."
]
wmrsk_plea = [
    "[You look upon Wmrsk, Scion of Occultation, a man of shadows]",
    "[Wmrsk speaks to you, his voice as a deepening of shadow]",
    "O Traveller...",
    "Seek not the way to the south...",
    "Lest ye too...",
    "Enter occultation...",
    "O woe... O annihilation... What hast thou wrought...",
    "O Traveller...",
    "[W], the incantation of Occultation... for the wiremites...",
    "Perchance... shall thee seek my sister...? But no...",
    "Thou art in occultation as well...",
    "I shall speak no more..."
]
wmrsk_thanks = [
    "[You look upon Wmrsk, Scion of Occultation, a man of shadows]",
    "[Wmrsk speaks to you, his voice as a deepening of shadow]",
    "O Traveller...",
    "The time of occultation has ended for my sister Sndrr...",
    "Yet...",
    "There is yet much to do...",
    "Hurry, find the pieces of temple...",
    "Hurry..."
]
emrsk_plea = [
    "[You look upon Emrsk, Scion of Annihilation, a man of flames]",
    "[Emrsk speaks to you, his voice as a crackle of cinders]",
    "O Traveller, in another life, I would annihilate you,",
    "Merely for having come to this place, yet that time is gone,",
    "For Trss had spent her last tears to return us to peace.",
    "Truly, the incantation [E] is an incantation of annihilation,",
    "Suitable for returning wiremites of annihilation (red).",
    "Find my brother to the west, and return him.",
    "He will offer aid. I shall speak no more. Be gone."
]
emrsk_thanks = [
    "[You look upon Emrsk, Scion of Annihilation, a man of flames]",
    "[Emrsk speaks to you, his voice as a crackle of cinders]",
    "O Traveller, my flames kindle to see my brother Indrr again.",
    "So much so that I consider, whether annihilation is not...",
    "In some way responsible... It was our school that... well...",
    "I shall say no more. But you are in my thanks."
]
trss_plea = [
    "[You look upon Trss, Noble of Power, a woman of fine silk]",
    "[Trss speaks to you, her voice as a silver drop of moonlight]",
    "O Traveller of incantation's warp and weft",
    "You find us here bereaved, of hope bereft...",
    "Assemble thou the pieces of the temple found", 
    "Completing in thy pilgrimage the round...",
    "In each direction cardinal embark",
    "Beware the wiremites who hunger, hark!",
    "My tale's a weary one of woe to tell,",
    "I'll tell it at the journey's end, and well."
]
trss_penultimate = [
    "Swiftly take the pieces of the temple in your hands,",
    "You have them all, incant [T] before me, it shall stand."
]

noble_dialogs = {
        QMRSK_ID: lambda state: qmrsk_plea if not state['player']['saved_rndrr'] else qmrsk_thanks,
        WMRSK_ID: lambda state: wmrsk_plea if not state['player']['saved_sndrr'] else wmrsk_thanks,
        EMRSK_ID: lambda state: emrsk_plea if not state['player']['saved_indrr'] else emrsk_thanks,
        TRSS_ID: lambda state: trss_plea if state['player']['temple_pieces_count'] < N_TEMPLE_PIECES else trss_penultimate,
        RNDRR_ID: lambda state: [
            "[You look upon Rndrr, Friend of Qmrsk, a man of learning.]",
            "[Rndrr speaks to you, his voice a flipping of pages]",
            "O Traveller, blessed art thou! Although...",
            "I know too much. Forgive me. I shall say no more."
        ],
        SNDRR_ID: lambda state: [
            "[You look upon Sndrr, Sister of Wmrsk]",
            "[Sndrr speaks, her voice a sighing of winds]",
            "O Traveller, blessed art thou! Yet...",
            "T'were better if...",
            "Seek the temple pieces, quickly!",
            "I shall say no more..."
        ],
        INDRR_ID: lambda state: [
            "[You look upon Indrr, Brother of Emrsk, a man of blades.]",
            "[Indrr speaks to you, his voice a rasp of daggers]",
            "O Traveller, blessed art thou.",
            "And cursed are the makers... those who created them,",
            "The progenitors of the wiremites.",
            "I would annihilate them!",
            "But my energy needs to recover...",
            "I shall say no more."
        ]
}

def dialog_noble(stdscr, state, nid):
    dialog_flow(stdscr, noble_dialogs[nid](state))

def gen_cardinal_nobles(state):
    nobles = {}
    nobles[QMRSK_ID] = {
        'name': 'Qmrsk, Scion of Emanation',
        'symbol': 'Q',
        'position': [
            MAGIC_MAP_W//2,
            MAGIC_MAP_H//2 - MIDDLE_ROOM_DIMENSION//2,
        ]
    }
    nobles[WMRSK_ID] = {
        'name': 'Wmrsk, Scion of Occultation',
        'symbol': 'W', 
        'position': [
            MAGIC_MAP_W//2,
            MAGIC_MAP_H//2 + MIDDLE_ROOM_DIMENSION//2,
        ]
    }
    nobles[EMRSK_ID] = {
        'name': 'Emrsk, Scion of Annihilation',
        'symbol': 'E',
        'position': [
            MAGIC_MAP_W//2 - MIDDLE_ROOM_DIMENSION//2,
            MAGIC_MAP_H//2
        ]
    }
    nobles[TRSS_ID] = {
        'name': 'Trss, Noble of Power',
        'symbol': 'T',
        'position': [
            MAGIC_MAP_W//2 + MIDDLE_ROOM_DIMENSION//2,
            MAGIC_MAP_H//2
        ]
    }
    state['world']['C']['nobles'] = nobles

def spawn_rescued_noble(state, nid):
    state['world']['C']['nobles'][nid] = rescuable_noble_spec[nid]
