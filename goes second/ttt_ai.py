from random import randint
from random import choice
from decision_tree import *
from random import choice
import pdb

"""
The goal for this AI is to implement a complete decision making tree, through trial and error
to beat any opponent in Tic-Tac-Toe. Or at least to never fail and always force a draw.

It does this by documenting its own steps and determining the best posible options given
the current state of the game.
"""
class TTT_ai:
	def __init__(self):
		self.dt_0 = Node(0, None)
		self.dt_1 = Node(1, None)
		self.dt_2 = Node(2, None)
		self.dt_3 = Node(3, None)
		self.dt_4 = Node(4, None)
		self.dt_5 = Node(5, None)
		self.dt_6 = Node(6, None)
		self.dt_7 = Node(7, None)
		self.dt_8 = Node(8, None)

		self.dt_array = [self.dt_0, self.dt_1, self.dt_2, self.dt_3, self.dt_4, self.dt_5, self.dt_6, self.dt_7, self.dt_8]

		self.play_tree = [None, None, None]
		self.last_move = None
		self.current_tree = None
		self.opps_pos = None #needs to update everytime the opponent makes a move

		self.best_tree = None #which tree is the best to start in?

	def population_memory(self, board, first):
		pick = choice(board)
		self.update_memory(pick, first)
		return pick

	def update_memory(self, pick, first, turn = 0):
		if (first): #Everytime we first start it picks a random spot, and goes to that tree, we're trying to identify the best starting position
			self.current_tree = self.dt_array[self.opps_pos]
			self.last_move = self.current_tree #the move we just took was into the top of the current_tree

		if (self.last_move.children[self.opps_pos][pick] == None): #we're making a new move, tag it and move on
			move = Node(pick, self.last_move)
			self.last_move.children[self.opps_pos][pick] = move
			self.last_move = self.last_move.children[self.opps_pos][pick]
		else: #our pick was something old, move into it and continue
			self.last_move = self.last_move.children[self.opps_pos][pick]

	#at the end of the game this gets called and the last_move node updates to reflect the outcome
	def finalize_score(self, result, player):
		comp = self.last_move.wins + self.last_move.losses + self.last_move.draws
		# print(result)
		# print(player)
		if (player and result != 0 and result != 1):
			while(self.last_move != None):
				self.last_move.losses += 10 #this means we'll have a definite outcome, not aggregates growing out of control
				self.last_move = self.last_move.parent #move up into the parent
			return

		if (comp != 0): #if it isn't 0 we've already been here, logged it, and push it up the stack. This should not happen again
			return

		if (result == 1):
			self.last_move.wins = 1
			self.last_move.final_win = True
		elif (result == 0):
			self.last_move.draws = 1
		else:
			self.last_move.losses = 1
			self.last_move.final_win = False

		win = self.last_move.wins #document what happened
		draw = self.last_move.draws
		lose = self.last_move.losses
		self.last_move = self.last_move.parent
		while(self.last_move != None):
			# pdb.set_trace()
			self.last_move.wins += win #update the parent with whatever happened
			self.last_move.draws += draw #we're only changing the one variable, and only by 1
			self.last_move.losses += lose #this means we'll have a definite outcome, not aggregates growing out of control
			self.last_move = self.last_move.parent #move up into the parent

	#now we're actually playing the game, access the memory
	#start_mem_connection has already been called by this point
	#so we need only to access the play_tree
	def play_game(self, board, first):
		if (first):
			self.last_move = self.dt_array[self.opps_pos] #move last_move into the play tree and begin

		best_pick = self.get_best(self.last_move.children[self.opps_pos])
		if (best_pick == None):
			pick = choice(board)
			self.update_memory(pick, first)
			return pick
		else:
			self.last_move = best_pick
			return self.last_move.position

	def get_best(self, chl_array):
		non_losses = 0
		ret_tree = None
		losses = 10**10
		loss_tree = None

		exists = True
		for x in chl_array:
			if(x != None):
				exists = False

		#none of the children existed, we never hit this.
		if(exists):
			return None

		i = 0
		for decision in chl_array:
			if (decision == None):
				continue

			if (decision.final_win == True):
				return decision

			comp = (decision.wins + decision.draws) - decision.losses
			# print("Comp: " + str(comp) + " -- Losses: " + str(decision.losses) + " -- Position: " + str(decision.position))
			if (comp >= non_losses): #find the tree with the most wins + draws, we're aiming to not lose, not necessarily to win
				non_losses = comp
				ret_tree = decision
			elif (decision.losses <= losses): #even if there are no wins, let's get the least losses (mostly just to catch if we fall down a failuer tree)
				losses = decision.losses
				loss_tree = decision
			i += 1

		if (ret_tree == None):
			return loss_tree
		else:
			return ret_tree
			
	def start_mem_connection(self):
		non_losses = 0
		ret_tree = [self.dt_array[0], self.dt_array[4], self.dt_array[8]]
		for tree in self.dt_array:
			comp = (tree.wins + tree.draws)
			if (comp > non_losses): #find the tree with the most wins + draws, we're aiming to not lose, not necessarily to win
				non_losses = comp
				ret_tree[2] = ret_tree[1]
				ret_tree[1] = ret_tree[0]
				ret_tree[0] = tree
		self.play_tree = ret_tree

	def set_opps_pos(self, position):
		self.opps_pos = position