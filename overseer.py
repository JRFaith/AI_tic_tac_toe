from ttt_ai import *
from randomP1 import *
from decision_tree import *

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

	def game_loop2(self):
		running = True
		while(running):
			user_pick = int(self.ask_for_selection())
			if(self.pick % 2 == 0):
				self.board[user_pick] = 'X'
			else:
				self.board[user_pick] = 'O'
			self.pick += 1
			self.print_board()
			mark = self.board[user_pick]
			if(self.check_for_win(self.board, mark)):
				print(mark + " wins!")
				break
			elif(self.check_for_draw(self.board)):
				print("Draw")
				break

	def game_loop(self):
		running = True
		pick = self.ai_plr.make_decision(0, [0,1,2,3,4,5,6,7,8]) #first move
		self.ai_plr.update_last_move(pick)
		self.board[pick] = 'X'
		self.pick += 1
		opp_pos = 0;
		while(running):
			board_info = self.get_open()
			if(self.pick % 2 == 0):
				pick = self.ai_plr.make_decision(opp_pos, board_info)
				self.ai_plr.update_last_move(pick)
				self.board[pick] = 'X'
			else:
				pick = rnd_player.select_move(board_info)
				self.ai_plr.update_opponent(pick)
				self.board[pick] = 'O'
				opp_pos = pick
			self.pick += 1
			# self.print_board()
			mark = self.board[pick]
			if(self.check_for_win(self.board, mark)):
				# print(mark + " wins!")
				if (mark == "X"):
					self.ai_plr.set_last_move_result(1)
					return 0
				elif (mark == "O"):
					self.ai_plr.set_last_move_result(2)
					return 2
			elif(self.check_for_draw(self.board)):
				# print("Draw")
				self.ai_plr.set_last_move_result(0)
				return 1
		return

ai_player = TTT_ai()
rnd_player = random_player()
ai_player.reset_game()
results = [0, 0, 0]


# print("Game: 1")
board = Overseer(rnd_player, ai_player)
# board.print_board()
res = board.game_loop()
results[res] += 1
for x in range(2,10000):
	# print("Game: " + str(x))
	ai_player.reset_game()
	board = Overseer(rnd_player, ai_player)
	# board.print_board()
	res = board.game_loop()
	results[res] += 1

print("Wins: " + str(results[0]))
print("Draws: " + str(results[1]))
print("Losses: " + str(results[2]))
print((results[0] + results[1])/10000)
ai_player.reset_game()
print(ai_player.last_move.children[0].children[0])

board = Overseer(None, ai_player)