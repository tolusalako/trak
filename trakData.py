from xlrd import open_workbook, Book
from xlutils.copy import copy
from xlwt import Workbook
from collections import defaultdict
from datetime import datetime, timedelta
import time

def list_to_time(l):
	return datetime.strptime(str(l), "['%I', '%M', '%p']")

class TrakData:
	def __init__(self, objects, from_, to, interval, load = r'data\data.xls'):
		self.output = load
		self.book = Workbook()
		self.sheets = []
		for o in objects:
			self.sheets.append(self.book.add_sheet(o, cell_overwrite_ok=True))
		delta = None
		if interval[1] == 'HR':
			delta = timedelta(hours = int(interval[0]))
		else:
			delta = timedelta(minutes = int(interval[0]))

		d = list_to_time(from_)
		self.cols = dict()
		i = 1
		while d <= list_to_time(to):
			for s in self.sheets:
				t = d.strftime("%I:%M %p")
				s.write(0, i, t)
				self.cols['t'] = i
			d += delta
			i += 1
		self.row_count = 1
		self.last_day = time.strftime('%d')

	def write(self, name, data):
		t = time.strftime("%I:%M %p")
		d = time.strftime("%d-%m-%Y")

		current_day = time.strftime('%d')
		if self.last_day != current_day:
			self.row_count += 1
			self.last_day = current_day
		row = self.row_count 

		for sheet in self.sheets:
			if sheet.name == name:
				sheet.write(row, 0, d)
				sheet.write(row, self.cols[t], str(data))

	def save(self):
		self.book.save(self.output)

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
		#print self.data

	def get(self, key):
		return self.data.get(key, None)

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