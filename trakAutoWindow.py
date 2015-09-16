import win32gui, win32ui, win32con, win32api, win32console
import cv2
import time, sys
from PIL import Image
from os import listdir
from scipy import where, asarray
from objects import object

class Trak():
	def take_screenshot(self):
 		windowSize = win32gui.GetWindowRect(self.window)
 		hwin = win32gui.GetDesktopWindow()
 		width = windowSize[2] - windowSize[0]
		height = windowSize[3] - windowSize[1]
		hwindc = win32gui.GetWindowDC(hwin)
		srcdc = win32ui.CreateDCFromHandle(hwindc)
		memdc = srcdc.CreateCompatibleDC()
		bmp = win32ui.CreateBitmap()
		bmp.CreateCompatibleBitmap(srcdc, width, height)
		memdc.SelectObject(bmp)
		memdc.BitBlt((0, 0), (width, height), srcdc, (windowSize[0], windowSize[1]), win32con.SRCCOPY)
		bmpinfo = bmp.GetInfo()
		bmpstr = bmp.GetBitmapBits(True)
		img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
		win32gui.DeleteObject(bmp.GetHandle())
		memdc.DeleteDC()
		srcdc.DeleteDC()
		win32gui.ReleaseDC(self.window, hwindc) 
		return img

	def find_objects(self, img): #Multiple objects fix
		img_rgb = asarray(img)
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
		objects = [f for f in listdir(self.objects_path)]

		found_objects = set()
		
		for obj in objects:
			img_copy = img_rgb.copy()
			template = cv2.imread(self.objects_path + obj, 0)
			w, h = template.shape[::-1]

			res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

			threshold = .6
			loc = where( res >= threshold)

			#DEBUG
			for pt in zip(*loc[::-1]): #pt is the topleft corner
			 	cv2.rectangle(img_copy, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
			if len(loc) != 0:
				cv2.imwrite('output/' + obj,img_copy)
			
			found_objects.add(object(obj, loc[0], (w,h))) #Can use the first loc value or the avg of them. It is usually accurate
		return found_objects



	def __callback(self, hwnd, lists):
		strings = lists[0]
	   	names = lists[1]
		if win32gui.IsWindowVisible(hwnd):
			window_title = win32gui.GetWindowText(hwnd)
			if any(n.lower() in window_title.lower().strip('-').strip(':').split() for n in names) and ('python' not in window_title):
				strings.append(hwnd)
		return True

	def __init__(self, names, obj_path):
		self.objects_path = obj_path
		self.window = None
		win_list = []  #list of all matching windows
		win32gui.EnumWindows(self.__callback, (win_list, names))  #populate list

		win_count = len(win_list)
		if win_count == 1:
			print 'Selecting ' + win32gui.GetWindowText(win_list[0]) + '.'
			self.window = win_list[0]
		else:
			print ('Error: Multiple windows found.' if win_count > 1 else 'Error: Window not found.')


if __name__ == '__main__':
	source = ''
	window_names = []
	obj = 'objects/'
	try:
		source = sys.argv[1]
		window_names = sys.argv[2:]
	except:
		print 'Usage: trakWindow.py source options'
		sys.exit(0)
	
	trak = Trak(window_names, obj)
	trak.find_objects(trak.take_screenshot())
