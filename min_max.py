import random
import numpy as np
from tqdm import tqdm
from overboard import Overboard

SIZE = 4


def play_tournament(white_move, red_move):
    overboard = Overboard(board_size=SIZE)

    average_game_length = 0
    wins = {Overboard.PLAYER_WHITE: 0, Overboard.PLAYER_RED: 0, 0: 0}

    for e in tqdm(range(100)):
        overboard.initialize_randomly()
        t = 0

        while (winner := overboard.get_winner()) is None:
            t += 1

            if t > 2 * (SIZE**2):
                winner = 0
                break

            if overboard.turn == Overboard.PLAYER_WHITE:
                piece, move = white_move(overboard)
            else:
                piece, move = red_move(overboard)

            overboard.make_move(piece, move)

        average_game_length = average_game_length + (t - average_game_length) / (e + 1)
        wins[winner] += 1

    print(f"Board size: {SIZE}")
    print(f"Average game length {average_game_length}")
    print(f"Wins by white: {wins[Overboard.PLAYER_WHITE]}")
    print(f"Wins by red: {wins[Overboard.PLAYER_RED]}")
    print(f"Incomplete games: {wins[0]}")


def random_move(overboard: Overboard):
    piece, move, _ = random.choice(overboard.get_moves())
    return (piece, move)


def greedy_move(overboard: Overboard):
    greedy_move_value = -1
    greedy_move = None

    current_board = overboard.board
    opponent_piece = (
        Overboard.PLAYER_WHITE
        if overboard.turn == Overboard.PLAYER_RED
        else Overboard.PLAYER_RED
    )

    for piece, move, preview in overboard.get_moves():
        line = (
            current_board[piece[0], :]
            if piece[0] == move[0]
            else current_board[:, piece[1]]
        )
        before = np.sum(line == opponent_piece)
        after = np.sum(preview == opponent_piece)
        score = before - after

        if score > greedy_move_value:
            greedy_move_value = score
            greedy_move = (piece, move)

    return greedy_move


def min_max_move(overboard: Overboard):
    if overboard.turn == Overboard.PLAYER_WHITE:
        best_move_value = -1000
        best_move = None

        for piece, move, _ in overboard.get_moves():
            preview, _ = overboard.get_preview_board(piece, move)
            eval = min_max(
                Overboard.from_numpy(preview, Overboard.PLAYER_RED), False, 2
            )

            if eval > best_move_value:
                best_move_value = eval
                best_move = (piece, move)

    else:
        best_move_value = 1000
        best_move = None

        for piece, move, _ in overboard.get_moves():
            preview, _ = overboard.get_preview_board(piece, move)
            eval = min_max(
                Overboard.from_numpy(preview, Overboard.PLAYER_WHITE), True, 2
            )

            if eval < best_move_value:
                best_move_value = eval
                best_move = (piece, move)

    return best_move


# WHITE -> Maximizing player
# RED -> Minimizing player
def min_max(overboard: Overboard, maximizing_player, depth=3):
    winner = overboard.get_winner()

    if winner == Overboard.PLAYER_WHITE:
        return 999
    elif winner == Overboard.PLAYER_RED:
        return -999

    if depth == 0:
        white_score = np.sum(overboard.board == Overboard.PLAYER_WHITE)
        red_score = np.sum(overboard.board == Overboard.PLAYER_RED)
        return white_score - red_score

    moves = overboard.get_moves()

    if maximizing_player:
        max_eval = -1000
        for piece, move, _ in moves:
            child, _ = overboard.get_preview_board(piece, move)
            eval = min_max(
                Overboard.from_numpy(child, Overboard.PLAYER_RED), False, depth - 1
            )
            max_eval = max(max_eval, eval)
        return max_eval

    else:
        min_eval = +1000
        for piece, move, _ in moves:
            child, _ = overboard.get_preview_board(piece, move)
            eval = min_max(
                Overboard.from_numpy(child, Overboard.PLAYER_WHITE), True, depth - 1
            )
            min_eval = min(min_eval, eval)
        return min_eval


if __name__ == "__main__":
    random.seed(12)

    # print("WHITE: Random - Red: Random")
    # play_tournament(random_move, random_move)
    # print()
    #
    # print("WHITE: Greedy - Red: Random")
    # play_tournament(greedy_move, random_move)
    # print()
    #
    # print("WHITE: Greedy - Red: Greedy")
    # play_tournament(greedy_move, greedy_move)
    # print()

    # print("WHITE: MinMax - Red: Random")
    # play_tournament(min_max_move, random_move)
    # print()

    # print("WHITE: Greedy - Red: MinMax")
    # play_tournament(greedy_move, min_max_move)
    # print()

    print("WHITE: MinMax - Red: MinMax")
    play_tournament(min_max_move, min_max_move)
    print()
