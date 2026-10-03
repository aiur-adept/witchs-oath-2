import curses
from curses.textpad import rectangle
from constants import (
        DIALOG_BOX_X, 
        DIALOG_BOX_Y, 
        DIALOG_BOX_W, 
        DIALOG_BOX_H
)

def dialog_flow(stdscr, msgs):
    for i in range(0, len(msgs)):
        dialog_win = display_dialog_box(stdscr, msgs[i])
        key = stdscr.getch()
        while key != ord(' '):
            key = stdscr.getch()
            if key == ' ':
                break
        dialog_win.erase()
        dialog_win.refresh()

def display_dialog_box(stdscr, msg):
    dialog_win = curses.newwin(DIALOG_BOX_H, DIALOG_BOX_W, 
                             DIALOG_BOX_Y, DIALOG_BOX_X)
    dialog_win.attrset(curses.color_pair(3))
    dialog_win.box()
    dialog_win.addstr(1, 1, msg, curses.color_pair(3))
    dialog_win.addstr(2, 5, "[space to continue]", curses.color_pair(0))
    dialog_win.refresh()
    return dialog_win
