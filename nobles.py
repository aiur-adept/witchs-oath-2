from dialog import (
        dialog_flow 
)

QMRSK_ID = 0
WMRSK_ID = 1
EMRSK_ID = 2
TRSS_ID  = 3

noble_dialogs = {
        QMRSK_ID: [
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
        ],
        WMRSK_ID: [
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
