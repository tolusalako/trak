from xlrd import open_workbook, Book
from xlutils.copy import copy
from xlwt import Workbook
from collections import defaultdict


class TrakData:
	def __init__(self, objects, load = r'data\data.xls'):
		self.output = load
		self.book = Workbook()
		self.sheets = []
		for o in objects:
			self.sheets.append(self.book.add_sheet(o, cell_overwrite_ok=True))

	def write(self, x, y, data, obj = 'ALL'):
		for sheet in self.sheets:
			if ((sheet.name == obj) or (obj == 'ALL')):
				sheet.write(x, y, str(data))

	def save(self):
		try:
			self.book.save(self.output)
		except Exception, e:
			self.__save_backup()

	def __save_backup(self):
		self.book.save(self.output.replace('.', '[Backup].'))


class TrakOptions():
	def __init__(self, file = r'data\options.txt'):
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

	def get(self, key):
		return self.data.get(key, [None])

	def set(self, key, value):
		self.data[key] = value

	def save(self):
		self.file = open(self.filename, 'w')
		self.file.write('#PLEASE AVOID EDITING THIS FILE MANUALLY\n')
		for k in self.data.keys():
			self.file.write('.' + str(k) + '\n')
			for l in self.data[k]:
				self.file.write(str(l) + '\n')
		self.file.close()