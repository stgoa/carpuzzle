from __future__ import annotations
from typing import Iterable
import numpy as np
import pandas as pd



class CarSlice:
	"""Represents a car slice within the tiles' borders
	"""
	def __init__(self, color:str, car_type:str) -> None:
		"""Initialize the class

		Args:
			color (str): string representing the color of the car: 'R' (red), 'G' (green), 'B' (blue) or 'Y' (yellow)
			car_type (str): string representing if the car slice is either front ('F') or back ('B')
		"""
		self.color = color
		self.type = car_type

	def __repr__(self) -> str:
		return self.color + self.type

class Tile:
	"""Represents a tile of the puzzle
	"""
	def __init__(self, borders:list, id:int)->None:
		"""Initialize the class

		Args:
			borders (list): list conaining the CarSlice objects in the order [ North (top), West (left), South (bottom),  East (right) ]
			id (int): unique integer used to identify the tile
		"""
		self.borders = borders
		self.id = id
		self.orientation = 0
	
	@property
	def N(self)->CarSlice:
		"""Gets the Northern border

		Returns:
			CarSlice: Northern border
		"""
		return self.borders[0]
	@property
	def W(self)->CarSlice:
		"""Gets the Western border

		Returns:
			CarSlice: Western border
		"""
		return self.borders[1]
	@property
	def S(self)->CarSlice:
		"""Gets the Southern border

		Returns:
			CarSlice: Southern border
		"""
		return self.borders[2]
	@property
	def E(self)->CarSlice:
		"""Gets the Eastern border

		Returns:
			CarSlice: Eastern border
		"""
		return self.borders[3]

	def rotate(self)->None:
		"""Permutes the list of elements at the borders cyclically"""
		self.borders = [self.W, self.S, self.E, self.N] 
		self.orientation  = (self.orientation + 1 ) % 4
		
	def compare(self, other:Tile, cardinal_dir:Iterable)->bool:
		"""Determine whether some other Tile can be a neighbors

		Args:
			other (Tile): Other Tile beign compared to self
			cardinal_dir (Iterable): tuple indicating the relative direction where the other Tile wants to be placed

		Returns:
			bool: True if the other tile is compatible with self when placed on the side indicated by cardinal_dir
		"""
		cardinal_dir = tuple(cardinal_dir)
		if cardinal_dir == (1,0):
			# compare the Southern border of 'self' with the Northern border of 'other'
			return (self.S.color == other.N.color) and (self.S.type != other.N.type) 
		elif cardinal_dir == (-1, 0):
			# compare the Northern border of 'self' with the Southern border of 'other'
			return (self.N.color == other.S.color) and (self.N.type != other.S.type)
		elif cardinal_dir == (0,1):
			# compare the Eastern border of 'self' with the Western border of 'other'
			return (self.E.color == other.W.color) and (self.E.type != other.W.type) 
		elif cardinal_dir == (0,-1):
			# compare the Western border of 'self' with the Eastern border of 'other'
			return (self.W.color == other.E.color) and (self.W.type != other.E.type)

	
	def __repr__(self)->str:
		string = "  " + self.N.__repr__() + "\n"
		string += self.W.__repr__()  +"  " +self.E.__repr__() + "\n"
		string += "  " + self.S.__repr__()
		return string
	
	def string_list(self)->list:	 
		return ["  " + self.N.__repr__() + "  ", self.W.__repr__() + "  " + self.E.__repr__() , "  "+ self.S.__repr__() + "  "]
	
class Board:
	"""Represents the board of the puzzle where the tiles must be placed
	"""
	cardinal_dirs = [ np.asarray(tup) for tup in [(1,0), (-1,0), (0,1),(0,-1)]]

	def __init__(self, shape:tuple)->None:
		"""Initializes the empty board

		Args:
			shape (tuple): tuple indicating the dimensions of the board: (n rows , n columns)
		"""
		self.array = np.array([None for _ in range(shape[0]*shape[1])]).reshape(shape) # initially empty array where the tiles will be placed
		self.shape = shape # dimensions of the board
		self.list_pos = [(i,j) for i in range(self.shape[0]) for j in range(self.shape[1])] # list of all coordinates of the board

	
	def get_adjacent_indices(self, current_pos:tuple)->list:
		"""Given some coordinates, returns a list of all adjacent coordinates 
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

	def is_compatible_tile(self, tile:Tile, position:tuple)->bool:
		"""Checks wheter some tile is compatible with the current state of the board. If there is some compatible orientation of the tile in board, the tile is added to the board

		Args:
			tile (Tile): tile to be checked
			position (tuple): position in which the tile wants to be placed

		Returns:
			bool: True if under some orientation of the tile in the position, the resultant board is compatible. False otherwise.
		"""
		self.array[position] = tile
		for _ in range(4):
			# each of the four orientations
			tile.rotate()
			if self.is_compatible_board():
				return True
		# if the tile isn't compatible, remove it from the board
		self.array[position] = None
		return False

	def is_compatible_board(self)->True:
		"""Makes around O(N*M*4) comparisons, where N / M are the number of rows / columns

		Returns: True if the board is in a compatible configuration with the current tiles 
		"""
		for i,j in self.list_pos:
			# compare all connections of the tile in pos i,j
			current_pos = (i,j)
			current_tile = self.array[i,j]

			if current_tile is not None: # is not necessary to check empty entries of the board

				for (k, l), cardinal_dir in self.get_adjacent_indices(current_pos): # Northern, Southern, Easter and western neighbour's

					adjacent_tile = self.array[k,l]

					if adjacent_tile is not None:
						if not current_tile.compare(adjacent_tile,cardinal_dir): # check if there is in incompatible conection
							return False
		# all connections are compatible
		return True

	def get_permutation(self):
		pi = []
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				pi.append(self.array[i,j].id)
		return pi 
			
	def print_ids(self):
		string = ""
		for row in self.array:
			string += ",".join([str(c.id) if c is not None else "*" for c in row ])+"\n"
		print(string)
		
	def __repr__(self)->str:
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