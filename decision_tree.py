class Node:
	def __init__(self):
		self.wins = 0
		self.losses = 0
		self.draws = 0
		self.children = []

	def __repr__(self):
		return ("Wins: " + str(self.wins) + " - Losses: " + str(self.losses) + " - Draws: " + str(self.draws))

	def get_wins(self):
		return self.wins

	def get_losses(self):
		return self.losses

	def get_draws(self):
		return self.draws