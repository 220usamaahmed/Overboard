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
        assert self.initialized == False
        self.initialized = True

        piece_count = self.board_size**2 // 2

        pieces = [self.PLAYER_WHITE] * piece_count + [self.PLAYER_RED] * piece_count
        random.shuffle(pieces)

        for r in range(self.board_size):
            for c in range(self.board_size):
                self.board[r, c] = pieces[r * self.board_size + c]

    def get_movable_piece_positions(self):
        assert self.initialized == True

        return list(zip(*np.where(self.board == self.turn)))

    def get_valid_moves(self, piece_position):
        assert self.board[*piece_position] == self.turn

        piece_row = self.board[piece_position[0], :]
        piece_col = self.board[:, piece_position[1]]

        # print(piece_row)
        # print(piece_col)

        # Testing cases

        self.board_size = 8
        piece_position = (0, 3)
        piece_row = np.array([2, 2, 2, 1, 2, 2, 2, 2])
        # piece_row = np.array([2, 1, 0, 0, 2, 2])
        # piece_row = np.array([2, 1, 0, 1, 2, 2])
        # piece_row = np.array([2, 0, 0, 1, 1, 2])

        print("\n" * 4)

        moves = []

        # Moving forward
        row_copy = piece_row.copy()
        d = -1
        print("Initial state", row_copy)
        print()
        i = piece_position[1]
        while i > 0 and i < self.board_size - 1:
            shifting_piece = row_copy[i]
            row_copy[i] = self.EMPTY
            j = i
            while j > 0 and j < self.board_size - 1:
                temp = row_copy[j + d]
                row_copy[j + d] = shifting_piece
                shifting_piece = temp
                if shifting_piece == self.EMPTY:
                    shifting_piece = None
                    break
                j += d
            if shifting_piece == self.turn:
                break
            print(row_copy)
            print("Overboard", shifting_piece)
            print()
            if shifting_piece == None and i != piece_position[1]:
                continue
            moves.append((piece_position[0], i + 1))
            i += d

        # Moving backward
        # row_copy = piece_row.copy()
        # d = -1
        # print("Initial state", row_copy)
        # print()
        # i = piece_position[1]
        # while i > 0 and i < self.board_size - 1:
        #     print(f"Staring from position {i} moving left one")
        #     shifting_piece = row_copy[i]
        #     row_copy[i] = self.EMPTY
        #     for j in reversed(range(1, i + 1)):
        #         temp = row_copy[j + d]
        #         row_copy[j + d] = shifting_piece
        #         shifting_piece = temp
        #         if shifting_piece == self.EMPTY:
        #             shifting_piece = None
        #             break
        #     if shifting_piece == self.turn:
        #         break
        #     print(row_copy)
        #     print("Overboard", shifting_piece)
        #     print()
        #     if shifting_piece == None and i != piece_position[1]:
        #         continue
        #     moves.append((piece_position[0], i + d))
        #     i += d

        print(moves)

    def display_board(self):
        assert self.initialized == True

        for r in range(self.board_size):
            print(" ".join(list(map(str, self.board[r]))))


if __name__ == "__main__":
    random.seed(1)

    overboard = Overboard(board_size=4)
    overboard.initialize_randomly()
    overboard.display_board()

    movable_pieces = overboard.get_movable_piece_positions()
    # print(movable_pieces)
    overboard.get_valid_moves(movable_pieces[0])
