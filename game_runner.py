from enum import Enum, auto
import curses
from overboard import Overboard


class Color(Enum):
    CYAN = auto()
    BLUE = auto()
    RED = auto()
    WHITE = auto()
    YELLOW = auto()
    GREEN = auto()

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
        self.overboard.initialize_randomly()
        # self.overboard.initialize_test_board()

        self.cursor = (0, 0)
        self.selected_piece = None

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
            self.selected_piece = None
            return
        elif key in [curses.KEY_ENTER, ord("\n")]:
            try:
                self.overboard.make_move(selected_piece, cursor)
                self.selected_piece = None
                self.cursor = (0, 0)
            except Exception:
                pass
            return

        try:
            self.overboard.get_preview_board(selected_piece, cursor)
            self.cursor = cursor
            self.selected_piece = selected_piece
        except Exception:
            ...

    def render(self, stdscr):
        self.draw_board(stdscr)

        if (winner := self.overboard.get_winner()) is not None:
            if winner == Overboard.PLAYER_WHITE:
                self.display_white_wins(stdscr)
            else:
                self.display_red_wins(stdscr)

    def draw_board(self, stdscr):
        terminal_rows, terminal_cols = stdscr.getmaxyx()
        board_size = self.overboard.board_size

        starting_c = (terminal_cols - board_size * self.BLOCK_WIDTH) // 2
        starting_r = (terminal_rows - board_size * self.BLOCK_HEIGHT) // 2

        self.display_turn_indicators(stdscr)

        for r in range(board_size):
            for c in range(board_size):
                block = self.get_block(r, c)
                for b_r in range(self.BLOCK_HEIGHT):
                    for b_c in range(self.BLOCK_WIDTH):
                        block_char = block[b_r][b_c][0]
                        block_color = block[b_r][b_c][1]
                        stdscr.addstr(
                            starting_r + r * self.BLOCK_HEIGHT + b_r,
                            starting_c + c * self.BLOCK_WIDTH + b_c,
                            block_char,
                            curses.color_pair(block_color),
                        )

    def display_turn_indicators(self, stdscr):
        terminal_rows, terminal_cols = stdscr.getmaxyx()

        white = "WHITE"
        red = "RED"

        board_width = self.BLOCK_WIDTH * self.overboard.board_size
        board_height = self.BLOCK_HEIGHT * self.overboard.board_size
        starting_x = (terminal_cols - board_width) // 2

        turn_color = curses.color_pair(Color.get(Color.BLUE, Color.WHITE))
        non_turn_color = curses.color_pair(Color.get(Color.WHITE, Color.BLUE))

        stdscr.addstr(
            (terminal_rows - board_height) // 2 - 2,
            starting_x,
            f" {white}{' ' * (board_width - len(white) - 1)}",
            (
                turn_color
                if self.overboard.turn == Overboard.PLAYER_WHITE
                else non_turn_color
            ),
        )
        stdscr.addstr(
            (terminal_rows - board_height) // 2 + board_height + 1,
            starting_x,
            f" {red}{' ' * (board_width - len(red) - 1)}",
            (
                turn_color
                if self.overboard.turn == Overboard.PLAYER_RED
                else non_turn_color
            ),
        )

    def display_white_wins(self, stdscr):
        banner = r"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ██╗    ██╗██╗  ██╗██╗████████╗███████╗    ██╗    ██╗██╗███╗   ██╗███████╗  │
│  ██║    ██║██║  ██║██║╚══██╔══╝██╔════╝    ██║    ██║██║████╗  ██║██╔════╝  │
│  ██║ █╗ ██║███████║██║   ██║   █████╗      ██║ █╗ ██║██║██╔██╗ ██║███████╗  │
│  ██║███╗██║██╔══██║██║   ██║   ██╔══╝      ██║███╗██║██║██║╚██╗██║╚════██║  │
│  ╚███╔███╔╝██║  ██║██║   ██║   ███████╗    ╚███╔███╔╝██║██║ ╚████║███████║  │
│   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝     ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚══════╝  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
        """
        self.display_banner(stdscr, banner, Color.get(Color.WHITE, Color.GREEN))

    def display_red_wins(self, stdscr):
        banner = f"""
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│  ██████╗ ███████╗██████╗     ██╗    ██╗██╗███╗   ██╗███████╗  │
│  ██╔══██╗██╔════╝██╔══██╗    ██║    ██║██║████╗  ██║██╔════╝  │
│  ██████╔╝█████╗  ██║  ██║    ██║ █╗ ██║██║██╔██╗ ██║███████╗  │
│  ██╔══██╗██╔══╝  ██║  ██║    ██║███╗██║██║██║╚██╗██║╚════██║  │
│  ██║  ██║███████╗██████╔╝    ╚███╔███╔╝██║██║ ╚████║███████║  │
│  ╚═╝  ╚═╝╚══════╝╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚══════╝  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
        """
        self.display_banner(stdscr, banner, Color.get(Color.WHITE, Color.GREEN))

    def display_banner(self, stdscr, banner, color):
        padding = 3
        terminal_rows, terminal_cols = stdscr.getmaxyx()

        banner = banner.split("\n")
        widest_line = max(map(len, banner))
        line_width = widest_line + 2 * padding

        starting_x = (terminal_cols - line_width) // 2
        starting_y = (terminal_rows - len(banner)) // 2

        for i, line in enumerate(banner):
            stdscr.addstr(
                starting_y + i,
                starting_x,
                f"{' ' * padding}{line}{' ' * (line_width - len(line) - padding)}",
                curses.color_pair(color),
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

    # Green Background
    curses.init_pair(
        Color.get(Color.WHITE, Color.GREEN), curses.COLOR_WHITE, curses.COLOR_GREEN
    )

    # White Background
    curses.init_pair(
        Color.get(Color.BLUE, Color.WHITE), curses.COLOR_BLUE, curses.COLOR_WHITE
    )


def game_loop(stdscr):
    setup_curses_colors()

    game_runner = GameRunner(8)

    stdscr.nodelay(False)
    curses.curs_set(0)

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
