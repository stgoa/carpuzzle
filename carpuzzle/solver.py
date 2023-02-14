from __future__ import annotations


import numpy as np
import pandas as pd

from carpuzzle.board import Board
from carpuzzle.slice import CarSlice
from carpuzzle.tile import Tile


class Recursive:
	"""This class is the actual solver. Handles the initialization and runs the algorithm"""
	def __init__(self, strategy:list, path:str, shape:tuple=(3,3))->None:
		"""Initializes the solver

		Args:
			strategy (list): list or coordinates (tuples) indicating the order of fullfilment of the entries of the board.
			path (str): string with the name of the file with the input data
			shape (tuple, optional): shape of the board. Defaults to (3,3).
		"""

		# read the input data
		df = pd.read_csv(path, sep="\t")

		# create the tiles
		tiles = [] 
		for id, row in df.iterrows():
			borders = []
			for string in [row.N, row.W, row.S, row.E]:
				carslice = CarSlice(color=string[0], car_type=string[1])
				borders.append(carslice)
			tile = Tile(borders=borders, id=id)
			tiles.append(tile)

		# create the board
		self.board = Board(shape)

		self.tiles = set(tiles) # set of tiles to be placed
		self.strategy = strategy # strategy of placement
		self.counter = 0 # counter of the number of calls of the function

	
	def backtracking(self, depth:int = 0, tiles_visited:set = set())->bool:
		""" Recursive function that implements the backtracking algorithm to solve the puzzle

		Args:
			depth (int, optional): Indicates the current recursion level. Defaults to 0.
			tiles_visited (set, optional): Set of tiles that already had been visited. Defaults to set().

		Returns:
			bool: True if the puzzle has a solution. False otherwise.
		"""
		self.counter += 1 # count the number of call of the function

		if depth == len(self.strategy): # if the depth is equal to the number of entries of the board, then the puzzle is solved
			return True

		current_pos = self.strategy[depth] # obtain the current position to be filled

		un_visited_tiles = self.tiles - tiles_visited # obtain the set of tiles that have not been visited yet

		for tile in un_visited_tiles:
			if self.board.is_compatible_tile(tile, current_pos): # check if the tile is compatible with the current position
				# recursive call 
				branch_has_future = self.backtracking(depth = depth+1,tiles_visited = tiles_visited.union({tile})) # the method 'add' operates inplace, so here we need union

				if branch_has_future: # if the branch has future, then the tile can be placed in the current position
					return True
				else: # if the branch has no future, then the tile cannot be placed in the current position
					# delete the tile form the current coordinate being checked
					self.board.array[current_pos] = None 

		# if the function reaches this point, then the puzzle has no solution with the current strategy and state of the board
		return False


if __name__ == "__main__":
	
	# initialize the solver using the optimal strategy
	strategy = [(1,1), (0,1), (1,0), (1,2), (2,1), (0,0), (0,2) , (2,0), (2,2)]
	solver = Recursive(strategy,path = "data/data.tsv", shape=(3,3))

	# run
	solver.backtracking()
	print(solver.board)
	print(solver.board.print_ids())
	print(solver.board.is_compatible_board())