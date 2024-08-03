import random
from overboard import Overboard

SIZE = 4

overboard = Overboard(board_size=SIZE)

average_game_length = 0
wins = { Overboard.PLAYER_WHITE: 0, Overboard.PLAYER_RED: 0 }


for e in range(100):
    overboard.initialize_randomly()
    t = 0

    while (winner := overboard.get_winner()) is None: 
        t += 1

        piece, move = random.choice(overboard.get_moves())
        overboard.make_move(piece, move)
 
    average_game_length = average_game_length + (t - average_game_length) / (e + 1)
    wins[winner] += 1

print(f"Board size: {SIZE}")
print(f"Average game length {average_game_length}")
print(f"Wins by white: {wins[Overboard.PLAYER_WHITE]}")
print(f"Wins by red: {wins[Overboard.PLAYER_RED]}")

        

