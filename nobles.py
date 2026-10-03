from dialog import (
        dialog_flow 
)

QMRSK_ID = 0
WMRSK_ID = 1
EMRSK_ID = 2
TRSS_ID  = 3

noble_dialogs = {
        QMRSK_ID: [
        ],
        WMRSK_ID: [
        ],
        EMRSK_ID: [
        ],
        TRSS_ID: [
            "[You look upon Trss, Noble of Power, a woman of fine silk]",
            "[Trss speaks to you, her voice as a silver drop of moonlight]",
            "O Traveller of incantation's warp and weft",
            "You find us here bereaved, of hope bereft...",
            "Assemble thee the pieces of the temple found", 
            "Completing in thy pilgrimage the round...",
            "In each direction cardinal embark",
            "Beware the wiremites who hunger, hark!",
            "My tale's a weary one of woe to tell,",
            "I'll tell it at the journey's end, and well."
        ]
}

def dialog_noble(stdscr, state, nid):
    dialog_flow(stdscr, noble_dialogs[nid])
