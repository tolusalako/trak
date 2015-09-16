import threading, time
#TODO: multiple threads management

class Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

   	def run(self, function, args, delay):
		while(True):
			result = function(args)
			if result != None:
				return result
			time.sleep(delay)

	def run_bool(cond)
