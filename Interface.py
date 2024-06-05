import sys
import os, shutil
import statistics
import numpy as np
import matplotlib.pyplot as plt
from ScanSim import ScanSim

'''
sim_iters: how many times will we simulate the same scan
decay_iters: how many times will the algorithm decay (zoom in)
multi_iters: how many iterations of a full scan (Interface.scanData()) will we do
'''


class Interface:
	def __init__(self, sim_iters=5, decay_iters=5, multi_iters=1000, show=False, std_dev_graph=False):
		self.sim_iters = sim_iters
		self.decay_iters = decay_iters
		self.multi_iters = multi_iters
		self.show = show
		self.std_dev_graph = std_dev_graph
		self.scan = ScanSim()

	# gets the average of a multscan's max y value from the before the decay through to the last decay
	def lineGraphCalculator(self, max_history: list[list[float]], max_history_x: list[list[float]]) -> tuple[list[float]]:
		average_values = []
		average_x = []
		final_std_dev = []
		for i in range(len(max_history[0])):
			average = 0
			for j in range(len(max_history)):
				average += max_history[j][i]
			average /= len(max_history)
			average_values.append(average)

		for i in range(len(max_history_x[0])):
			average = 0
			for j in range(len(max_history_x)):
				average += max_history_x[j][i]
			average /= len(max_history_x)
			average_x.append(average)

		for i in range(len(max_history[0])):
			todo_std_dev = []
			for j in range(len(max_history)):
				todo_std_dev.append(max_history[j][i])
			final_std_dev.append(statistics.stdev(todo_std_dev))
		return average_values, average_x, final_std_dev

	# scans a number of self.sim_iters points, then decays a number of self.decay_iters times
	def scanData(self, decay_rate: float) -> tuple[list[float, float], list[float]]:
		overall_max = [0, -999999] # arbritrary low point
		max_change = []
		max_change_x = []
		for i in range(self.decay_iters):
			calc_results, max_x, max_y = self.scan.scan(self.sim_iters)
			if max_y > overall_max[1]:
				overall_max = [max_x, max_y]
			max_change.append(overall_max[1])
			max_change_x.append(overall_max[0])
			print(f"\nOverall max: {overall_max[0]}, {overall_max[1]} \n")
			print(f"Max point found: {max_x}, {max_y} \n")
			print(f"Bounds: {self.scan.lower_bound}, {self.scan.upper_bound} \n")
			self.scan.decay(decay_rate)
			self.scan.get_bounds(overall_max[0])
		return overall_max, max_change, max_change_x

	# creates histograms of the max x values by the end of each scan
	def multiscan(self, decay_rate: float) -> list[float]:
		final_max = [] # list of all the final maximums at the end of each full scan
		final_max_y = []
		max_history = [] # list of each scan's maximum over the decay_iters iterations
		max_history_x = []
		for i in range(self.multi_iters):
			self.reset()
			new_maximum, max_change, max_change_x = self.scanData(decay_rate)
			max_history.append(max_change)
			max_history_x.append(max_change_x)
			final_max.append(new_maximum[0])
			final_max_y.append(new_maximum[1])
		graph = plt.figure()
		plt.title(str(decay_rate))
		plt.hist(np.array(final_max), bins=[0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7, 3.9, 4.1, 4.3, 4.5, 4.7, 4.9, 5.1, 5.3, 5.5, 5.7, 5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5, 8.7, 8.9, 9.1, 9.3])
		plt.savefig(f"graphs/histogram/histogram_{decay_rate}.jpg")
		if show:
			plt.show()
		else:
			plt.close(graph)

		graph = plt.figure()
		plt.title(str(decay_rate) + " y")
		plt.hist(np.array(final_max_y))
		plt.savefig(f"graphs/histogram/histogram_{decay_rate}_y.jpg")
		if show:
			plt.show()
		else:
			plt.close(graph)

		average_values, average_x, std_dev_values = self.lineGraphCalculator(max_history, max_history_x)
		
		if self.std_dev_graph:
			x_axis = [i for i in range(self.decay_iters)]
			graph = plt.figure()
			plt.title(str(decay_rate) + " Maximum History")
			plt.errorbar(x_axis, np.array(average_values), np.array(std_dev_values), marker="^")
			plt.savefig(f"graphs/standard_deviation/average_history_{decay_rate}.jpg")
			if show:
				plt.show()
			else:
				plt.close(graph)
		return average_values, average_x, std_dev_values

	# resets scanner to prepare for new scan
	def reset(self) -> None:
		self.scan.reset()

