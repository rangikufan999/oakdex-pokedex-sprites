# 'Captures' Pokemon
# - Requests JSON of Pokemon data in order to get the Pokemon's name by the Pokemon's id number
# - Requests PNG images of each Pokemon and copies them to a 'captured' folder,
#   renaming them from Pokemon id number to Pokemon name

import os
import requests
import time

def wait(seconds):
	global timer

	elapsed_time = time.time() - timer
	while elapsed_time < seconds:
		elapsed_time = time.time() - timer
	timer = time.time()

def track():
	# Keep track (count) the number of Pokemon 'captured'
	global counter

	counter += 1

def report():
	# Report (print) the number of Pokemon 'captured'
	global counter

	print(str(counter) + " pokemon captured!")

def establishPath(name):
	# Create folder if it doesn't exist and return the path
	try:
		os.mkdir(name)
	except FileExistsError:
		pass
	return name + "/"

def requestPokeAPIJSON(query_id):
	# Request Pokemon JSON data from PokeAPI
	url = "https://pokeapi.co/api/v2/pokemon/" + str(query_id)
	response = requests.get(url, headers={'Content-Type': 'application/json'})
	return response

def requestPokeAPIpng(filename):
	# Request Pokemon PNG image from PokeAPI
	url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + filename
	response = requests.get(url, headers={'Content-Type': 'image/png'})
	return response

# 'Capture' a single Pokemon
def capturePokemon(path, query_id):
	# Request Pokemon JSON data by the id number of the Pokemon
	json_response = requestPokeAPIJSON(query_id)

	if json_response.status_code == 200:
		# Get the name of the Pokemon
		name = json_response.json()['name']

		# Request Pokemon PNG by the id number of the Pokemon
		filename = str(query_id) + ".png"
		png_response = requestPokeAPIpng(filename)

		if png_response.status_code == 200:
			# Copy the PNG content from the response into a file saved by the name of the Pokemon
			with open(path + name + ".png", 'wb') as file:
				file.write(png_response.content)
			return True
		else:
			# Print the id number and name of the Pokemon and the error code of failed requests
			print("id=" + str(query_id) + ", name=" + name + ", status_code=" + str(png_response.status_code))
	else:
		# Print the id number of the Pokemon and the error code of failed requests
		print("id=" + str(query_id) + ", status_code=" + str(json_response.status_code))

	return False

# 'Capture' a batch quantity of Pokemon
def batchQueryPokemon(path, start, end, n=5):
	global counter

	for query_id in range(start, end+1):
		captured = capturePokemon(path, query_id)
		wait(0.6) # slow down time to 0.6 seconds per request (conforms to 100 request per minute limit of PokeAPI)
		if captured:
			track() # track every Pokemon 'captured'
			if counter % n == 0 and counter != 0: # report number of Pokemon 'captured' to console after every nth capture
				report()

if __name__ == '__main__':
	# initialize global variables
	timer = time.time()
	counter = 0
	
	# set path
	path = establishPath('captured')
	
	# 'capture' pokemon
	batchQueryPokemon(path, 1, 807)
	batchQueryPokemon(path, 10001, 10090)

	# While the following conform to the 'query by id number' convention for JSON requests,
	# they do NOT conform to the 'query by id number' convention for PNG requests...
	##batchQueryPokemon(path, 10091, 10157)

	# report final number of Pokemon 'captured'
	report()