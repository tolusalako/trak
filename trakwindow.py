#Toluwanimi Salako  (www.salakotech.com) 
import Tkinter as TK
from PIL import ImageTk, Image
from os import listdir, path, makedirs
import traksource, trakdata, trak
from datetime import datetime

class MainWindow(TK.Frame):
    STICKY_ALL = TK.N + TK.S + TK.W + TK.E

    def __init__(self, objects_path):
        self.master = TK.Tk()
        TK.Frame.__init__(self, self.master)

        self.master.protocol('WM_DELETE_WINDOW', self.__on_exit)
        self.master.wm_title("Trak")

        self.objects_path = objects_path
        self.preview_width = 300
        self.preview_height = 200

        #SOURCE
        self.labelframe_source = TK.LabelFrame(master = self, text = 'Source')
        self.labelframe_source.grid(row = 0, column = 0, rowspan = 3, sticky = TK.W)

        self.input_var=TK.IntVar()
        self.radiobutton_cam = TK.Radiobutton(master = self.labelframe_source, text = "Cam", variable = self.input_var, value = 0, command = self.switch_input)
        self.radiobutton_cam.grid(row = 0, column = 0,sticky = TK.W)
        self.radiobutton_window = TK.Radiobutton(master = self.labelframe_source, text = "Window", variable = self.input_var, value = 1, command = self.switch_input)
        self.radiobutton_window.grid(row = 0, column = 1,sticky = TK.W)

        self.list_var = TK.StringVar(self)

        self.preview_var = TK.IntVar()
        self.checkbutton_preview = TK.Checkbutton(master = self.labelframe_source, variable = self.preview_var, command = self.preview_input)
        self.checkbutton_preview.grid(row = 1, column = 1)
        self.preview_var.set(0)

        self.labelframe_preview = TK.LabelFrame(master = self.labelframe_source, text = 'Preview')
        self.labelframe_preview.grid(row = 2, columnspan = 3)

        self.canvas_preview = TK.Canvas(master = self.labelframe_preview, background = "#FFFFFF", height = self.preview_height, width = self.preview_width)
        self.canvas_preview.grid(row = 0, columnspan = 3, sticky = TK.W)
        self.canvas_preview.bind("<ButtonRelease-1>", lambda event: self.popout_preview(event))
        self.canvas_preview.bind("<ButtonRelease-3>", lambda event: self.save_preview(event))

        self.frame_righthalf = TK.Frame(master = self)
        self.frame_righthalf.grid(row = 0, column = 1, sticky = TK.E)

        #TIMER
        self.labelframe_timer = TK.LabelFrame(master = self.frame_righthalf, text = 'Timer')
        self.labelframe_timer.grid(row = 1, column = 0, columnspan = 3, sticky = TK.E)

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

        self.frame_interval = TK.Frame(master = self.labelframe_timer)
        self.frame_interval.grid(row = 1, column = 0, columnspan = 3)
        self.label_interval = TK.Label(master = self.frame_interval, text = 'INTERVAL: Every ')
        self.label_interval.grid(row = 1, column = 0, columnspan = 2, sticky = TK.W)
        self.interval_var = TK.StringVar(self)
        self.spinbox_interval = TK.Spinbox(master = self.frame_interval, from_ = 1, to = 999, width = 3, textvariable = self.interval_var)
        self.spinbox_interval.grid(row = 1, column = 2)
        self.button_interval = TK.Button(master = self.frame_interval, text = 'MIN')
        self.button_interval.grid(row = 1, column = 3)
        self.button_interval.bind('<ButtonRelease-1>', lambda event: self.min_to_hr_swap(event))

        self.labelframe_blackout =  TK.LabelFrame(master = self.labelframe_timer, text = 'Blackout')
        self.labelframe_blackout.grid(row = 2, columnspan = 3, sticky = TK.W)

        self.label_from = TK.Label(master = self.labelframe_blackout, text = 'FROM:')
        self.label_from.grid(row = 1, column = 0, columnspan = 1, sticky = TK.W)
        self.from_hr_var = TK.StringVar(self)
        self.spinbox_from_hr = TK.Spinbox(master = self.labelframe_blackout, from_ = 1, to = 12, width = 2, textvariable = self.from_hr_var)
        self.spinbox_from_hr.grid(row = 1, column = 2)
        self.from_min_var = TK.StringVar(self)
        self.spinbox_from_min = TK.Spinbox(master = self.labelframe_blackout, from_ = 00, to = 59, width = 2, textvariable = self.from_min_var)
        self.spinbox_from_min.grid(row = 1, column = 3)
        self.button_from = TK.Button(master = self.labelframe_blackout, text = 'AM')
        self.button_from.grid(row = 1, column = 4)
        self.button_from.bind('<ButtonRelease-1>', lambda event: self.am_pm_swap(event))

        self.label_to = TK.Label(master = self.labelframe_blackout, text = 'TO:')
        self.label_to.grid(row = 2, column = 0, columnspan = 1, sticky = TK.W)
        self.to_hr_var = TK.StringVar(self)
        self.spinbox_to_hr = TK.Spinbox(master = self.labelframe_blackout, from_ = 1, to = 12, width = 2, textvariable = self.to_hr_var)
        self.spinbox_to_hr.grid(row = 2, column = 2)
        self.to_min_var = TK.StringVar(self)
        self.spinbox_to_min = TK.Spinbox(master = self.labelframe_blackout, from_ = 0, to = 59, width = 2, textvariable = self.to_min_var)
        self.spinbox_to_min.grid(row = 2, column = 3)
        self.button_to = TK.Button(master = self.labelframe_blackout, text = 'PM')
        self.button_to.grid(row = 2, column = 4)
        self.button_to.bind('<ButtonRelease-1>', lambda event: self.am_pm_swap(event))

        #OBJECTS
        self.labelframe_objects = TK.LabelFrame(master = self.frame_righthalf, text = 'Objects')
        self.labelframe_objects.grid(row = 0, column = 1, sticky = TK.W)

        self.listbox_objects = TK.Listbox(master = self.labelframe_objects, selectmode = TK.SINGLE)
        self.listbox_objects.grid(row = 0)
        self.listbox_objects.bind('<Enter>', self.update_object_list)
        self.listbox_objects.bind('<ButtonRelease-1>', self.preview_object)

        self.canvas_preview_object = TK.Canvas(master = self.labelframe_objects, background = "#FFFFFF", height = 100, width = 100)
        self.canvas_preview_object.grid(row = 0, column = 1, sticky = TK.E)

        #THRESHOLD
        self.labelframe_threshold = TK.LabelFrame(master = self.labelframe_source, text = 'Threshold')
        self.labelframe_threshold.grid(row = 1, column = 2)

        self.scale_threshold = TK.Scale(master = self.labelframe_threshold, from_ = 0, to = 1, orient = TK.HORIZONTAL, resolution = 0.1)
        self.scale_threshold.grid(row = 0)


        #START
        self.labelframe_start = TK.LabelFrame(master = self.labelframe_timer, text = 'START')
        self.labelframe_start.grid(row = 2, column =5, sticky = TK.E)

        self.label_time_status = TK.Label(master = self.labelframe_start, text = '')
        self.label_time_status.grid(row = 0)
        self.button_start = TK.Button(master = self.labelframe_start, text = 'START', command = self.start)
        self.button_start.grid(row = 1)

        self.setup()
        self.pack()


    def setup(self):
        #LOAD Data
        self.options = trakdata.TrakOptions()
        source = self.options.get('SOURCE')[0]
        preview = self.options.get('PREVIEW')[0]
        to = self.options.get('TO')
        from_ = self.options.get('FROM')
        every = self.options.get('EVERY')
        threshold = self.options.get('THRESHOLD')[0]
        days = ['MON', 'TUE', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
        [self.repeat_var[d].set(int(self.options.get(days[d])[0])) for d in range(len(days))]

        #SET options
        if source == 'CAM':
            self.source = traksource.TrakCam(self.objects_path)
            self.input_var.set(0)
        else:
            self.source = traksource.TrakWindow(self.objects_path)
            self.input_var.set(1)	
        self.optionmenu_sources = apply(TK.OptionMenu, (self.labelframe_source, self.list_var) + tuple(self.source.source_list[1]))
        self.optionmenu_sources.grid(row = 1, column = 0, columnspan = 2, sticky = TK.W)

        if preview == '1':
            self.preview_var.set(1)
            self.preview_input()

        self.scale_threshold.set(float(threshold))

        self.to_hr_var.set(to[0])
        self.to_min_var.set(to[1])
        self.button_to['text'] = to[2]

        self.from_hr_var.set(from_[0])
        self.from_min_var.set(from_[1])
        self.button_from['text'] = from_[2]

        self.interval_var.set(every[0])
        self.button_interval['text'] = every[1] 

        self.update_object_list(None)

    def show(self):
        self.master.mainloop()

    def am_pm_swap(self, event):
        event.widget['text'] = 'PM' if event.widget['text'] == 'AM' else 'AM'

    def min_to_hr_swap(self, event):
        event.widget['text'] = 'MIN' if event.widget['text'] == 'HR' else 'HR'	

    def preview_input(self):
        if not self.preview_var.get():
            self.canvas_preview.delete("all")
            return
        elif self.list_var.get() == "":
            self.preview_var.set(0)
            self.canvas_preview.delete("all")
            return
        else:
            if len(self.source.source_list) > 0:
               
                self.temp_img = self.source.capture(self.list_var.get()) #Capture Image from source
                if self.temp_img == None: #Make sure Image IS captured
                    self.preview_var.set(0)
                    return

                #If an object is selected, let's modify the image to show that.
                i = self.get_selected_object()
                if i != -1:
                    f = self.objects_path + self.listbox_objects.get(i)
                    self.temp_img = traksource.find_objects_as_image(self.temp_img, [f], self.scale_threshold.get())
                else:
                    self.temp_img = traksource.find_objects_as_image(self.temp_img, [self.objects_path + o for o in self.objects], self.scale_threshold.get(), all_ = False)    
                self.photo_preview = self.temp_img.copy()
                self.photo_preview_resized = ImageTk.PhotoImage(self.temp_img.resize((self.preview_width, self.preview_height)))
                self.canvas_preview.create_image((0, 0), image = self.photo_preview_resized, anchor = TK.N +TK.W)
                self.after(8, self.preview_input)
            else:
                self.preview_var.set(0)
                self.source.release()

            #self.canvas_preview.delete("all")

    def get_selected_object(self):
        if len(self.listbox_objects.curselection()) == 0:
            return -1
        else:
            return self.listbox_objects.curselection()[0]

    def preview_object(self, event):
        i = self.get_selected_object()
        if (i != -1):
            f = self.objects_path + self.listbox_objects.get(i)
            temp_obj = Image.open(f)
            self.obj_preview = ImageTk.PhotoImage(temp_obj.resize((100, 100)))
            self.canvas_preview_object.create_image((0,0), image = self.obj_preview, anchor = TK.N +TK.W)

    def save_preview(self, event):
        if self.preview_var.get():
            self.photo_preview.save('saves/' + datetime.now().strftime("%Y-%m-%d_%I-%M-%S") + '.jpg')

    def popout_preview(self, event):
        if self.preview_var.get():
            self.photo_preview.show()

    def switch_input(self):
        self.preview_var.set(0)
        if not self.input_var.get():
            self.source = traksource.TrakCam(self.objects_path)
        else:
            self.source = traksource.TrakWindow(self.objects_path)

        self.optionmenu_sources = apply(TK.OptionMenu, (self.labelframe_source, self.list_var) + tuple(self.source.source_list[1]))
        self.optionmenu_sources.grid(row = 1, column = 0, columnspan = 2, sticky = TK.W)

    def update_object_list(self, event):
        size = self.listbox_objects.size()
        self.listbox_objects.delete(0, size)
        self.objects = [f for f in listdir(self.objects_path)]
        apply(self.listbox_objects.insert, (0,) + tuple(self.objects))


    def save_options(self):
        self.options.set('SOURCE', ['CAM'] if not self.input_var.get() else ['WINDOW'])
        self.options.set('PREVIEW', [self.preview_var.get()])
        self.options.set('TO', [self.to_hr_var.get(), self.to_min_var.get(), self.button_to['text']])
        self.options.set('FROM', [self.from_hr_var.get(), self.from_min_var.get(), self.button_from['text']])
        self.options.set('EVERY', [self.interval_var.get(), self.button_interval['text']])
        self.options.set('THRESHOLD', [str(self.scale_threshold.get())])
        days = ['MON', 'TUE', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
        [self.options.set(days[d], [self.repeat_var[d].get()]) for d in range(len(days))]
        self.options.save()

    def start(self):
        input_ = self.list_var.get()
        default_input = self.source.source_list[0] if self.source.source_count > 0 else None

        if input_ != "":
            self.__on_exit() 
            runner = trak.Trak(self.objects_path, input_)
        elif default is not None:
            self.__on_exit() 
            runner = trak.Trak(self.objects_path, default_input)
        else:
            return  


    def __on_exit(self):
        try:
            self.save_options()
        except Exception as c:
            print c
        self.source.release()
        self.canvas_preview.delete("all")
        self.master.destroy()


if __name__ == '__main__':
    if not path.isdir('objects/'):
        makedirs('objects/')
    if not path.isdir('saves/'):
        makedirs('saves/')
    main = MainWindow('objects/')
    main.show()

	
