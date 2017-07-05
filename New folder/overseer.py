from ttt_ai import *
from randomP1 import *
from decision_tree import *
import time

class Overseer:
	def __init__(self, rnd_plr, ai_plr):
		self.board = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
		self.winning_combos = ([0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [2, 4, 6], [0, 4, 8])
		self.pick = 0
		self.rnd_plr = rnd_plr
		self.ai_plr = ai_plr

		self.template = """
		   \t  %s | %s | %s  
		   \t-------------
		   \t  %s | %s | %s  
		   \t-------------
		   \t  %s | %s | %s  
		"""

	def print_board(self,board = None):
		"Display board on screen"
		if board is None:
			print(self.template % tuple(self.board[0:3] + self.board[3:6] + self.board[6:9]))
		else:
			print(self.template % tuple(board[0:3] + board[3:6] + board[6:9]))

	def check_for_win(self, board, marker):
		for combo in self.winning_combos:
			if (board[combo[0]] == board[combo[1]] == board[combo[2]] == marker):
				return True
		return False

	def check_for_draw(self, board):
		draw = True 
		for x in board:
			if (x in ['0', '1', '2', '3', '4', '5', '6', '7', '8']):
				draw = False
		return draw

	def is_space_occupied(self, selection):
		if (selection.isdigit() == False):
			return True

		selection = int(selection)
		if (selection not in [0, 1, 2, 3, 4, 5, 6, 7, 8]):
			return True
		elif (self.board[int(selection)] in ['X', 'O']):
			return True
		else:
			return False

	def ask_for_selection(self):
		while(1):
			selection = input("Please select an open space: ")
			if (self.is_space_occupied(selection)):
				print("Invalid selection. Try again")
			else :
				return selection

	def get_open(self):
		result = []
		for space in range(0,9):
			if (self.board[space].isdigit() and int(self.board[space]) in [0, 1, 2, 3, 4, 5, 6, 7, 8]):
				result.append(space)
		# print(result)
		return result

	def game_loop_learn(self, play_order):
		#first run belongs to the AI
		board_info = self.get_open()
		self.pick += 1
		while(True):
			board_info = self.get_open()
			if (self.pick % 2 == 0): #AI goves
				pick = self.ai_plr.populate_memory(board_info, self.pick <= 2, play_order)
				self.board[pick] = 'O'
			else: #random goes
				pick = rnd_player.select_move(board_info)
				self.board[pick] = 'X'
				self.ai_plr.set_opps_pos(pick)
			self.pick += 1
			mark = self.board[pick]
			if(self.check_for_win(self.board, mark)):
				# print(mark + " wins!")
				if (mark == "X"):
					return 2
				elif (mark == "O"):
					return 1
			elif(self.check_for_draw(self.board)):
				# print("Draw")
				return 0

	#the AI is overwrwiting moves by going first
	def game_loop_play(self, play_order):
		board_info = self.get_open()
		# self.print_board()
		self.pick += 1
		while(True):
			board_info = self.get_open()
			self.print_board()
			if (self.pick % 2 == 0): #AI goves
				print("AI is thinking")
				time.sleep(1)
				pick = self.ai_plr.play_game_second(board_info, self.pick <= 2)
				self.board[pick] = 'O'
				print("O picked: " + str(pick))
			else: #random goes
				pick = int(self.ask_for_selection())
				self.board[pick] = 'X'
				self.ai_plr.set_opps_pos(pick)
			self.pick += 1
			mark = self.board[pick]
			if(self.check_for_win(self.board, mark)):
				self.print_board()
				print(mark + " wins!")
				if (mark == "X"):
					return 2
				elif (mark == "O"):
					return 1
			elif(self.check_for_draw(self.board)):
				self.print_board()
				print("Draw")
				return 0



ai_player = TTT_ai()
rnd_player = random_player()
results = [0, 0, 0]


# print("Game: 1")
board = Overseer(rnd_player, ai_player)
# board.print_board()
res = board.game_loop_learn(False)
ai_player.finalize_score(res)
results[res] += 1
for x in range(2,700000):
	if (x % 10000 == 0):
		print("Game: " + str(x))
	board = Overseer(rnd_player, ai_player)
	# board.print_board()
	res = board.game_loop_learn(False)
	ai_player.finalize_score(res)
	results[res] += 1


# for x in range(2,600000):
# 	if (x % 10000 == 0):
# 		print("Game: " + str(x))
# 	board = Overseer(rnd_player, ai_player)
# 	# board.print_board()
# 	res = board.game_loop_learn(False)
# 	ai_player.finalize_score(res)
# 	results[res] += 1

ai_player.start_mem_connection(False)

while (True):
	board = Overseer(None, ai_player)
	res = board.game_loop_play(True)
	print(ai_player.last_move.position)
	ai_player.finalize_score(res)
	results[res] += 1

	reply = input("Do you want to continue? (Y | N): ")
	reply = reply.upper()
	if (reply == "N"):
		print("Thanks for playing")
		break


# print("Wins: " + str(results[1]))
# print("Draws: " + str(results[0]))
# print("Losses: " + str(results[2]))
# print((results[0] + results[1])/10000)

# board = Overseer(None, ai_player)