def reset_dir(path_name: str = ''):
	folder = f'graphs{path_name}'
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))
	if path_name == '':
		os.makedirs('graphs/average')
		os.makedirs('graphs/standard_deviation')
		os.makedirs('graphs/iters')
		os.makedirs('graphs/histogram')
	print(f'graphs{path_name} was deleted')

# runs multiple multiscans at the rates defined in decay_rate_list
def main(sim_iters=5, decay_iters=5, multi_iters=1000, show=False, std_dev_graph=False, remove=6):
	if remove == 1:
		reset_dir('/average')
	elif remove == 2:
		reset_dir('/standard_deviation')
	elif remove == 3:
		reset_dir('/iters')
	elif remove == 4:
		reset_dir('/histogram')
	elif remove == 5:
		reset_dir('')
	else:
		print("No files removes")
	interface = Interface(sim_iters, decay_iters, multi_iters, show, std_dev_graph)
	average_values = {}
	average_x = {}
	std_dev_values = {}
	decay_rate_list = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
	x_axis = [i for i in range(decay_iters)]

	for i in decay_rate_list:
		interface.reset() # reset the scanner
		average_values[str(i)], average_x[str(i)], std_dev_values[str(i)] = interface.multiscan(i)
	graph = plt.figure()
	for key, value in average_values.items():
		plt.plot(x_axis, np.array(value), label=key)
	plt.title("Averages Maximum History")
	plt.legend()
	plt.savefig("graphs/average/average_history.jpg")

	if show:
		plt.show()
	else:
		plt.close(graph)

	graph = plt.figure()
	for key, value in average_x.items():
		plt.plot(x_axis, np.array(value), label=key)
	plt.title("Averages Maximum x History")
	plt.legend()
	plt.savefig("graphs/average/average_x_history.jpg")

	if show:
		plt.show()
	else:
		plt.close(graph)

# main function modified to run a history with different iters
def main_sim_iters(sim_iters=5, decay_iters=5, multi_iters=1000, show=False, std_dev_graph=False, iters_range=25, decay_rate=0.001, remove=6):
	if remove == 1:
		reset_dir('/average')
	elif remove == 2:
		reset_dir('/standard_deviation')
	elif remove == 3:
		reset_dir('/iters')
	elif remove == 4:
		reset_dir('/histogram')
	elif remove == 5:
		reset_dir('')
	else:
		print("No files removes")
	interface = Interface(sim_iters, decay_iters, multi_iters, show, std_dev_graph)
	average_values = {}
	average_x = {}
	std_dev_values = {}
	iters_list = [i for i in range(iters_range) if i % 5 == 0 and i != 0]
	iters_history = []
	decay_rate_list = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
	x_axis = [i for i in range(decay_iters)]

	for i in iters_list:
		interface.reset() # reset the scanner
		interface.sim_iters = i
		average_values[str(i)], average_x[str(i)], std_dev_values[str(i)] = interface.multiscan(decay_rate)
	graph = plt.figure()
	for key, value in average_values.items():
		plt.plot(x_axis, np.array(value), label=key)
	plt.title("Average Iters Maximum History")
	plt.legend()
	plt.savefig("graphs/iters/average_sim_iters_history.jpg")

	if show:
		plt.show()
	else:
		plt.close(graph)

	graph = plt.figure()
	for key, value in average_x.items():
		plt.plot(x_axis, np.array(value), label=key)
	plt.title("Average Iters Maximum x History")
	plt.legend()
	plt.savefig("graphs/iters/average_sim_iters_x_history.jpg")

	if show:
		plt.show()
	else:
		plt.close(graph)

	iters_history.append(object)

