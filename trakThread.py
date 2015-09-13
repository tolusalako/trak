import threading, time
#TODO: multiple threads management

class Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._stop = False

   	def run(self, function, args, delay):
		while(not self._stop):
			result = function(args)
			if result != None:
				return result
			time.sleep(delay)

	def stop(self):
		self._stop = True
