class Node:
	def __init__(self, position, parent):
		self.position = position
		self.parent = parent
		self.wins = 0
		self.losses = 0
		self.draws = 0
		self.final_win = None
		self.children = [[None for x in range(9)] for y in range(9)]

	def __repr__(self):
		return ("Child")
		# return ("W: " + str(self.wins) + " - L: " + str(self.losses) + " - D: " + str(self.draws))
			
	#Getters and setters
	def get_wins(self):
		return self.wins

	def get_losses(self):
		return self.losses

	def get_draws(self):
		return self.draws

	def get_parent(self):
		return self.parent

	def get_position(self):
		return self.position

	def get_children(self):
		return self.children

	def increase_win(self, value):
		self.wins += value

	def increase_loss(self, value):
		self.losses += value

	def increase_draw(self, value):
		self.draws += value

	def add_child(self, child, position):
		self.children[position] = child