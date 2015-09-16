from xlrd import open_workbook, Book
from tempfile import TemporaryFile
from xlwt import Workbook


class TrakData:
	def __init__(self, output, objects, load = ''):
		self.output = output + '\\'+ 'trakdata.csv'
		self.book = Workbook()
		for n in objects:
			self.book.add_sheet(n)

	def add_data(self, object, data):
		pass

	def save(self):
		self.book.save(self.output)



if __name__ == '__main__':
	td = TrakData('output', ['Mario', 'Loot'])
	td.save()