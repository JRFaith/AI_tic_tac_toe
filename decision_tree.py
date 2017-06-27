class Node:
	def __init__(self, opponent, position, parent, top):
		self.opponent_turn = opponent
		self.position = position
		self.parent = parent
		self.top = top
		self.wins = 0
		self.losses = 0
		self.draws = 0
		self.children = [None] * 9

	def __repr__(self):
		return ("Child")
		# return ("W: " + str(self.wins) + " - L: " + str(self.losses) + " - D: " + str(self.draws))

	#this will grab the child with the most wins and the one with the most draws
	#returning the best option, the path with the greatest possible options to not fail
	def get_best_decision(self):
		best_win = 0
		win_node = None
		best_draw = 0
		draw_node = None

		exists = True
		for x in range(0,8):
			if(self.children[x] != None):
				exists = False

		if(exists):
			return None

		for decisions in self.children:
			if (decisions == None):
				continue

			d_wins = decisions.get_wins()
			d_draw = decisions.get_draws()
			if (d_wins > best_win):
				best_win = d_wins
				win_node = decisions

			if (d_draw > best_draw):
				best_draw = d_draw
				draw_node = decisions

		if (best_draw > best_win): #if there is a better chance to draw than to win, draw
			return [draw_node, "draw"]
		
		if (best_win > 0):
			return [win_node, "win"]
		elif (best_draw > 0):
			return [draw_node, "draw"]
		else:
			return [None, "loss"]
			
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