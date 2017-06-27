class Overseer:
	def __init__(self):
		self.board = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
		self.winning_combos = ([0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [2, 4, 6], [0, 4, 8])
		self.pick = 0
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

	def game_loop(self):
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

board = Overseer()
board.print_board()
board.game_loop()
