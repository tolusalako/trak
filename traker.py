#GUI
import Tkinter as TK
from PIL import ImageTk, Image

import trak, trakData


class MainWindow(TK.Frame):
	STICKY_ALL = TK.N + TK.S + TK.W + TK.E

	def __init__(self, master = None):
		TK.Frame.__init__(self, master)
		OPTIONS = ['None']
		self.preview_width = 300
		self.preview_height = 200

		#LOAD DEFAULT SOURCES (CAMS)
		self.source = trak.TrakCam('objects/')
		OPTIONS = ['Camera {}'.format(i) for i in range(self.source.source_count)]


		#SOURCE
		self.labelframe_source = TK.LabelFrame(master = self, text = 'Source')
		self.labelframe_source.grid(row = 0, column = 0, rowspan = 3, sticky = TK.W)

		self.input_var=TK.IntVar()
		self.radiobutton_cam = TK.Radiobutton(master = self.labelframe_source, text = "Cam", variable = self.input_var, value = 0, command = self.switch_input)
		self.radiobutton_cam.grid(row = 0, column = 0,sticky = TK.W)
		self.radiobutton_cam.select()
		self.radiobutton_window = TK.Radiobutton(master = self.labelframe_source, text = "Window", variable = self.input_var, value = 1, command = self.switch_input)
		self.radiobutton_window.grid(row = 0, column = 1,sticky = TK.W)

		self.list_var = TK.StringVar(self)
		self.list_var.set(OPTIONS[0])
		self.optionmenu_sources = apply(TK.OptionMenu, (self.labelframe_source, self.list_var) + tuple(OPTIONS))
		self.optionmenu_sources.grid(row = 1, column = 0, columnspan = 2, sticky = TK.W)

		self.preview_var = TK.IntVar()
		self.checkbutton_preview = TK.Checkbutton(master = self.labelframe_source, variable = self.preview_var, command = self.preview)
		self.checkbutton_preview.grid(row = 1, column = 1)
		self.preview_var.set(1)

		self.labelframe_preview = TK.LabelFrame(master = self.labelframe_source, text = 'Preview')
		self.labelframe_preview.grid(row = 2, columnspan = 3)

		self.canvas_preview = TK.Canvas(master = self.labelframe_preview, background = "#FFFFFF", height = self.preview_height, width = self.preview_width)
		self.canvas_preview.grid(row = 0, columnspan = 3, sticky = TK.W)

		#TIMER
		self.labelframe_timer = TK.LabelFrame(master = self, text = 'Timer')
		self.labelframe_timer.grid(row = 0, column = 1, sticky = TK.E)

		self.repeat_var = [TK.IntVar() for i in range(7)]
		self.checkbutton_repeat_Mon = TK.Checkbutton(master = self.labelframe_timer, text = 'Mon', variable = self.repeat_var[0])
		self.checkbutton_repeat_Mon.grid(row = 0, column = 0)
		self.checkbutton_repeat_Tue = TK.Checkbutton(master = self.labelframe_timer, text = 'Tue', variable = self.repeat_var[1])
		self.checkbutton_repeat_Tue.grid(row = 0, column = 1)
		self.checkbutton_repeat_Wed = TK.Checkbutton(master = self.labelframe_timer, text = 'Wed', variable = self.repeat_var[2])
		self.checkbutton_repeat_Wed.grid(row = 0, column = 2)
		self.checkbutton_repeat_Thurs = TK.Checkbutton(master = self.labelframe_timer, text = 'Thurs', variable = self.repeat_var[3])
		self.checkbutton_repeat_Thurs.grid(row = 0, column = 3)
		self.checkbutton_repeat_Fri = TK.Checkbutton(master = self.labelframe_timer, text = 'Fri', variable = self.repeat_var[4])
		self.checkbutton_repeat_Fri.grid(row = 0, column = 4)
		self.checkbutton_repeat_Sat = TK.Checkbutton(master = self.labelframe_timer, text = 'Sat', variable = self.repeat_var[5])
		self.checkbutton_repeat_Sat.grid(row = 0, column = 5)
		self.checkbutton_repeat_Sun = TK.Checkbutton(master = self.labelframe_timer, text = 'Sun', variable = self.repeat_var[6])
		self.checkbutton_repeat_Sun.grid(row = 0, column = 6)

		self.label_from = TK.Label(master = self.labelframe_timer, text = 'FROM:')
		self.label_from.grid(row = 1, column = 0, columnspan = 1, sticky = TK.W)
		self.spinbox_from_hr = TK.Spinbox(master = self.labelframe_timer, from_ = 1, to = 12, width = 2)
		self.spinbox_from_hr.grid(row = 1, column = 2)
		self.spinbox_from_min = TK.Spinbox(master = self.labelframe_timer, from_ = 00, to = 59, width = 2)
		self.spinbox_from_min.grid(row = 1, column = 3)
		self.button_from = TK.Button(master = self.labelframe_timer, text = 'AM')
		self.button_from.grid(row = 1, column = 4)
		self.button_from.bind('<ButtonRelease-1>', lambda event: self.am_pm_swap(event))

		self.label_to = TK.Label(master = self.labelframe_timer, text = 'TO:')
		self.label_to.grid(row = 2, column = 0, columnspan = 1, sticky = TK.W)
		self.spinbox_to_hr = TK.Spinbox(master = self.labelframe_timer, from_ = 1, to = 12, width = 2)
		self.spinbox_to_hr.grid(row = 2, column = 2)
		self.spinbox_to_min = TK.Spinbox(master = self.labelframe_timer, from_ = 0, to = 59, width = 2)
		self.spinbox_to_min.grid(row = 2, column = 3)
		self.button_to = TK.Button(master = self.labelframe_timer, text = 'PM')
		self.button_to.grid(row = 2, column = 4)
		self.button_to.bind('<ButtonRelease-1>', lambda event: self.am_pm_swap(event))

		self.label_interval = TK.Label(master = self.labelframe_timer, text = 'EVERY: ')
		self.label_interval.grid(row = 3, column = 0, sticky = TK.W)
		self.spinbox_interval = TK.Spinbox(master = self.labelframe_timer, from_ = 1, to = 999, width = 3)
		self.spinbox_interval.grid(row = 3, column = 2)
		self.button_interval = TK.Button(master = self.labelframe_timer, text = 'MIN')
		self.button_interval.grid(row = 3, column = 3)
		self.button_interval.bind('<ButtonRelease-1>', lambda event: self.min_to_hr_swap(event))

		#INPUT
		# self.labelframe_input = TK.LabelFrame(master = self, text = 'Input')
		# self.labelframe_input.grid(row = 1, column = 2)
		# self.button_browse_input = TK.Button(master = self.labelframe_input, text = 'Browse')
		# self.button_browse_input.grid()

		self.preview()
		self.pack()

	def show(self):
		self.mainloop()

	def am_pm_swap(self, event):
		event.widget['text'] = 'PM' if event.widget['text'] == 'AM' else 'AM'

	def min_to_hr_swap(self, event):
		event.widget['text'] = 'MIN' if event.widget['text'] == 'HR' else 'HR'	

	def preview(self):
		if self.preview_var.get():
			self.temp_img = self.source.capture(self.list_var.get())
			if self.temp_img == None:
				self.preview_var.set(0)
				return
			self.temp_photo = ImageTk.PhotoImage(self.temp_img.resize((self.preview_width, self.preview_height)))
			self.canvas_preview.create_image((0, 0), image = self.temp_photo, anchor = TK.N +TK.W)
			self.after(8, self.preview)
		else:
			self.source.release()
			self.canvas_preview.delete("all")

	def switch_input(self):
		self.preview_var.set(0)
		if not self.input_var.get():
			self.source = trak.TrakCam('objects/')
		else:
			self.source = trak.TrakWindow('objects/')



		self.optionmenu_sources = apply(TK.OptionMenu, (self.labelframe_source, self.list_var) + tuple(self.source.source_list[1]))
		self.optionmenu_sources.grid(row = 1, column = 0, columnspan = 2, sticky = TK.W)


if __name__ == '__main__':
	main = MainWindow()
	main.show()