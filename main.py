from dataclasses import dataclass
from typing import List, Literal, Tuple
import os
import shutil
import curses
import random


BLOCK_WIDTH = 7
BLOCK_HEIGHT = 3

RED_ON_RED = 1
BLUE_ON_BLUE = 2
RED_ON_WHITE = 3


@dataclass
class Char:
    char: str
    color: int


def setup_colors():
    curses.start_color()
    curses.init_pair(RED_ON_RED, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(BLUE_ON_BLUE, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(RED_ON_WHITE, curses.COLOR_RED, curses.COLOR_WHITE)


def get_block(red) -> List[List[Char]]:
    block = [
        [
            Char("\u0020", RED_ON_RED if red else BLUE_ON_BLUE)
            for _ in range(BLOCK_WIDTH)
        ]
        for _ in range(BLOCK_HEIGHT)
    ]

    block[BLOCK_HEIGHT // 2][BLOCK_WIDTH // 2] = Char("\u25CB", RED_ON_WHITE)
    block[BLOCK_HEIGHT // 2][BLOCK_WIDTH // 2 - 1].color = RED_ON_WHITE
    block[BLOCK_HEIGHT // 2][BLOCK_WIDTH // 2 + 1].color = RED_ON_WHITE

    return block


def draw_board(
    stdscr, board: List[List[Literal["W", "R"]]], selected_piece: Tuple[int, int]
):
    for i in range(5):
        for j in range(5):
            block = get_block((i + j) % 2 == 0)
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


def main(stdscr):
    SIZE = 8

    board: List[List[Literal["R", "W"]]] = [
        [random.choice(["R", "W"]) for _ in range(SIZE)] for _ in range(SIZE)
    ]

    selected_piece = (0, 0)

    setup_colors()

    curses.curs_set(0)

    stdscr.nodelay(1)
    stdscr.timeout(1000)

    count = 0

    while True:
        if count == 0:
            stdscr.clear()
            draw_board(stdscr, board, selected_piece)

        stdscr.addstr(17, 0, str(count))
        count += 1
        if count > 10:
            count = 0

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_piece = (max(0, selected_piece[0] - 1), selected_piece[1])
        elif key == curses.KEY_DOWN:
            selected_piece = (min(SIZE - 1, selected_piece[0] + 1), selected_piece[1])
        elif key == curses.KEY_LEFT:
            selected_piece = (selected_piece[0], max(0, selected_piece[1] - 1))
        elif key == curses.KEY_RIGHT:
            selected_piece = (selected_piece[0], min(SIZE - 1, selected_piece[1] + 1))
        elif key == ord("q"):
            break


if __name__ == "__main__":
    curses.wrapper(main)


"""
    RED = "\033[91m"
    GRAY = "\033[90m"
    RESET = "\033[0m"

    SPACE = "\u0020"
    HORIZONTAL = f"{GRAY}\u2500{RESET}"
    VERTICAL = f"{GRAY}\u2502{RESET}"
    PIECE = "\u25CB"
    SELECTED_PIECE = "\u25CF"

    SIZE = len(board)
    H_SPACING = 3

    terminal_size = shutil.get_terminal_size()
    board_width = H_SPACING * SIZE + (H_SPACING - 1)

    for row_i in range(SIZE):
        print(f"{SPACE * H_SPACING}{VERTICAL}" * SIZE)

        for col_i in range(SIZE):
            print(HORIZONTAL * H_SPACING, end="")
            piece_char = PIECE if (row_i, col_i) != selected_piece else SELECTED_PIECE
            if board[row_i][col_i] == "W":
                print(piece_char, end="")
            else:
                print(f"{RED}{piece_char}{RESET}", end="")
        print(HORIZONTAL * 3)

    print(f"{SPACE * H_SPACING}{VERTICAL}" * SIZE)

    stdscr.refresh()
"""
