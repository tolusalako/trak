from PIL import Image, ImageFilter
import sys, time, random
from scipy import array, any, all

#pixel = scipy.array

output_colors = {0:(102, 225, 51), 1:(51, 153, 255),
				2:(255, 153, 255), 3:(255, 153, 102),
				4:(153, 153, 255), 5:(204, 255, 204),
				6:(178, 178, 0), 7:(255, 153, 153),
				8:(128, 178, 178), 9:(51, 153, 255),
				10:(163, 163, 255)}


def evaluate(pixel1, pixel2, diff):
	z = abs(pixel1 - pixel2)
	return any(z >= diff)

class PixMage():
	null = -1 #leave as negative #

	def get_coordinates(self, i = null): #If null, function returns all coordinates instead of the coordinates at index i
		if i == self.null:
			return [x for x in self.pixel_coordinates]
		else:
			return self.pixel_coordinates[i] if i < len(self.pixel_coordinates) else []

	def get_smallest_coordinates(self):
		f = lambda x,y: x if len(x) < len(y) else y
		return reduce(f, self.pixel_coordinates)

	def get_largest_coordinates(self):
		f = lambda x,y: x if len(x) > len(y) else y
		return reduce(f, self.pixel_coordinates)

	def find_index(self, pixel):
		for p in self.color_indices.keys():
			if not evaluate(pixel, array(p), self.diff):
				return self.color_indices.get(p, self.null)
		return -1

	def save_coordinates(self, i = null):
		if i == self.null:
			pass
		else:
			pass

	def add_coordinate(self, coord, pixel):
		i = self.find_index(pixel)
		if i != self.null:
			self.pixel_coordinates[i].append(coord)
		else:
			i = len(self.pixel_coordinates)
			self.color_indices[tuple(pixel)] = i;
			self.pixel_coordinates.append([coord])

	def __init__(self, offset):
		self.color_indices = dict() #Key = pixel, value = index
		self.pixel_coordinates = list() #i = index, value = list(coordinate pixels in tuples)
		self.diff = array([offset, offset, offset])
	def __len__(self):
		return len(self.pixel_coordinates)
	def __repr__(self):
		result = ''
		total = 0
		for i in range(len(self.pixel_coordinates)):
			t = len(self.pixel_coordinates[i])
			result += '\n\n' + str(i) + ':	\n' + str(t)
			total += t
		result += '\n Total = %d. For more info use get_coordinates()' % (total,)
		return result

#TESTZONE

def to_image(coords, size):
	img = Image.new('RGB', size, 'white')
	for c in coords:
		img.putpixel(c, (0, 0, 0))
	img.save('result.jpg')

def coord_eval(c1, c2, cutoff):
	c = abs(c1 - c2)
	return any(c >= cutoff)

def object_from_coordinates(coords, size):
	# print coords
	last = ''
	obj_count = 0
	color = (0,0,0)
	img = Image.new('RGB', size, 'white')
	# for c in coords:
	# 	a = array(c)
	# 	strike = 0
	# 	if last != '':
	# 		if not coord_eval(last, a, 3):
	# 			img.putpixel(tuple(a), color)
	# 		else:
	# 			if strike > 5:
	# 				img.save('objects/' + str(obj_count) + '.jpg')
	# 				obj_count += 1
	# 				img = Image.new('RGB', size, 'white')
	# 				img.putpixel(tuple(a), color)
	# 	else:
	# 		img.putpixel(tuple(a), color)
	# 	last = a

	x,y = coords[0] #First item
	while True: #Try to traverse depth and breadth at the same time
		if x+1,y in coords:

		if x+2,y in coords


#Objective: Sort a list of coords - find disconnect / distant ones and separate them
#Connection can be linked through x or y.
#Find pattern for whole objects.
#Disregard outlines/inaccuracy
#Join closely related coords
#TESTZONE

def find_starting_points(img):
	global output_colors

	height = img.size[1]
	width = img.size[0]
	data = array(list(img.getdata()))
	data = data.ravel().reshape(height, width, 3) #RGB
	diff = 200 #Increase # for more simpler images
	pm = PixMage(diff)

	# result_image = img.copy()
	
	for y in range(len(data)):
		for x in range(len(data[y])):
			pixel = data[y][x] 
			pm.add_coordinate((x, y), pixel)
			c = pm.find_index(pixel)
			# if c != -1:
			# 	result_image.putpixel((x, y), output_colors.get(c, (0,0,0)))
	print len(pm)
	# result_image.save('output.jpg')
	print pm.get_smallest_coordinates()
	#object_from_coordinates(pm.get_smallest_coordinates(), (width, height))
	#to_image(pm.get_smallest_coordinates(), (width, height))