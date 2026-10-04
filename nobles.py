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
            "[You look upon Emrsk, Scion of Annihilation, a man of flames]",
            "[Emrsk speaks to you, his voice as a crackle of cinders]",
            "O Traveller, in another life, I would annihilate you,",
            "Merely for having come to this place, yet that time is gone,",
            "For Trss had spent her last tears to return us to peace.",
            "Truly, the incantation [E] is an incantation of annihilation,",
            "Suitable for returning wiremites of annihilation (red).",
            "Find my brother to the west, and return him.",
            "He will offer aid. I shall speak no more. Be gone."
        ],
        TRSS_ID: [
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
}

def dialog_noble(stdscr, state, nid):
    dialog_flow(stdscr, noble_dialogs[nid])
