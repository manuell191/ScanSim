import random
import numpy as np
import matplotlib.pyplot as plt

# x is values 1 - 100
# y = x^10 - 49.5x^9 + 1063.03x^8 - 12981.935x^7 + 99239.3917x^6 - 492186.36785x^5 + 1585470.496893x^4 - 3218089.1724245x^3 + 3821229.8104174x^2 - 2249281.4285439x + 406046.27998575

x = 0
y = x**10 - 49.5*(x**9) + 1063.03*(x**8) - 12981.935*(x**7) + 99239.3917*(x**6) - 492186.36785*(x**5) + 1585470.496893*(x**4) - 3218089.1724245*(x**3) + 3821229.8104174*(x**2) - 2249281.4285439*x + 406046.27998575

range_val = 4.51

def calc_y(x):
  y = x**10 - 49.5*(x**9) + 1063.03*(x**8) - 12981.935*(x**7) + 99239.3917*(x**6) - 492186.36785*(x**5) + 1585470.496893*(x**4) - 3218089.1724245*(x**3) + 3821229.8104174*(x**2) - 2249281.4285439*x + 406046.27998575
  return y

# returns x, y coordinates
def find_y(top, bottom):
  x = random.random() * (top - bottom) + bottom
  return x, calc_y(x)

# array: [(x,y), (x,y), (x,y)]
def get_array(z, top, bottom):
  array = []
  max_val = 2.93
  for i in range(z):
    array.append(find_y(top, bottom))
    if array[-1][1] > calc_y(max_val):
      max_val = array[-1][0]
  return array, max_val, calc_y(max_val)

def decay(range_val, decay_val):
  range_val = range_val - (range_val*decay_val)
  return range_val

def get_range(x, range_val):
  max_range = x + range_val
  min_range = x - range_val
  move_val = 0
  
  if max_range > 9.31:
    move_val = max_range - 9.31
    max_range = 9.31
    min_range -= move_val
  if min_range < 0.3:
    move_val = -(min_range - 0.3) 
    min_range = 0.3
    max_range += move_val
  
  return min_range, max_range
  
def read_data(range_val, decay_val, loops):
  bottom, top = get_range(4.8, range_val)
  overall_max = [0, -999999]
  max_change = []
  for i in range(loops):
    array, max_x, max_y = get_array(5, top, bottom)
    if max_y > overall_max[1]:
      overall_max = [max_x, max_y]
    max_change.append(overall_max[1])
    print("Overall max point: " + str(overall_max[0]) + ", " + str(overall_max[1]))
    print("")
    print("Max point found: " + str(max_x) + ", " + str(max_y))
    print("")
    print("Bounds: " + str(bottom) + " " + str(top))
    print("")
    #print("Array data: " + str(array))
    print("")
    print("")
    range_val = decay(range_val, decay_val)
    bottom, top = get_range(max_x, range_val)
  return overall_max, max_change

def loop_data(range_val, decay_val, loops):
  results = []
  lines = []
  for i in range(1000):
    new_results, max_change = read_data(range_val, decay_val, loops)
    lines.append(max_change)
    results.append(new_results[0])
  graph = plt.figure()
  plt.title(str(decay_val))
  plt.hist(np.array(results), bins=[0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7, 3.9, 4.1, 4.3, 4.5, 4.7, 4.9, 5.1, 5.3, 5.5, 5.7, 5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5, 8.7, 8.9, 9.1, 9.3])
  plt.savefig("histogram_{}.jpg".format(str(decay_val)))
  plt.close(graph)
  #plt.show()
  average_array = []
  for i in range(len(lines[0])):
    average = 0
    for j in range(len(lines)):
      average += lines[j][i]
    average /= len(lines)
    average_array.append(average)
  #plt.plot(np.array(average_array))
  #plt.title(str(decay_val))
  #plt.savefig("average_{}.jpg".format(str(decay_val)))
  #plt.show()
  return results, average_array

def sim(range_val, loops):
  results = {}
  averages = {}
  results["0.01"], averages["0.01"] = loop_data(range_val, 0.01, loops)
  results["0.05"], averages["0.05"] = loop_data(range_val, 0.05, loops)
  results["0.1"], averages["0.1"] = loop_data(range_val, 0.1, loops)
  results["0.2"], averages["0.2"] = loop_data(range_val, 0.2, loops)
  results["0.3"], averages["0.3"] = loop_data(range_val, 0.3, loops)
  results["0.4"], averages["0.4"] = loop_data(range_val, 0.4, loops)
  results["0.5"], averages["0.5"] = loop_data(range_val, 0.5, loops)
  print(averages)
  for key, value in averages.items():
    plt.plot(np.array(value), label=key)
  plt.title(str("Averages"))
  plt.legend()
  plt.savefig("averages.jpg")
  plt.show()
  print("\n")
  print("\n")
  print(results)


#read_data(range_val, 0.02, 5)

sim(range_val, 5)

#arry = np.array([0, 2, 5, 3, 1, 7, 2, 2, 5, 2])

#plt.hist(arry)
#plt.show()