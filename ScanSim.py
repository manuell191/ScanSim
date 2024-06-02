import random

class ScanSim:
	def __init__(self) -> None:
		self.upper_bound = 9.3
		self.lower_bound = 0.3
		self.half_range = ((self.upper_bound - self.lower_bound) / 2)

	# Calculate y, given an x value
	# return y value (float)
	def calc_y(self, x: float) -> float:
		y = x**10 - 49.5*(x**9) + 1063.03*(x**8) - 12981.935*(x**7) + 99239.3917*(x**6) - 492186.36785*(x**5) + 1585470.496893*(x**4) - 3218089.1724245*(x**3) + 3821229.8104174*(x**2) - 2249281.4285439*x + 406046.27998575
		return y

	# Generate a random value for x, then return x, y coordinate values
	# return x, y coordinates (float, float)
	def calc(self) -> tuple[float, float]:
		x = random.random() * (self.upper_bound - self.lower_bound) + self.lower_bound
		return x, self.calc_y(x)

	# runs self.calc for sim_iters(int) and returns all calculation results
	# returns array in format: [(x1, y1), (x2, y2)...], max x, y coordinates (float, float)
	def scan(self, sim_iters: int) -> tuple[list[list[float, float]], float]:
		calc_results = []
		max_x = 9.01 # arbritrary at minima 
		for i in range(sim_iters):
			calc_results.append(self.calc())
			if calc_results[-1][1] > self.calc_y(max_x): # if most recently added y value is less than current max y value
				max_x = calc_results[-1][0] # set to x of most recently added point
		return calc_results, max_x, self.calc_y(max_x)

	# takes current half range, and takes away decay rate % from the half range
	# returns new half range (float)
	def decay(self, decay_rate: float) -> float:
		self.half_range = self.half_range - (self.half_range * decay_rate)
		return self.half_range

	# with x being the current known max point, gets a new upper and lower bound
	# returns a new upper and lower bound (float, float)
	def get_bounds(self, x: float) -> None:
		self.upper_bound = x + self.half_range
		self.lower_bound = x - self.half_range
		move_range = 0

		if self.upper_bound > 9.3:
			move_range = self.upper_bound - 9.3
			self.upper_bound = 9.3
			self.lower_bound -= move_range
		if self.lower_bound < 0.3:
			move_range = -(self.lower_bound - 0.3)
			self.lower_bound = 0.3
			self.upper_bound += move_range
		return
	
	# resets to scan defaults, for starting a new scan
	def reset(self) -> None:
		self.upper_bound = 9.3
		self.lower_bound = 0.3
		self.half_range = ((self.upper_bound - self.lower_bound) / 2)