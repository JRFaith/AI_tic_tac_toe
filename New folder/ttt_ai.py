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
		self.dt_0_f = Node(0, None)
		self.dt_1_f = Node(1, None)
		self.dt_2_f = Node(2, None)
		self.dt_3_f = Node(3, None)
		self.dt_4_f = Node(4, None)
		self.dt_5_f = Node(5, None)
		self.dt_6_f = Node(6, None)
		self.dt_7_f = Node(7, None)
		self.dt_8_f = Node(8, None)

		self.dt_0_s = Node(0, None)
		self.dt_1_s = Node(1, None)
		self.dt_2_s = Node(2, None)
		self.dt_3_s = Node(3, None)
		self.dt_4_s = Node(4, None)
		self.dt_5_s = Node(5, None)
		self.dt_6_s = Node(6, None)
		self.dt_7_s = Node(7, None)
		self.dt_8_s = Node(8, None)

		self.dt_array_f = [self.dt_0_f, self.dt_1_f, self.dt_2_f, self.dt_3_f, self.dt_4_f, self.dt_5_f, self.dt_6_f, self.dt_7_f, self.dt_8_f]
		self.dt_array_s = [self.dt_0_s, self.dt_1_s, self.dt_2_s, self.dt_3_s, self.dt_4_s, self.dt_5_s, self.dt_6_s, self.dt_7_s, self.dt_8_s]

		self.play_tree = [None, None, None]
		self.last_move = None
		self.current_tree = None
		self.opps_pos = None #needs to update everytime the opponent makes a move

		self.best_tree = None #which tree is the best to start in?

	#first here means its first move, play_order == true means they are the first to play
	def populate_memory(self, board, first, play_order):
		pick = choice(board)
		if (play_order):
			self.update_memory(pick, first)
		else:
			self.update_memory_second(pick,first)
		return pick

	#learns to play the game going second
	def update_memory_second(self, pick, first):
		if (first): #Everytime we first start it picks a random spot, and goes to that tree, we're trying to identify the best starting position
			self.current_tree = self.dt_array_s[self.opps_pos]
			self.last_move = self.current_tree #the move we just took was into the top of the current_tree

		if (self.last_move.children[self.opps_pos][pick] == None): #we're making a new move, tag it and move on
			move = Node(pick, self.last_move)
			self.last_move.children[self.opps_pos][pick] = move
			self.last_move = self.last_move.children[self.opps_pos][pick]
		else: #our pick was something old, move into it and continue
			self.last_move = self.last_move.children[self.opps_pos][pick]

	#plays the game with the going_second set of rules
	def play_game_second(self, board, first):
		if (first):
			self.last_move = self.dt_array_s[self.opps_pos] #move last_move into the play tree and begin

		best_pick = self.get_best(self.last_move.children[self.opps_pos])
		if (best_pick == None):
			pick = choice(board)
			self.update_memory_second(pick, first)
			return pick
		else:
			self.last_move = best_pick
			return self.last_move.position

	#learns to play the game going first
	def update_memory(self, pick, first):
		if (first): #Everytime we first start it picks a random spot, and goes to that tree, we're trying to identify the best starting position
			self.current_tree = self.dt_array_f[pick]
			self.last_move = self.current_tree #the move we just took was into the top of the current_tree
			return #we're done, no need to continue
		else: #we're down the tree now, last_move should be where we left off, just made a move and need to move last_move into it
			if (self.last_move.children[self.opps_pos][pick] == None): #we're making a new move, tag it and move on
				move = Node(pick, self.last_move)
				self.last_move.children[self.opps_pos][pick] = move
				self.last_move = self.last_move.children[self.opps_pos][pick]
			else: #our pick was something old, move into it and continue
				self.last_move = self.last_move.children[self.opps_pos][pick]

	#now we're actually playing the game, access the memory
	#start_mem_connection has already been called by this point
	#so we need only to access the play_tree
	def play_game(self, board, first):
		if (first):
			self.last_move = choice(self.play_tree) #move last_move into the play tree and begin
			return self.last_move.position
		else: #opponent just moved, set_opps_pos was called, move into the appropiate child
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
		print(chl_array)

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

			comp = (decision.wins + decision.draws) - decision.losses
			# print(str(comp) + " - comp " + str(i))
			# print(str(decision.losses) + " - losses" + str(i))
			# print("position: " + str(decision.position))
			# i += 1
			if (comp > non_losses): #find the tree with the most wins + draws, we're aiming to not lose, not necessarily to win
				non_losses = comp
				ret_tree = decision
			elif (decision.losses < losses): #even if there are no wins, let's get the least losses (mostly just to catch if we fall down a failuer tree)
				losses = decision.losses
				loss_tree = decision

		if (ret_tree == None):
			return loss_tree
		else:
			return ret_tree
			
	def start_mem_connection(self, first):
		non_losses = 0
		if (first):
			ret_tree = [self.dt_array_f[0], self.dt_array_f[4], self.dt_array_f[8]]
			iterable = self.dt_array_f
		else:
			ret_tree = [self.dt_array_s[0], self.dt_array_s[4], self.dt_array_s[8]]
			iterable = self.dt_array_s
		for tree in iterable:
			comp = (tree.wins + tree.draws)
			if (comp > non_losses): #find the tree with the most wins + draws, we're aiming to not lose, not necessarily to win
				non_losses = comp
				ret_tree[2] = ret_tree[1]
				ret_tree[1] = ret_tree[0]
				ret_tree[0] = tree
		self.play_tree = ret_tree

	#at the end of the game this gets called and the last_move node updates to reflect the outcome
	def finalize_score(self, result):
		comp = self.last_move.wins + self.last_move.losses + self.last_move.draws
		if (comp != 0): #if it isn't 0 we've already been here, logged it, and push it up the stack. This should not happen again
			return

		if (result == 1):
			self.last_move.wins = 1
		elif (result == 0):
			self.last_move.draws = 1
		else:
			self.last_move.losses = 1

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

	def set_opps_pos(self, position):
		self.opps_pos = position