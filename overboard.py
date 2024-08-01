import numpy as np
import random


class Overboard:
    EMPTY = 0
    PLAYER_WHITE = 1
    PLAYER_RED = 2

    def __init__(self, board_size=8):
        self.board_size = board_size
        self.reset()

    def reset(self):
        self.initialized = False
        self.board = np.array(
            [
                [self.EMPTY for _ in range(self.board_size)]
                for _ in range(self.board_size)
            ]
        )
        self.turn = self.PLAYER_WHITE

    def initialize_randomly(self):
        self.reset()
        self.initialized = True

        piece_count = self.board_size**2 // 2

        pieces = [self.PLAYER_WHITE] * piece_count + [self.PLAYER_RED] * piece_count
        random.shuffle(pieces)

        for r in range(self.board_size):
            for c in range(self.board_size):
                self.board[r, c] = pieces[r * self.board_size + c]

    def initialize(self, board, turn):
        assert self.board.shape[0] == self.board.shape[1]

        self.reset()
        self.initialized = True

        self.board = board
        self.board_size = self.board.shape[0]
        self.turn = turn

    def get_movable_piece_positions(self):
        assert self.initialized == True

        return list(zip(*np.where(self.board == self.turn)))

    def get_winner(self):
        if not np.any(self.board == self.PLAYER_RED):
            return self.PLAYER_WHITE

        if not np.any(self.board == self.PLAYER_WHITE):
            return self.PLAYER_RED

        return None

    def get_moves(self, piece_position):
        assert self.board[*piece_position] == self.turn

        pieces_row = self.board[piece_position[0], :]
        pieces_col = self.board[:, piece_position[1]]

        left_moves = [
            ((piece_position[0], i), preview, valid)
            for i, preview, valid in self.get_shifts(
                pieces_row.copy(), piece_position[1], -1
            )
        ]

        right_moves = [
            ((piece_position[0], i), preview, valid)
            for i, preview, valid in self.get_shifts(
                pieces_row.copy(), piece_position[1], +1
            )
        ]

        up_moves = [
            ((i, piece_position[1]), preview, valid)
            for i, preview, valid in self.get_shifts(
                pieces_col.copy(), piece_position[0], -1
            )
        ]

        down_moves = [
            ((i, piece_position[1]), preview, valid)
            for i, preview, valid in self.get_shifts(
                pieces_col.copy(), piece_position[0], +1
            )
        ]

        return left_moves + right_moves + up_moves + down_moves

    def make_move(self, start_position, end_position):
        board, valid = self.get_preview_board(start_position, end_position)
        if valid:
            self.board = board
            self.turn = (
                self.PLAYER_WHITE if self.turn == self.PLAYER_RED else self.PLAYER_RED
            )
        else:
            raise Exception("Invalid move")

    def get_preview_board(self, start_position, end_position):
        assert self.board[*start_position] == self.turn

        preview_board = self.board.copy()
        valid = True

        if start_position[0] == end_position[0]:
            pieces_row = self.board[start_position[0], :].copy()
            direction = 1 if end_position[1] > start_position[1] else -1
            shifts = self.get_shifts(
                pieces_row, start_position[1], direction, end_position[1]
            )
            if len(shifts):
                _, preview, valid = shifts[-1]
                preview_board[start_position[0], :] = preview
        elif start_position[1] == end_position[1]:
            pieces_col = self.board[:, start_position[1]].copy()
            direction = 1 if end_position[0] > start_position[0] else -1
            shifts = self.get_shifts(
                pieces_col, start_position[0], direction, end_position[0]
            )
            if len(shifts):
                _, preview, valid = shifts[-1]
                preview_board[:, start_position[1]] = preview
        else:
            raise Exception("You can only slide in one direction")

        return preview_board, valid

    def get_shifts(self, pieces, start_index, direction, end_index=None):
        slides = []
        # print("Initial state", pieces, start_index, end_index)
        # print()
        i = start_index
        while (
            (direction == -1 and i > 0) or (direction == +1 and i < self.board_size - 1)
        ) and i != end_index:
            shifting_piece = pieces[i]
            pieces[i] = self.EMPTY
            j = i
            while (direction == -1 and j > 0) or (
                direction == +1 and j < self.board_size - 1
            ):
                temp = pieces[j + direction]
                pieces[j + direction] = shifting_piece
                shifting_piece = temp
                if shifting_piece == self.EMPTY:
                    shifting_piece = None
                    break
                j += direction
            if shifting_piece == self.turn:
                break
            # print(pieces)
            # print("Overboard", shifting_piece)
            # print()
            i += direction
            slides.append(
                (
                    i,
                    pieces.copy(),
                    shifting_piece != None or i - direction == start_index,
                )
            )
        if end_index is not None and i != end_index:
            raise Exception("Can not overboard your own piece")
        return slides

    def display_board(self):
        assert self.initialized == True

        for r in range(self.board_size):
            print(" ".join(list(map(str, self.board[r]))))

    def initialize_test_board(self):
        board = np.array(
            [
                [1, 0, 0, 2, 0, 2, 2, 2],
                [0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0],
                [2, 2, 2, 1, 2, 2, 2, 2],
                [0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0],
                [2, 2, 2, 2, 0, 1, 0, 1],
            ]
        )
        self.initialize(board, Overboard.PLAYER_WHITE)


if __name__ == "__main__":
    random.seed(1)

    overboard = Overboard(board_size=4)
    board = np.array(
        [
            [1, 0, 0, 2, 0, 2, 2, 2],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [2, 2, 2, 1, 2, 2, 2, 2],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [2, 2, 2, 2, 0, 1, 0, 1],
        ]
    )
    overboard.initialize(board, Overboard.PLAYER_WHITE)
    moves = overboard.get_moves((7, 7))
    for i, p, v in moves:
        print(i, p, v)
    overboard.display_board()
    preview, valid = overboard.get_preview_board((7, 7), (7, 0))
    print(preview)
    print(valid)
