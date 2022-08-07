
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