def main_multi_iters(sim_iters=5, decay_iters=5, multi_iters=1000, show=False, std_dev_graph=False, iters_range=25, decay_rate=0.001, remove=6):
	if remove == 1:
		reset_dir('/average')
	elif remove == 2:
		reset_dir('/standard_deviation')
	elif remove == 3:
		reset_dir('/iters')
	elif remove == 4:
		reset_dir('/histogram')
	elif remove == 5:
		reset_dir('')
	else:
		print("No files removes")
	interface = Interface(sim_iters, decay_iters, multi_iters, show, std_dev_graph)
	average_values = {}
	average_x = {}
	std_dev_values = {}
	iters_list = [i for i in range(iters_range) if (i % 2500 == 0 and i != 0) or i == 1000]
	iters_history = []
	decay_rate_list = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
	x_axis = [i for i in range(decay_iters)]

	for i in iters_list:
		interface.reset() # reset the scanner
		interface.multi_iters = i
		average_values[str(i)], average_x[str(i)], std_dev_values[str(i)] = interface.multiscan(decay_rate)
	graph = plt.figure()
	for key, value in average_values.items():
		plt.plot(x_axis, np.array(value), label=key)
	plt.title("Average Multi Iters Maximum History")
	plt.legend()
	plt.savefig("graphs/iters/average_multi_iters_history.jpg")

	if show:
		plt.show()
	else:
		plt.close(graph)

	graph = plt.figure()
	for key, value in average_x.items():
		plt.plot(x_axis, np.array(value), label=key)
	plt.title("Average Multi Iters Maximum x History")
	plt.legend()
	plt.savefig("graphs/iters/average_multi_iters_x_history.jpg")

	if show:
		plt.show()
	else:
		plt.close(graph)

	iters_history.append(object)



'''
The following code is to check if the user
wants to alter iterations through a user
interface in the console, otherwise it
will run with the default values
'''



if any("--help" in x for x in sys.argv) or any("-h" in x for x in sys.argv):
	print("Valid command line arguments:\n--user or -ui\t\t: alter iteration values through console ui")
	print("--show or -S\t\t: display graphs to the user (default only saves graphs)")
	print("--remove or -r\t\t: delete all graphs within a directory (for organization)")
	print("--std_dev or -sd\t: show standard_deviation for history graphs")
	print("--user or -ui\t\t: allows user to input arguments for the scans")
	print("--sim_iters or -si\t: runs multiple scans with different sim_iters arguments")
	print("--multi_iters or -mi\t: runs multiple scans with different multi_iters arguments")
else:
	if any("--std_dev" in x for x in sys.argv) or any("-sd" in x for x in sys.argv):
		std_dev_graph = True
	else:
		std_dev_graph = False
	if any("--show" in x for x in sys.argv) or any("-S" in x for x in sys.argv):
		show = True
	else:
		show = False
	if any("--remove" in x for x in sys.argv) or any("-r" in x for x in sys.argv):
		while (True):
			remove = input("Where do you want to remove all files?\n1 : graphs/average\n2 : graphs/standard_deviation\n3 : graphs/iters\n4 : graphs/histogram\n5 : graphs/\n6 : None\n")
			try:
				remove = int(remove)
				break
			except (ValueError, TypeError) as e:
				print("Value entered is not a number, please enter a number")
	else:
		remove = 0
	if any("--user" in x for x in sys.argv) or any("-ui" in x for x in sys.argv):
		while (True):
			sim_iters = input("Enter a value for the amount of times to run a scan before decaying: ")
			decay_iters = input("Enter a value for the amount of times to decay: ")
			multi_iters = input("Enter a value for the amount of times you want to run a multiscan at each decay rate: ")
			try:
				sim_iters = int(sim_iters)
				decay_iters = int(decay_iters)
				multi_iters = int(multi_iters)
				break
			except (ValueError, TypeError) as e:
				print("One of the entered values was not a number, please enter a number")
		main(sim_iters, decay_iters, multi_iters, show, remove=remove)
	elif any("--sim_iters" in x for x in sys.argv) or any("-si" in x for x in sys.argv):
		while (True):
			iters_range = input("Enter up to how many iterations you want to run (every 5 will be ran):")
			try:
				iters_range = int(iters_range)
				break
			except (ValueError, TypeError) as e:
				print("Value entered is not a number, please enter a number")
		main_sim_iters(show=show, std_dev_graph=std_dev_graph, iters_range=iters_range, remove=remove)
	elif any("--multi_iters" in x for x in sys.argv) or any("-mi" in x for x in sys.argv):
		while (True):
			iters_range = input("Enter up to how many iterations you want to run (every 2500 will be ran):")
			try:
				iters_range = int(iters_range)
				break
			except (ValueError, TypeError) as e:
				print("Value entered is not a number, please enter a number")
		main_multi_iters(show=show, std_dev_graph=std_dev_graph, iters_range=iters_range, remove=remove)
	else:
		main(show=show, std_dev_graph=std_dev_graph, remove=remove)