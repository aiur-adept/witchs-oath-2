import curses

COLORS_WIREMITE = 1
COLORS_PLAYER = 2
COLORS_NOBLES = 3
COLORS_Q_INCANT = 4
COLORS_W_INCANT = 5
COLORS_E_INCANT = 6
COLORS_ITEM = 7

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    # wiremites
    curses.init_pair(COLORS_WIREMITE,
                     curses.COLOR_BLACK, curses.COLOR_WHITE)
    # player
    curses.init_pair(COLORS_PLAYER, 
                     curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    # nobles
    curses.init_pair(COLORS_NOBLES, 
                     curses.COLOR_CYAN, curses.COLOR_BLACK)
    # Q incant (emanation)
    curses.init_pair(COLORS_Q_INCANT, 
                     curses.COLOR_GREEN, curses.COLOR_BLACK)
    # W incant (occultation)
    curses.init_pair(COLORS_W_INCANT, 
                     curses.COLOR_BLUE, curses.COLOR_BLACK)
    # E incant (annihilation)
    curses.init_pair(COLORS_E_INCANT, 
                     curses.COLOR_RED, curses.COLOR_BLACK)
    # items
    curses.init_pair(COLORS_ITEM,
                     curses.COLOR_YELLOW, curses.COLOR_BLACK)

