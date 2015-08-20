
class object:
	length = 0
	width = 0
	parent = None
	location = tuple()
	img_file = ''
	image = None

	def __init__(self, img_file):
		pass



class mobileObjects(object):
	speed = 0
	angle = 0

	def slow(x = 1):
		self.speed -= x

	def accelerate(x = 1):
		self.speed += x

	def stop():
		self.speed = 0

	def setSpeed(x):
		self.speed = x

	def setAngle(x):
		self.angle = x

	def __init__(self, img_file):
		object.__init__(self, img_file)
		pass
