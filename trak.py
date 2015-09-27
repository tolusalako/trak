from PIL import ImageTk, Image
from os import listdir
import traksource, trakdata
import time, sys
from datetime import datetime, timedelta

class Trak():
    def __init__(self, obj):
        self.objects_path = obj
        self.options = trakdata.TrakOptions()
        source = self.options.get('SOURCE')[0]
        preview = self.options.get('PREVIEW')[0]
        to = self.options.get('TO')
        from_ = self.options.get('FROM')
        every = self.options.get('EVERY')
        days = ['MON', 'TUE', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
        self.repeat_var = [int(self.options.get(days[d])[0]) for d in range(len(days))]

        #SET options
        if source == 'CAM':
            self.source = traksource.TrakCam(self.objects_path)
            self.input_var = 0
        else:
            self.source = traksource.TrakWindow(self.objects_path)
            self.input_var = 1	


        self.to_hr_var = to[0]
        self.to_min_var = to[1]
        self.to_am_pm = to[2]

        self.from_hr_var = from_[0]
        self.from_min_var = from_[1]
        self.from_am_pm = from_[2]

        self.interval_var = every[0]
        self.interval_am_pm = every[1]

        to = [self.to_hr_var, self.to_min_var, self.to_am_pm]
        from_ = [self.from_hr_var, self.from_min_var, self.from_am_pm]
        every = [self.interval_var, self.interval_am_pm]

        now = datetime.now()
        start = datetime.strptime(str(from_), "['%I', '%M', '%p']").replace(year = now.year, day = now.day, month = now.month)
        end = datetime.strptime(str(to), "['%I', '%M', '%p']").replace(year = now.year, day = now.day, month = now.month)


        if end < start:
            end = end.replace(day = now.day + 1)

        self.data = trakdata.TrakData(['Kai Test'])
        delta = None
        interval = every[0]
        if every[1] == 'HR':
            delta = timedelta(hours = int(interval))
        else:
            delta = timedelta(minutes = int(interval))

        d = end
        self.cols = {}
        i = 1
        while True:
            t = d.strftime("%I:%M %p")
            self.cols[(d.hour, d.minute)] = i
            self.data.write(0, i, t) #Column Names
            d += delta
            i += 1

            if d == start.replace(day = d.day, minute = d.minute):
                break
            elif start < d.replace(day = end.day) < end:
                continue
        self.data.save()
        x, y = 1,1

        wait_in_seconds = 0
        first_run = True
        while True:
            self.wait(wait_in_seconds)
            now = datetime.now()
            end = end.replace(year = now.year, month = now.month, day = now.day)

            if end < start:
                end = end.replace(day = now.day + 1)

            if start < now < end: #Blackout hours. No activity
                print 'Blackout Hours starting now...'
                wait_in_seconds = int((end - now).seconds)
                y += 1
            else:
                day = datetime.today().weekday()
                if self.repeat_var[day]:#Current day is checked.
                    x = self.cols.get((now.hour, now.minute), None)
                    if x != None:
                        print 'Writing data...'
                        if x == 1 or first_run: #New Day
                            self.data.write(y, 0, time.strftime("%m-%d-%Y")) #Write the current date on all lines
                            first_run = False
                        self.write_data(x, y)
                        wait_in_seconds = int(((now + delta) - now).seconds)
                    else:
                        for h,m in self.cols.keys():
                            if h == now.hour:
                                if m > now.minute:
                                    print m, now.minute
                                    wait_in_seconds = (m - now.minute) * 60
                                else:
                                    wait_in_seconds = (60 - now.minute) * 60
                                break
                else: 
                    day = day + 1 if day < 6 else 0
                    if self.repeat_var[day].get():  
                        wait_in_seconds = int((start.replace(day = now.day + 1, minute = now.minute) - now).seconds)
                    else:
                        wait_in_seconds = 24 * 60 * 60
            
            print 'Next in %s seconds.' % (wait_in_seconds) if wait_in_seconds > 60 else ''
	    sys.stdout.flush()

    def write_data(self, x, y):
        self.data.write(y, x, 'Test')
    	self.data.save()
#        if self.list_var.get() != "":
#            self.temp_img = self.source.capture(self.list_var.get())
#            if self.temp_img != None:
#                found_objects = traksource.find_objects_as_objects(self.temp_img, [self.objects_path + o for o in self.objects]) 
#                for obj in found_objects:
#                    self.data.write(y, x, obj.location, obj = obj.name)

    def wait(self, t):
        if t > 60:
            time.sleep(abs(t - 5))

