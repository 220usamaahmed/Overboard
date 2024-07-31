from dataclasses import dataclass
from typing import List, Literal, Tuple
import os
import shutil
import curses
import random
from overboard import Overboard


BLOCK_WIDTH = 7
BLOCK_HEIGHT = 3

BLUE_ON_BLUE = 1
CYAN_ON_CYAN = 2
RED_ON_BLUE = 3
WHITE_ON_BLUE = 4
RED_ON_CYAN = 5
WHITE_ON_CYAN = 6
RED_ON_YELLOW = 7
WHITE_ON_YELLOW = 8

SPACE = "\u0020"
HORIZONTAL = f"\u2500"
VERTICAL = f"\u2502"
PIECE = "\u25CB"
SELECTED_PIECE = "\u25CF"


@dataclass
class Char:
    char: str
    color: int


def setup_colors():
    curses.start_color()
    curses.init_pair(BLUE_ON_BLUE, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(CYAN_ON_CYAN, curses.COLOR_CYAN, curses.COLOR_CYAN)

    curses.init_pair(RED_ON_BLUE, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)

    curses.init_pair(RED_ON_CYAN, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(WHITE_ON_CYAN, curses.COLOR_WHITE, curses.COLOR_CYAN)

    curses.init_pair(RED_ON_YELLOW, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(WHITE_ON_YELLOW, curses.COLOR_WHITE, curses.COLOR_YELLOW)


def get_block(piece, highlighted=False, selected=False) -> List[List[Char]]:
    block = [
        [
            Char(SPACE, BLUE_ON_BLUE if highlighted else CYAN_ON_CYAN)
            for _ in range(BLOCK_WIDTH)
        ]
        for _ in range(BLOCK_HEIGHT)
    ]

    piece_char = SELECTED_PIECE if selected else PIECE

    if piece == Overboard.PLAYER_RED:
        block[BLOCK_HEIGHT // 2][BLOCK_WIDTH // 2] = Char(
            piece_char, RED_ON_BLUE if highlighted else RED_ON_CYAN
        )
    elif piece == Overboard.PLAYER_WHITE:
        block[BLOCK_HEIGHT // 2][BLOCK_WIDTH // 2] = Char(
            piece_char, WHITE_ON_BLUE if highlighted else WHITE_ON_CYAN
        )

    return block


def draw_board(stdscr, board, cursor, selected_piece):
    for i in range(board.shape[0]):
        for j in range(board.shape[0]):
            block = get_block(board[i, j], (i, j) == cursor, (i, j) == selected_piece)
            for b_i in range(BLOCK_HEIGHT):
                for b_j in range(BLOCK_WIDTH):
                    block_char = block[b_i][b_j].char
                    block_color = block[b_i][b_j].color
                    stdscr.addstr(
                        i * BLOCK_HEIGHT + b_i,
                        j * BLOCK_WIDTH + b_j,
                        block_char,
                        curses.color_pair(block_color),
                    )


SIZE = 2
selected_piece = None
cursor = (0, 0)
message = ""
overboard = Overboard(board_size=SIZE)


def handle_piece_selection(key):
    global message, cursor, selected_piece

    if key == curses.KEY_UP:
        cursor = (max(0, cursor[0] - 1), cursor[1])
    elif key == curses.KEY_DOWN:
        cursor = (min(SIZE - 1, cursor[0] + 1), cursor[1])
    elif key == curses.KEY_LEFT:
        cursor = (cursor[0], max(0, cursor[1] - 1))
    elif key == curses.KEY_RIGHT:
        cursor = (cursor[0], min(SIZE - 1, cursor[1] + 1))
    elif key == ord(" "):
        if overboard.board[*cursor] == overboard.turn:
            selected_piece = cursor
        else:
            message = "Pick a piece of your color"


def handle_slide(key):
    global selected_piece, cursor, message

    assert selected_piece is not None

    if key == curses.KEY_UP and cursor[1] == selected_piece[1]:
        cursor = (max(0, cursor[0] - 1), cursor[1])
    elif key == curses.KEY_DOWN and cursor[1] == selected_piece[1]:
        cursor = (min(SIZE - 1, cursor[0] + 1), cursor[1])
    elif key == curses.KEY_LEFT and cursor[0] == selected_piece[0]:
        cursor = (cursor[0], max(0, cursor[1] - 1))
    elif key == curses.KEY_RIGHT and cursor[0] == selected_piece[0]:
        cursor = (cursor[0], min(SIZE - 1, cursor[1] + 1))
    elif key == ord(" "):
        selected_piece = None
    elif key == ord("a"):
        message = "Here"
        try:
            overboard.make_move(selected_piece, cursor)
            selected_piece = None
            cursor = (0, 0)
        except Exception:
            message = "You can not move your piece here"


def main(stdscr):
    global overboard, selected_piece, cursor

    # overboard.initialize_test_board()
    overboard.initialize_randomly()

    setup_colors()

    curses.curs_set(0)

    stdscr.nodelay(1)
    stdscr.timeout(1000)

    blit = True

    while True:
        if True or blit:
            stdscr.clear()
            board = overboard.board
            if selected_piece is not None:
                board, valid = overboard.get_preview_board(selected_piece, cursor)
            draw_board(stdscr, board, cursor, cursor if selected_piece else None)
            blit = False

        if winner := overboard.get_winner() is not None:
            stdscr.addstr(8 * BLOCK_HEIGHT + 3, 0, f"Game won by {winner}")
        else:
            stdscr.addstr(8 * BLOCK_HEIGHT + 3, 0, message)

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord("q"):
            break

        if selected_piece is None:
            handle_piece_selection(key)
        else:
            handle_slide(key)


if __name__ == "__main__":
    curses.wrapper(main)
