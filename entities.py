displays = [
        ' ', # empty space          0   SPACE
        '█', # barrier                  
        'O', # Trss's ring              ITEMS
        '^', # Trss's hat 
        '+', # health bottle 
        'w', # witch                5   ENTITIES
        'n', # noble
        'b', # bird TODO
        '0', # unknown ring 
        'W', # wiremite
        't', # temple piece         10
        '!', # Q Incantation            EFFECTS
        '@', # W Incantation 
        '#', # E Incantation
]

EMPTY_SPACE = 0
BARRIER = 1
TRSS_RING = 2
TRSS_HAT = 3
HEALTH_BOTTLE = 4
WITCH = 5
NOBLE = 6
BIRD = 7
UNKNOWN_RING = 8
WIREMITE = 9
TEMPLE_PIECE = 10
Q_INCANT = 11
W_INCANT = 12
E_INCANT = 13

def is_item(e):
    return e in [TRSS_RING, TRSS_HAT, HEALTH_BOTTLE, UNKNOWN_RING, TEMPLE_PIECE]
