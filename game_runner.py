from enum import Enum, auto
import curses
from overboard import Overboard


class Color(Enum):
    CYAN = auto()
    BLUE = auto()
    RED = auto()
    WHITE = auto()
    YELLOW = auto()

    @staticmethod
    def get(foreground: "Color", background: "Color"):
        return background.value * 10 + foreground.value


class GameRunner:
    BLOCK_WIDTH = 7
    BLOCK_HEIGHT = 3

    SPACE = "\u0020"
    HORIZONTAL = f"\u2500"
    VERTICAL = f"\u2502"
    PIECE = "\u25CB"
    SELECTED_PIECE = "\u25CF"

    def __init__(self, board_size=8):
        self.overboard = Overboard(board_size)
        # self.overboard.initialize_randomly()
        self.overboard.initialize_test_board()

        self.cursor = (0, 0)
        self.selected_piece = None
        self.message = ""

    def handle_key_press(self, key):
        if self.selected_piece == None:
            self.handle_piece_selection(key)
        else:
            self.handle_slide(key)

    def handle_piece_selection(self, key):
        board_size = self.overboard.board_size

        if key == curses.KEY_UP:
            self.cursor = (max(0, self.cursor[0] - 1), self.cursor[1])
        elif key == curses.KEY_DOWN:
            self.cursor = (min(board_size - 1, self.cursor[0] + 1), self.cursor[1])
        elif key == curses.KEY_LEFT:
            self.cursor = (self.cursor[0], max(0, self.cursor[1] - 1))
        elif key == curses.KEY_RIGHT:
            self.cursor = (self.cursor[0], min(board_size - 1, self.cursor[1] + 1))
        elif key == ord(" "):
            if self.overboard.board[*self.cursor] == self.overboard.turn:
                self.selected_piece = self.cursor
            else:
                self.message = "Pick a piece of your color"

    def handle_slide(self, key):
        assert self.selected_piece is not None

        cursor = self.cursor
        selected_piece = self.selected_piece
        board_size = self.overboard.board_size

        if key == curses.KEY_UP and cursor[1] == selected_piece[1]:
            cursor = (max(0, cursor[0] - 1), cursor[1])
        elif key == curses.KEY_DOWN and cursor[1] == selected_piece[1]:
            cursor = (min(board_size - 1, cursor[0] + 1), cursor[1])
        elif key == curses.KEY_LEFT and cursor[0] == selected_piece[0]:
            cursor = (cursor[0], max(0, cursor[1] - 1))
        elif key == curses.KEY_RIGHT and cursor[0] == selected_piece[0]:
            cursor = (cursor[0], min(board_size - 1, cursor[1] + 1))
        elif key == ord(" "):
            selected_piece = None
            return
        elif key == ord("a"):
            try:
                self.overboard.make_move(selected_piece, cursor)
                self.selected_piece = None
                self.cursor = (0, 0)
            except Exception:
                self.message = "You can not move your piece here"
            return

        try:
            self.overboard.get_preview_board(selected_piece, cursor)
            self.cursor = cursor
            self.selected_piece = selected_piece
        except Exception:
            self.message = "Can not overboard your own piece"

    def render(self, stdscr):
        self.draw_board(stdscr)

        stdscr.addstr(
            self.overboard.board_size * self.BLOCK_HEIGHT + 2, 0, self.message
        )

    def draw_board(self, stdscr):
        board_size = self.overboard.board_size
        for r in range(board_size):
            for c in range(board_size):
                block = self.get_block(r, c)
                for b_r in range(self.BLOCK_HEIGHT):
                    for b_c in range(self.BLOCK_WIDTH):
                        block_char = block[b_r][b_c][0]
                        block_color = block[b_r][b_c][1]
                        stdscr.addstr(
                            r * self.BLOCK_HEIGHT + b_r,
                            c * self.BLOCK_WIDTH + b_c,
                            block_char,
                            curses.color_pair(block_color),
                        )

    def get_block(self, row, col):
        board = self.overboard.board
        if self.selected_piece is not None:
            board, valid = self.overboard.get_preview_board(
                self.selected_piece, self.cursor
            )

        piece = board[row, col]
        background = Color.BLUE
        if self.selected_piece is not None and (
            row == self.selected_piece[0] or col == self.selected_piece[1]
        ):
            background = Color.CYAN

        if row == self.cursor[0] and col == self.cursor[1]:
            background = Color.YELLOW

        block = [
            [
                (self.SPACE, Color.get(background, background))
                for _ in range(self.BLOCK_WIDTH)
            ]
            for _ in range(self.BLOCK_HEIGHT)
        ]
        piece_char = (
            self.SELECTED_PIECE
            if self.selected_piece is not None and (row, col) == self.cursor
            else self.PIECE
        )

        if piece == Overboard.PLAYER_RED:
            block[self.BLOCK_HEIGHT // 2][self.BLOCK_WIDTH // 2] = (
                piece_char,
                Color.get(Color.RED, background),
            )
        elif piece == Overboard.PLAYER_WHITE:
            block[self.BLOCK_HEIGHT // 2][self.BLOCK_WIDTH // 2] = (
                piece_char,
                Color.get(Color.WHITE, background),
            )

        return block


def setup_curses_colors():
    curses.start_color()

    # BLUE Background
    curses.init_pair(
        Color.get(Color.BLUE, Color.BLUE), curses.COLOR_BLUE, curses.COLOR_BLUE
    )
    curses.init_pair(
        Color.get(Color.RED, Color.BLUE), curses.COLOR_RED, curses.COLOR_BLUE
    )
    curses.init_pair(
        Color.get(Color.WHITE, Color.BLUE), curses.COLOR_WHITE, curses.COLOR_BLUE
    )

    # CYAN Background
    curses.init_pair(
        Color.get(Color.CYAN, Color.CYAN), curses.COLOR_CYAN, curses.COLOR_CYAN
    )
    curses.init_pair(
        Color.get(Color.RED, Color.CYAN), curses.COLOR_RED, curses.COLOR_CYAN
    )
    curses.init_pair(
        Color.get(Color.WHITE, Color.CYAN), curses.COLOR_WHITE, curses.COLOR_CYAN
    )

    # Yellow Background
    curses.init_pair(
        Color.get(Color.YELLOW, Color.YELLOW), curses.COLOR_YELLOW, curses.COLOR_YELLOW
    )
    curses.init_pair(
        Color.get(Color.RED, Color.YELLOW), curses.COLOR_RED, curses.COLOR_YELLOW
    )
    curses.init_pair(
        Color.get(Color.WHITE, Color.YELLOW), curses.COLOR_WHITE, curses.COLOR_YELLOW
    )


def game_loop(stdscr):
    setup_curses_colors()

    game_runner = GameRunner()

    stdscr.nodelay(1)
    stdscr.timeout(1000)

    while True:
        stdscr.clear()
        game_runner.render(stdscr)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord("q"):
            break
        else:
            game_runner.handle_key_press(key)


if __name__ == "__main__":
    curses.wrapper(game_loop)
