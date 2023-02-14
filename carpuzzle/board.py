from __future__ import annotations

import numpy as np
import pandas as pd

from carpuzzle.tile import Tile


class Board:
	"""Represents the board of the puzzle where the tiles must be placed
	"""
	cardinal_dirs = [ np.asarray(tup) for tup in [(1,0), (-1,0), (0,1),(0,-1)]] # list of the cardinal directions

	def __init__(self, shape:tuple)->None:
		"""Initializes the empty board

		Args:
			shape (tuple): tuple indicating the dimensions of the board: (n rows , n columns)
		"""
		self.array = np.array([None for _ in range(shape[0]*shape[1])]).reshape(shape) # initially empty array of the board, where the tiles will be placed
		self.shape = shape # shape of the board
		self.list_pos = [(i,j) for i in range(self.shape[0]) for j in range(self.shape[1])] # list of all the coordinates of the board

	
	def get_adjacent_indices(self, current_pos:tuple)->list:
		""" Returns the coordinates of the adjacent tiles to the current position

		Args:
			current_pos (tuple): tuple or coordinates (row, column)

		Returns:
			list: list of pairs ('coordinate', 'direction') such that when moving from 'current_pos' in 'direction', one obtains 'coordinate'
		"""
		neighbours = [] 
		for dir in self.cardinal_dirs:
			neighbour = np.asarray(current_pos) + dir # Northern, Southern, Easter and Western neighbour's coordinates
			if 0<= neighbour[0] < self.shape[0] and 0<= neighbour[1] < self.shape[1]: # check whether the coordinates are within the bounds of the board
				neighbours.append((tuple(neighbour), dir))
		return neighbours

	def is_compatible_tile(self, tile:Tile, coordinate:tuple)->bool:
		"""Checks wheter some tile is compatible with the current state of the board. If there is some compatible orientation of the tile in board, the tile is added to the board

		Args:
			tile (Tile): tile to be checked
			coordinate (tuple): coordinate in which the tile wants to be placed

		Returns:
			bool: True if under some orientation of the tile, in the coordinate the resultant board is compatible. False otherwise.
		"""
		self.array[coordinate] = tile # add the tile to the board
		for _ in range(4):
			# for each of the four possible orientations of the tile
			tile.rotate()
			if self.is_compatible_board(): # check if the resultant board is compatible
				return True # in that case return True
		# if the tile isn't compatible, remove it from the board
		self.array[coordinate] = None
		return False #...and return False

	def is_compatible_board(self)->True:
		""" Checks whether the current state of the board is compatible. Makes approx. O(N*M*4) comparisons, where N / M are the number of rows / columns

		Returns: True if the board is in a compatible configuration with the current tiles 
		"""
		for i,j in self.list_pos:
			# compare all connections of the tile in pos i,j
			current_pos = (i,j)
			current_tile = self.array[i,j]

			if current_tile is not None: # is not necessary to check empty entries of the board

				for (k, l), cardinal_dir in self.get_adjacent_indices(current_pos): # Northern, Southern, Easter and Western neighbour's

					adjacent_tile = self.array[k,l]

					if adjacent_tile is not None:
						if not current_tile.compare(adjacent_tile,cardinal_dir): # check if there is in incompatible conection
							return False
		# all connections are compatible
		return True

	def get_permutation(self):
		"""Auxiliary function that returns the permutation coresponding to the tiles in the board. We use the id of each tile as the permutation element. This is used to rearange the tiles in the board to the correct order"""
		pi = []
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				pi.append(self.array[i,j].id)
		return pi 
			
	def print_ids(self):
		"""Prints the id of each tile in the board. If there is no tile in a position, prints a *
		"""
		string = ""
		for row in self.array:
			string += ",".join([str(c.id) if c is not None else "*" for c in row ])+"\n"
		print(string)
		
	def __repr__(self)->str:
		"""Returns a string representation of the board
		"""
		string = ""
		for row in self.array:
			l1 = ""
			l2 = ""
			l3 = ""
			for tile in row:
				if tile is None:
					sl = ["      "," None ", "      "]
				else:
					sl = tile.string_list()
				l1 += sl[0]
				l2 += sl[1]
				l3 += sl[2]
			string += l1 + "\n"+ l2 + "\n" +l3 + "\n"
		return string