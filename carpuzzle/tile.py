from __future__ import annotations
from carpuzzle.slice import CarSlice
from typing import Iterable

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
		"""Permutes the list of elements at the borders clockwisely"""
		self.borders = [self.W, self.S, self.E, self.N] 
		self.orientation  = (self.orientation + 1 ) % 4
		
	def compare(self, other:Tile, cardinal_dir:Iterable)->bool:
		"""Determines whether some other Tile can be a neighbor

		Args:
			other (Tile): Other Tile beign compared to 'self'
			cardinal_dir (Iterable): tuple indicating the relative direction where the other Tile wants to be placed

		Returns:
			bool: True if the other tile is compatible with 'self' when placed on the side indicated by 'cardinal_dir'
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