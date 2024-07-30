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

    def get_valid_moves(self, piece_position):
        assert self.board[*piece_position] == self.turn

        pieces_row = self.board[piece_position[0], :]
        pieces_col = self.board[:, piece_position[1]]

        print()
        print()

        left_moves = [
            (piece_position[0], i)
            for i in self.get_valid_shifts(pieces_row.copy(), piece_position[1], -1)
        ]
        print(f"{left_moves=}")
        right_moves = [
            (piece_position[0], i)
            for i in self.get_valid_shifts(pieces_row.copy(), piece_position[1], +1)
        ]
        print(f"{right_moves=}")
        up_moves = [
            (i, piece_position[1])
            for i in self.get_valid_shifts(pieces_col.copy(), piece_position[0], -1)
        ]
        print(f"{up_moves=}")
        down_moves = [
            (i, piece_position[1])
            for i in self.get_valid_shifts(pieces_col.copy(), piece_position[0], +1)
        ]
        print(f"{down_moves=}")

    def get_valid_shifts(self, pieces, start_index, direction):
        valid_indices = []
        print("Initial state", pieces)
        print()
        i = start_index
        while (direction == -1 and i > 0) or (
            direction == +1 and i < self.board_size - 1
        ):
            print(i)
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
            print(pieces)
            print("Overboard", shifting_piece)
            print()
            i += direction
            if shifting_piece == None and i - direction != start_index:
                continue
            valid_indices.append(i)
        return valid_indices

    def display_board(self):
        assert self.initialized == True

        for r in range(self.board_size):
            print(" ".join(list(map(str, self.board[r]))))


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
            [2, 2, 2, 2, 0, 0, 0, 1],
        ]
    )
    overboard.initialize(board, Overboard.PLAYER_WHITE)
    overboard.display_board()
    overboard.get_valid_moves((7, 7))
