import numpy as np
import pandas as pd



cardinal_dirs = [ np.asarray(tup) for tup in [(1,0), (-1,0), (0,1),(0,-1)]]

class Car:
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
		
	def compare(self, other_car, cardinal_dir):
		cardinal_dir = tuple(cardinal_dir)
		if cardinal_dir == (1,0):
			# tengo que comparar mi S con tu N
			return (self.S[0] == other_car.N[0]) and (self.S[1] != other_car.N[1]) 
		elif cardinal_dir == (-1, 0):
			# tengo que comparar mi N con tu S
			return (self.N[0] == other_car.S[0]) and (self.N[1] != other_car.S[1])
		elif cardinal_dir == (0,1):
			# tengo que comparar mi E con tu W
			return (self.E[0] == other_car.W[0]) and (self.E[1] != other_car.W[1]) 
		elif cardinal_dir == (0,-1):
			# tengo que comparar mi W con tu E
			return (self.W[0] == other_car.E[0]) and (self.W[1] != other_car.E[1])

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
		self.list_pos = [(i,j) for i in range(self.shape[0]) for j in range(self.shape[1])]

	

	def get_adjacent_indices(self, current_pos):
		# returns list of tuples of indices which ...
		neighbours = [] 
		for dir in cardinal_dirs:
			neighbour = np.asarray(current_pos) + dir # Northern, Southern, Easter and western neighbour
			if 0<= neighbour[0] < self.shape[0] and 0<= neighbour[1] < self.shape[1]:
				# neighbour is within bounds of the board
				neighbours.append((tuple(neighbour), dir))
		return neighbours

	def is_compatible(self, car, position):
		"""return True if the car is compatible with the board when fixed in postion for some orientation"""
		self.array[position] = car
		for i in range(4):
			# each of the four orientations
			car.rotate()
			if self.is_compatible_board():
				return True
		self.array[position] = None
		return False

	def is_compatible_board(self):
		"""return True if the board is in a compatible configuration"""

		for i,j in self.list_pos:
			# compare all connections of the car in pos i,j
			current_pos = (i,j)
			current_car = self.array[i,j]

			if current_car is not None: # is not necessary to check empty entries 

				for (k, l), cardinal_dir in self.get_adjacent_indices(current_pos): # Northern, Southern, Easter and western neighbour
					adjacent_car = self.array[k,l]

					if adjacent_car is not None:
						
						if not current_car.compare(adjacent_car,cardinal_dir):
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
			for car in row:
				if car is None:
					sl = ["      "," None ", "      "]
				else:
					sl = car.string_list()
				l1 += sl[0]
				l2 += sl[1]
				l3 += sl[2]
			string += l1 + "\n"+ l2 + "\n" +l3 + "\n"
		return string
	
class Recursive:
	def __init__(self, strategy, path=None, shape=(3,3)):

		#read csv puzzle
		df = pd.read_csv(path, sep="\t")

		# populate the cars
		cars = [] 
		for id, row in df.iterrows():
			car = Car([row.N, row.W, row.S, row.E], id=str(id))
			cars.append(car)

		#instantiate board
		self.strategy = strategy
		self.cars = set(cars) # populate cars
		self.board = Board(shape)

		self.counter = 0

	
	def depth_search(self, depth = 0, cars_visited = set()):
		self.counter += 1

		if depth == len(self.strategy):
			return True
		else:
			pass
			# print("depth", depth, "pos", self.strategy[depth])
			# self.board.print_ids()

		current_pos = self.strategy[depth]

		

		un_visited_cars = list(self.cars - cars_visited)

		un_visited_cars  = [un_visited_cars[i] for i in np.random.permutation(len(un_visited_cars))]

		for car in un_visited_cars:

			if self.board.is_compatible(car, current_pos):
				branch_has_future = self.depth_search(depth = depth+1,cars_visited = cars_visited.union(set([car])))

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

	r = Recursive(strategy,path = "carcomb - original.tsv", shape=(3,3))

	# run
	r.depth_search()
	# print(r.board)

	suma += r.counter

print(suma/n)

# combs = 9*8*7*6*5*4*3*2
# combs *= 4**9

# print(4 / combs)

#print(r.board.is_compatible_board())


