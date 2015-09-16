import win32gui, win32ui, win32con, win32api, win32console
import cv2
import time, sys
from PIL import Image
from os import listdir
from scipy import where, asarray
from objects import object

class TrakWindow():

	def __init__(self, obj_path):
		self.objects_path = obj_path
		self.source_list = ([], [])  #list of all matching windows
		win32gui.EnumWindows(self.__callback, self.source_list)  #populate list
		self.source_count = len(self.source_list)

	def capture(self, source):
		hwnd = self.source_list[0][int(source.split('-')[0])]
 		windowSize = win32gui.GetWindowRect(hwnd)
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
		win32gui.ReleaseDC(hwnd, hwindc) 
		return img

	def release(self):
		pass

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
		if win32gui.IsWindowVisible(hwnd):
			window_title = win32gui.GetWindowText(hwnd)
			if window_title != '':
				lists[0].append(hwnd)
				lists[1].append(str(len(lists[1])) + '-' + window_title)
		return True


class TrakCam():

	def __init__(self, obj_path):
		self.source_list = ([], [])
		try:
			for i in range(3):
				cam = cv2.VideoCapture(i)
				cam.release()
				self.source_list[0].append(i)
				self.source_list[1].append('Camera ' + str(i))
			self.setupCam()
		except:
			pass
		self.source_count = len(self.source_list)
		self._released = True

	def setupCam(self):
		if self.source_count > 0:
			self.camera = cv2.VideoCapture(0)
			self._released = False
		else:
			self.camera = None
			self._released = True

	def capture(self, source = 0, ramp_frames = 0):
		if self._released:
			self.setupCam()
		for i in xrange(ramp_frames):
			retval, im = self.camera.read()
		retval, im = self.camera.read()
 		return None if im == None else Image.fromarray(im)

 	def release(self):
 		if not self._released:
 			self.camera.release()
 			self._released = True



		# while(True):
		#     # Capture frame-by-frame
		#     ret, frame = cap.read()

		#     # Our operations on the frame come here
		#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		#     # Display the resulting frame
		#     cv2.imshow('frame',gray)
		#     if cv2.waitKey(1) & 0xFF == ord('q'):
		#         break

		# # When everything done, release the capture
		# cap.release()
		# cv2.destroyAllWindows()

