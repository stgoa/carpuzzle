from __future__ import annotations
from typing import Iterable

import numpy as np
import pandas as pd

from carpuzzle.slice import CarSlice
from carpuzzle.tile import Tile
from carpuzzle.board import Board



	
	
class Recursive:
	"""This class is the actual solver. Handles the initialization and runs the algorithm"""
	def __init__(self, strategy:list, path:str, shape:tuple=(3,3))->None:
		"""Initializes the class

		Args:
			strategy (list): list or coordinates (tuples) indicating the order of fullfilment of the entries of the board.
			path (str): string with the name of the file with the input data
			shape (tuple, optional): shape of the board. Defaults to (3,3).
		"""

		#read csv puzzle
		df = pd.read_csv(path, sep="\t")

		# populate the tiles
		tiles = [] 
		for id, row in df.iterrows():
			borders = []
			for string in [row.N, row.W, row.S, row.E]:
				carslice = CarSlice(color=string[0], car_type=string[1])
				borders.append(carslice)
			tile = Tile(borders=borders, id=id)
			tiles.append(tile)

		#initiallize the board
		self.board = Board(shape)

		self.tiles = set(tiles) # populate the tiles
		self.strategy = strategy
		self.counter = 0

	
	def depth_search(self, depth:int = 0, tiles_visited:set = set())->bool:
		"""Depth search first for the finding of a branch of tiles that solves the puzzle

		Args:
			depth (int, optional): Indicates the current recursion level. Defaults to 0.
			tiles_visited (set, optional): Set of tiles that already had been visited. Defaults to set().

		Returns:
			bool: True if such branch has been found, False otherwise.
		"""
		self.counter += 1 # count the number of call of the function

		if depth == len(self.strategy): # ending case
			return True

		current_pos = self.strategy[depth] # obtain the coordinates of the next entry of the board to fill

		un_visited_tiles = self.tiles - tiles_visited # obtain the set of unvisited tiles

		for tile in un_visited_tiles:
			if self.board.is_compatible_tile(tile, current_pos):
				# recursive call 
				branch_has_future = self.depth_search(depth = depth+1,tiles_visited = tiles_visited.union({tile})) # the method 'add' operates inplace, so here we need union

				if branch_has_future:
					return True
				else:
					# delete the tile form the current coordinate being checked
					self.board.array[current_pos] = None

		# if none of the tiles was fit for the current position, then this branch of exploration has no future
		return False


if __name__ == "__main__":
	
	# initialize the solver using the optimal strategy
	strategy = [(1,1), (0,1), (1,0), (1,2), (2,1), (0,0), (0,2) , (2,0), (2,2)]
	solver = Recursive(strategy,path = "data.tsv", shape=(3,3))

	# run
	solver.depth_search()
	print(solver.board)
	print(solver.board.print_ids())
	print(solver.board.is_compatible_board())