from ttt_ai import *
from randomP1 import *
from decision_tree import *
from overseer import *
import time

#just stuff to play the game, no thinking going on down here

ai_player_1 = TTT_ai()
ai_player_2 = TTT_ai()
rnd_player = random_player()
results = [0, 0, 0]


# print("Game: 1")
board = Overseer(rnd_player, ai_player_1)
# board.print_board()
res = board.game_loop_learn()
ai_player_1.finalize_score(res)
results[res] += 1
for x in range(1,100005):
	if (x % 10000 == 0):
		print("Game: " + str(x))
	board = Overseer(rnd_player, ai_player_1)
	# board.print_board()
	res = board.game_loop_learn()
	ai_player_1.finalize_score(res)
	results[res] += 1


ai_player_1.start_mem_connection(True)
print("Now training the second AI")
time.sleep(2)

# print("Game: 1")
board = Overseer(rnd_player, ai_player_2)
# board.print_board()
res = board.game_loop_learn()
ai_player_2.finalize_score(res)
results[res] += 1
for x in range(1,100005):
	if (x % 10000 == 0):
		print("Game: " + str(x))

	if (x % 2 == 0):
		board = Overseer(ai_player_1, ai_player_2)
	else:
		board = Overseer(rnd_player, ai_player_2)

	# board.print_board()
	res = board.game_loop_learn()
	ai_player_2.finalize_score(res)
	results[res] += 1

ai_player_2.start_mem_connection(False)


play_order = True
while (True):
	# if (play_order):
	# print("AI goes first")
	board = Overseer(None, ai_player_2)
	res = board.game_loop_play()
	ai_player_2.finalize_score(res)
	# else:
	# 	print("AI goes second")
	# 	board = Overseer(None, ai_player_2)
	# 	res = board.game_loop_play(play_order)
	# 	ai_player_2.finalize_score(res)

	results[res] += 1
	play_order = not play_order
	reply = input("Do you want to continue? (Y | N): ")
	reply = reply.upper()
	if (reply == "N"):
		print("Thanks for playing")
		break