from random import randint
from random import choice
from decision_tree import *

"""
The goal for this AI is to implement a complete decision making tree, through trial and error
to beat any opponent in Tic-Tac-Toe. Or at least to never fail and always force a draw.

It does this by documenting its own steps and determining the best posible options given
the current state of the game.
"""
class TTT_ai:
	def __init__(self):
		self.decision_tree = Node(None, None, None, True) #First node is just a place to house the rest of the nodes
		self.last_move = self.decision_tree
		self.first_move = True
		self.old_board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
		self.new_board = [0, 1, 2, 3, 4, 5, 6, 7, 8]

	def make_decision(self, opp_pos, board):
		if (self.first_move): #first move
			self.first_move = False
			return self.random_decision(board)
		elif (self.last_move.children[opp_pos] == None):
			return self.random_decision(board)
		else:
			res = self.last_move.children[opp_pos].get_best_decision()


		if (res == None):
			return self.random_decision(board)			
		elif (res[1] in ["win", "draw"]): #ai in on a non-losing path
			self.last_move = res[0]
			return res[0].get_position()
		else: #no children, or ai failed, pick random
			return self.random_decision(board)

	def random_decision(self, board):
		selection = choice(board)
		move = Node(False, selection, self.last_move, False)
		self.last_move.add_child(move, selection)
		return selection

	def update_last_move(self, position):
		# print(str(position) + " last move")
		# print(self.last_move.children)
		self.last_move = self.last_move.children[position]

	def set_last_move_result(self, value):
		if (value == 1):
			self.last_move.increase_win(1)
		elif (value == 0):
			self.last_move.increase_draw(1)
		else:
			self.last_move.increase_loss(1)
		# self.push_result(self.last_move)

	def update_opponent(self, position):
		# print(self.last_move)
		# print(position)
		move = Node(True, position, self.last_move, False)
		self.last_move.add_child(move, position)

	def reset_game(self):
		while(self.last_move.top != True):
			self.last_move = self.last_move.get_parent()
		# print("in reset")
		# print(self.last_move.children)

	#move the result up the tree, let it know which branches have the most wins
	def push_result(self, leaf):
		parent = leaf.get_parent()
		# print(leaf)
		while(parent != None):
			parent.increase_win(leaf.get_wins())
			parent.increase_loss(leaf.get_losses())
			parent.increase_draw(leaf.get_draws())
			leaf = parent
			parent = leaf.get_parent()