#Toluwanimi Salako  (www.salakotech.com) 
import traksource, trakdata
import time, sys
from datetime import datetime, timedelta
from os import listdir

class TrakTimer():
    def __init__(self, obj_path, source_input):
        self.objects_path = obj_path
        self.input = source_input
        self.objects = [f for f in listdir(self.objects_path)]
        self.time_threshold = 10
        self.options = trakdata.TrakOptions()
        source = self.options.get('SOURCE')[0]
        preview = self.options.get('PREVIEW')[0]
        to = self.options.get('TO')
        from_ = self.options.get('FROM')
        every = self.options.get('EVERY')
        days = ['MON', 'TUE', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
        threshold = self.options.get('THRESHOLD')

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

        self.print_settings()
        if end < start:
            end += timedelta(days = 1)

        self.data = trakdata.TrakData(['Kai Test'])
        delta = None
        interval = every[0]
        if every[1] == 'HR':
            delta = timedelta(hours = int(interval))
        else:
            delta = timedelta(minutes = int(interval))

        #Populate excel with column titles
        d = end
        e = start + timedelta(days = 1)
        self.cols = {}
        i = 1
        while d <= e:
            t = d.strftime("%I:%M %p")
            self.cols[t] = i
            self.data.write(0, i, t) #Column Names
            d += delta
            i += 1
        self.data.save()
        x, y = 1,1

        #Action loop
        wait_in_seconds = 0
        new_day = True
        last_day = datetime.today().weekday()
        while True:
            self.wait(wait_in_seconds)
            now = datetime.now()
            end = end.replace(year = now.year, month = now.month, day = now.day)

            if end < start:
                end += timedelta(days = 1)

            day = datetime.today().weekday()
            if self.repeat_var[day]:#Current day is checked.
                if last_day < day:
                    y += 1
                    new_day = True
                columns_as_time = [datetime.strptime(t, "%I:%M %p").
                     replace(year = now.year, month = now.month, day = now.day, second = now.second, microsecond = now.microsecond) for t in self.cols.keys()]
                valid_times = filter(lambda x: x >= now, columns_as_time) 
                if len(valid_times) == 0:
                    wait_in_seconds = int((end - now).seconds) #Sleep till blackout ends
                else:
                    future_time = min(valid_times)
                    if (now.hour == future_time.hour and now.minute == future_time.minute):
                        x = self.cols.get(now.strftime("%I:%M %p"), None)
                        if new_day: #New Day
                            self.data.write(y, 0, time.strftime("%m-%d-%Y")) #Write the current date on all lines
                            new_day = False
                        self.write_data(x, y)
                        wait_in_seconds = int(delta.seconds)
                    else:
                        wait_in_seconds = int((future_time - now).seconds)
            else: 
                midnight = now.replace(day = now.day + 1, hour = 0, minute = 0)
                wait_in_seconds = int((midnight - now).seconds) #Sleep till next day
                
            last_day = day
            if wait_in_seconds > self.time_threshold:
                print 'Next in %s seconds.' % (wait_in_seconds)
            sys.stdout.flush()

    def write_data(self, x, y):
        print 'Writing data...'
        print datetime.now().strftime("%I:%M %p"), x, y

        if self.input != "":
           self.temp_img = self.source.capture(self.input)
           if self.temp_img != None:
               found_objects = traksource.find_objects_as_objects(self.temp_img, [self.objects_path + o for o in self.objects], all_ = False) 
               for obj in found_objects:
                   self.data.write(y, x, obj.location)
                   break
        self.data.save()

    def print_settings(self):
        print 'Trak started. \nLogging every %s %s.' % (self.interval_var, self.interval_am_pm)
        print 'Blackout Hours: %s:%s %s to %s:%s %s.' % (self.from_hr_var, self.from_min_var, self.from_am_pm, self.to_hr_var, self.to_min_var, self.to_am_pm)

    def wait(self, t):
        if t > self.time_threshold:
            time.sleep(abs(t - 1))

