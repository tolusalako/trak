from xlrd import open_workbook, Book
from tempfile import TemporaryFile
from xlwt import Workbook
from collections import defaultdict


# class TrakData:
# 	def __init__(self, output, objects, load = ''):
# 		self.output = output + '\\'+ 'trakdata.csv'
# 		self.book = Workbook()
# 		for n in objects:
# 			self.book.add_sheet(n)

# 	def add_data(self, object, data):
# 		pass

# 	def save(self):
# 		self.book.save(self.output)



# if __name__ == '__main__':
# 	td = TrakData('output', ['Mario', 'Loot'])
# 	td.save()


class TrakData():
	def __init__(self, file):
		self.data = defaultdict(list)
		self.filename = file
		try:
			self.file = open(file, 'r')
			self.__read()
		except:
			self.file = open(file, 'w')
		finally:
			self.file.close()


	def __read(self):
		key = 'NULL'
		for line in self.file.readlines():
			line = line.strip('\n')
			if line[0] == ".":
				key = line[1:]
				continue
			elif line[0] == "#":
				continue
			self.data[key].append(line)
		#print self.data

	def get(self, key):
		return self.data.get(key, None)

	def set(self, key, value):
		self.data[key] = value

	def save(self):
		self.file = open(self.filename, 'w')
		for k in self.data.keys():
			self.file.write('.' + k + '\n')
			for l in self.data[k]:
				self.file.write(l + '\n')
		self.file.close()