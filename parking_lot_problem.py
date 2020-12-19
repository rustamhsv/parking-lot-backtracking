""" Algorithms fills the parking lot with cars. At the end prints the best arrangement of cars possible in the lot.
	Best solution means as minimum empty spaces in the parking lot as possible. 
	Empty spaces are shown with 0s, while filled areas have values [car numbers - 1,2,3,...] in the parking lot.
"""
import copy

# Take user input
pl_width, pl_length = map(int, input().split()) # width -> from top to bottom, length -> from left to right
n = int(input()) # number of cars
cars = [] 
for i in range(n):
	a, b = map(int, input().split()) # take width & length of cars
	cars.append([a, b, i+1])  # add dimensions and cars to the list

parking_space = [[0]*pl_length for _ in range(pl_width)] # define dimensions of parking lot
visited_spots = [] # store visited spots for each car [mainly after backtracking]
all_arrangements = [] # store all arrangements of cars in parking lot to show the BEST solution at the end


def print_solution(parking_space):
	""" Prints the best solution algorithm could achieve"""

	# Search for the best arrangement"""
	num_of_zeros = [] # list to store empty spaces for each arrangement
	for all in range(len(all_arrangements)):
		num_of_iterations_zeros = 0
		for i in range(pl_width):
			for j in range(pl_length):
				if(all_arrangements[all][i][j] == 0):
					num_of_iterations_zeros += 1  # number of empty spaces 
		num_of_zeros.append(num_of_iterations_zeros)

	index_of_min_zeros = num_of_zeros.index(min(num_of_zeros)) # index of the best solution

	# Print solution
	for i in range(pl_width):
		for j in range(pl_length):
			if j == pl_length - 1:
				print(all_arrangements[index_of_min_zeros][i][j], end = "\n\n") # remove extra tabs at the end
			else:
				print(all_arrangements[index_of_min_zeros][i][j], end = "\t") # tabs between values in the line

def sort_cars(cars):
	""" Sort cars from largest to smallest based on areas [len x wid]"""
	cars.sort(key = lambda x: x[0]*x[1], reverse = True)

def is_possible(car_width, car_length, m, n):
	""" Check if the car fits to the space in the lot, return True if fits"""
	if m + car_width > pl_width or n + car_length > pl_length: # m and n -> starting points
		return False

	for i in range(m, m + car_width):
		for j in range(n, n + car_length):
			if parking_space[i][j] != 0:
				return False
	return True

def is_rotated_possible(car_width, car_length, m, n):
	""" Check if the 90 degree rotated car fits to the space in the lot, return True if fits"""
	if m + car_length > pl_width or n + car_width > pl_length: # m and n -> starting points
		return False

	for i in range(m, m + car_length):
		for j in range(n, n + car_width):
			if parking_space[i][j] != 0:				
				return False
	return True


def place_car(new_x, new_y, i):
	""" Place car in the parking lot"""
	for x in range(new_x, new_x + cars[i][0]): # i -> car number
		for y in range(new_y, new_y + cars[i][1]):
			parking_space[x][y] = cars[i][2]

def place_car_rotated(new_x, new_y, i):
	""" Place rotated car in the parking lot"""
	for x in range(new_x, new_x + cars[i][1]): # i -> car number
		for y in range(new_y, new_y + cars[i][0]):
			parking_space[x][y] = cars[i][2]

def remove_car(i):
	""" Remove car from the parking lot for better arrangement, used for backtracking"""
	flag = True
	for x in range(pl_width):
		for y in range(pl_length):
			if parking_space[x][y] == cars[i][2]:
				parking_space[x][y] = 0 
				if flag == True:
					visited_spots.append([i, x, y]) 
					flag = False

def is_visited(x, y, i):
	""" Returns True if the spot is already visited by the same car"""
	for t in range(len(visited_spots)):
		if visited_spots[t][0] == i and visited_spots[t][1] == x and visited_spots[t][2] == y: # check car number & coordinates
				return True
	return False	          	

def solve_parking_problem(cars, parking_space, num_cars):
	""" Main function. Places the cars in the parking lot """
	i = 0 # place of the car in the sorted array
	num_of_iterations = 0 # number of iterations
	while i < num_cars: 
		placed = False # check if car is placed or it was not possible 
		for x in range(pl_width): # x coordinate in matrix
			for y in range(pl_length): # y coordinate in matrix
				if (parking_space[x][y] == 0 and is_possible(cars[i][0], cars[i][1], x, y) and # place car if possible
				not is_visited(x, y, i)):
					place_car(x, y, i)
					placed = True
					break
				elif (parking_space[x][y] == 0 and is_rotated_possible(cars[i][0], cars[i][1], x, y) and # place car if rotated possible
				not is_visited(x, y, i)):
					place_car_rotated(x, y, i)
					placed = True
					break
			else:
				continue
			break

		# Backtracking
		if not placed and i >= 0:
			remove_car(i-1) # if it was not possible to place the current car then remove previous car
			i = i - 1 # place previous car again
		else:
			i += 1 # if it was  possible to place the current car then continue to place the next car

		all_arrangements.append(copy.deepcopy(parking_space)) # store all arrangement matrices
		num_of_iterations += 1
		if(num_of_iterations == 1000): # max number of iterations -> 1000 [not to exceed the time limit]
			break

sort_cars(cars)
solve_parking_problem(cars, parking_space, n)
print_solution(parking_space)