import entities
from dialog import (
        dialog_flow
)

names = {
    entities.TRSS_RING: "Trss's Ring",
    entities.TRSS_HAT: "Trss's Hat",
    entities.HEALTH_BOTTLE: 'Health Bottle',
    entities.UNKNOWN_RING: 'Unknown Ring',
    entities.TEMPLE_PIECE: 'Piece of Temple'
}

def pick_up_item(stdscr, state, collided_item, p):
    # clear space where item was
    cardinal = state['player']['setting']
    state['map'][cardinal][p[1]][p[0]] = entities.EMPTY_SPACE
    # display dialog
    dialog_flow(stdscr, [f'[You picked up {names[collided_item]}]'])
    # track temple completion
    if collided_item == entities.TEMPLE_PIECE:
        state['player']['temple_pieces_count'] += 1
