import Tkinter as TK
from PIL import ImageTk, Image

class MainWindow(TK.Frame):
	STICKY_ALL = TK.N + TK.S + TK.W + TK.E


	def mouseOverZone(self, event,  zone, img_file):
		#Snapping to edges
		#Rotation
		if zone == 1 and event.y < 5:
			event.y = 0

		elif zone == 2:
			event.y = self.scene.coords(self.zone2)[3]
		elif zone == 3:
			event.x = 0
		elif zone == 4:
			event.x = self.scene.coords(self.zone4)[2]

		if self.temp == None:
			self.temp = ImageTk.PhotoImage(img_file), 
		if self.cursor == None:
			self.cursor = self.scene.create_image(event.x, event.y, image = self.temp)
		else:
			self.scene.delete( self.cursor)
			self.cursor = self.scene.create_image(event.x, event.y, image = self.temp)

		self.scene.tag_bind(self.cursor, '<ButtonRelease-3>', lambda event: self.rotateImage(event, img_file))

	def rotateImage(self, event, img_file):
		self.angle -=45 
		if self.angle == -360:
			self.angle = 0

		self.temp = ImageTk.PhotoImage(img_file.rotate(self.angle))
		self.cursor = self.scene.create_image(event.x, event.y, image = self.temp)
		self.scene.tag_bind(self.cursor, '<ButtonRelease-3>', lambda event: self.rotateImage(event, img_file))
		
		

	def highlightSpawnZone(self, img_file):
		self.zone1 = self.scene.create_rectangle(0, 0, self.sceneW, self.sceneH*.1, fill = 'lightgreen')
		self.zone2 = self.scene.create_rectangle(0, self.sceneH*.9, self.sceneW, self.sceneH, fill = 'lightgreen')
		self.zone3 = self.scene.create_rectangle(0, self.sceneH*.1, self.sceneW*.1, self.sceneH*.9, fill = 'lightgreen')
		self.zone4 = self.scene.create_rectangle(self.sceneW*.9, self.sceneH*.1, self.sceneW, self.sceneH*.9, fill = 'lightgreen')


		self.scene.tag_bind(self.zone1, '<Motion>', lambda event, zone = 1: self.mouseOverZone(event, zone, img_file))
		self.scene.tag_bind(self.zone2, '<Motion>', lambda event, zone = 2: self.mouseOverZone(event, zone, img_file))
		self.scene.tag_bind(self.zone3, '<Motion>', lambda event, zone = 3: self.mouseOverZone(event, zone, img_file))
		self.scene.tag_bind(self.zone4, '<Motion>', lambda event, zone = 4: self.mouseOverZone(event, zone, img_file))

	def removeHighlights(self):
		print 'remove'
		self.scene.delete( self.cursor)
		self.cursor = None
		del self.temp
		self.temp = None
		self.scene.delete(self.zone1)
		self.scene.delete(self.zone2)
		self.scene.delete(self.zone3)
		self.scene.delete(self.zone4)


	def spawn(self, obj):
		file = None
		if obj == 'football':
			file = self.file_football
		elif obj == 'trampoline':
			file = self.file_trampoline
		elif obj == 'airvent':
			file = self.file_airvent
		elif obj == 'oil':
			file = self.file_oil

		self.highlightSpawnZone(file)


	def repack(self): 
		self.update()
		self.after(800, self.repack)

	def show(self):
		self.repack()
		self.mainloop()

	def __init__(self, master = None):
		TK.Frame.__init__(self, master)
		self.grid(row = 1, pady = 5, padx = 5, sticky = self.STICKY_ALL)
		self.btnsize = 70

		self.sceneW = 700
		self.sceneH = 500

		self.cursor = None
		self.temp = None
		self.angle = 0

		#RESOURCES
		self.file_football = Image.open("./images/football.png").resize((self.btnsize, self.btnsize))
		self.img_football = ImageTk.PhotoImage(self.file_football)

		self.file_trampoline = Image.open("./images/trampoline.png").resize((self.btnsize, self.btnsize))
		self.img_trampoline = ImageTk.PhotoImage(self.file_trampoline)

		self.file_airvent = Image.open("./images/airvent.png").resize((self.btnsize, self.btnsize))
		self.img_airvent = ImageTk.PhotoImage(self.file_airvent)

		self.file_oil = Image.open("./images/oil.png").resize((self.btnsize, self.btnsize))
		self.img_oil = ImageTk.PhotoImage(self.file_oil)


		#CONTROLS
		self.labelframe_control = TK.LabelFrame(master = self, text = 'Control')
		self.labelframe_control.grid(row = 0, column = 0, sticky = TK.W + TK.N + TK.S)
		self.frame_control = TK.Frame(self.labelframe_control)	# self.scene.itemconfigure(self.zone1, cursor = 'none')
		# self.scene.itemconfigure(self.zone2, cursor = 'none')
		# self.scene.itemconfigure(self.zone3, cursor = 'none')
		# self.scene.itemconfigure(self.zone4, cursor = 'none')
		self.frame_control.grid(row = 0)

		self.btn_ball = TK.Button(master = self.frame_control, command = 'football')
		self.btn_ball.grid(row = 0, sticky = self.STICKY_ALL)
		self.btn_ball.configure(image = self.img_football, height = self.btnsize, width = self.btnsize)
		self.btn_trampoline = TK.Button(master = self.frame_control, command = lambda: self.spawn('trampoline'))
		self.btn_trampoline.grid(row = 1, sticky = self.STICKY_ALL)
		self.btn_trampoline.configure(image = self.img_trampoline, height = self.btnsize, width = self.btnsize)
		self.btn_airvent = TK.Button(master = self.frame_control, command = lambda: self.spawn('airvent'))
		self.btn_airvent.grid(row = 2, sticky = self.STICKY_ALL)
		self.btn_airvent.configure(image = self.img_airvent, height = self.btnsize, width = self.btnsize)
		self.btn_oil = TK.Button(master = self.frame_control, command = lambda: self.spawn('oil'))
		self.btn_oil.grid(row = 3, sticky = self.STICKY_ALL)
		self.btn_oil.configure(image = self.img_oil, height = self.btnsize, width = self.btnsize)

		#SCENE
		self.labelframe_scene = TK.LabelFrame(master = self, text = 'Scene')
		self.labelframe_scene.grid(row = 0, column = 1, sticky = TK.E + TK.N + TK.S)

		self.scene = TK.Canvas(master = self.labelframe_scene, width = self.sceneW, height = self.sceneH, background = 'white')
		self.scene.grid(sticky = self.STICKY_ALL)
		#self.scene.configure(cursor = 'none')

		self.pack()

if __name__ == '__main__':
	main = MainWindow()
	main.show()