import numpy as np
import pandas as pd


class Square:
	"""
	Object used to represent one squared tile of the puzzle. 

	Each Square has one label in each of its four sides. This labels are stored in a list of strings

	"""
	def __init__(self, borders, id="0"):
		self.borders = borders #N W S E
		self.id = id
	
	@property
	def N(self):
		return self.borders[0]
	@property
	def W(self):
		return self.borders[1]
	@property
	def S(self):
		return self.borders[2]
	@property
	def E(self):
		return self.borders[3]

	def rotate(self):
		"""permute cyclically the labels of the sides"""
		self.borders = [self.W, self.S, self.E, self.N]   
		
	def compare(self, other_square, cardinal_dir):
		cardinal_dir = tuple(cardinal_dir)
		if cardinal_dir == (1,0):
			# tengo que comparar mi S con tu N
			return (self.S[0] == other_square.N[0]) and (self.S[1] != other_square.N[1]) 
		elif cardinal_dir == (-1, 0):
			# tengo que comparar mi N con tu S
			return (self.N[0] == other_square.S[0]) and (self.N[1] != other_square.S[1])
		elif cardinal_dir == (0,1):
			# tengo que comparar mi E con tu W
			return (self.E[0] == other_square.W[0]) and (self.E[1] != other_square.W[1]) 
		elif cardinal_dir == (0,-1):
			# tengo que comparar mi W con tu E
			return (self.W[0] == other_square.E[0]) and (self.W[1] != other_square.E[1])

		else:
			raise Exception
	
	def __repr__(self):
		string = "  " + self.N + "\n"
		string += self.W  +"  " +self.E + "\n"
		string += "  " + self.S
		return string
	
	def string_list(self):	 
		return ["  " + self.N + "  ", self.W + "  " + self.E , "  "+ self.S + "  "]
	
class Board:
	def __init__(self, shape):
		self.array = np.array([None for i in range(shape[0]*shape[1])]).reshape(shape)
		self.shape = shape
	

	def get_adjacent_indices(self, current_pos):
		# returns list of tuples of indices which ...
		neighbours = []
		cardinal_dirs = [ np.asarray(tup) for tup in [(1,0), (-1,0), (0,1),(0,-1)]]

		for dir in cardinal_dirs:
			neighbour = np.asarray(current_pos) + dir # Northern, Southern, Easter and western neighbour
			if 0<= neighbour[0] < self.shape[0] and 0<= neighbour[1] < self.shape[1]:
				# neighbour is within bounds of the board
				neighbours.append((tuple(neighbour), dir))
		return neighbours

	def is_compatible(self, square, position):
		"""return True if the square is compatible with the board when fixed in postion for some orientation"""
		self.array[position] = square
		for i in range(4):
			# each of the four orientations
			square.rotate()
			if self.is_compatible_board():
				return True
		self.array[position] = None
		return False

	def is_compatible_board(self):
		"""return True if the board is in a compatible configuration"""

		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				# compare all connections of the square in pos i,j
				current_pos = (i,j)
				current_square = self.array[i,j]

				if current_square is not None: # is not necessary to check empty entries 

					for (k, l), cardinal_dir in self.get_adjacent_indices(current_pos): # Northern, Southern, Easter and western neighbour
						adjacent_square = self.array[k,l]

						if adjacent_square is not None:
							
							if not current_square.compare(adjacent_square,cardinal_dir):
								"""There is in incompatible conection"""
								return False
		# conditions are satisfied
		return True

	def print_ids(self):
		string = ""
		for row in self.array:
			string += ",".join([c.id if c is not None else "*" for c in row ])+"\n"
		print(string)
		
	def __repr__(self):
		string = ""
		for row in self.array:
			l1 = ""
			l2 = ""
			l3 = ""
			for square in row:
				if square is None:
					sl = ["      "," None ", "      "]
				else:
					sl = square.string_list()
				l1 += sl[0]
				l2 += sl[1]
				l3 += sl[2]
			string += l1 + "\n"+ l2 + "\n" +l3 + "\n"
		return string
	
class Recursive:
	def __init__(self, strategy, path=None, shape=(3,3)):

		#read csv puzzle
		df = pd.read_csv(path, sep="\t")

		# populate the squares
		squares = [] 
		for id, row in df.iterrows():
			square = Square([row.N, row.W, row.S, row.E], id=str(id))
			squares.append(square)
		np.random.shuffle(squares)

		#instantiate board
		self.strategy = strategy
		self.squares = set(squares) # populate squares
		self.board = Board(shape)

		self.counter = 0 # counts the number of recursive calls to measure performance

	
	def depth_search(self, depth = 0, squares_visited = set()):
		self.counter += 1

		if depth == len(self.strategy):
			return True
		else:
			pass
			# print("depth", depth, "pos", self.strategy[depth])
			# self.board.print_ids()

		current_pos = self.strategy[depth]

		for square in self.squares - squares_visited:

			if self.board.is_compatible(square, current_pos):
				branch_has_future = self.depth_search(depth = depth+1,squares_visited = squares_visited.union(set([square])))

				if branch_has_future:
					return True
				else:
					self.board.array[current_pos] = None
		return False



# initialize the solver
strategy = [(1,1), (0,1), (1,0), (1,2), (2,1), (0,0), (0,2) , (2,0), (2,2)]

# strategy.reverse()

suma = 0
n=1
for i in range(n):

	r = Recursive(strategy,path = "data.tsv", shape=(3,3))

	# run
	r.depth_search()
	print(r.board)

	suma += r.counter

print(suma/n)

# combs = 9*8*7*6*5*4*3*2
# combs *= 4**9

# print(4 / combs)

#print(r.board.is_compatible_board())


