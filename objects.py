
class object:

	def __init__(self, name, top_left, size):
		self.top_left = top_left
		self.size = size
		self.name = name

	def __repr__(self):
		print name + 'TL: {}, W: {}, H: {}'.format(self.top_left, self.size[0], self.size[1]) 