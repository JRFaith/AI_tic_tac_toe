from random import choice

#not a smart player, but it gets the job done
class random_player:
	def __init__(self):
		self.occupied = False


	def select_move(self, board):
		pick = choice(board)
		# print("O: " + str(pick))
		return pick