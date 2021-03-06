#Toluwanimi Salako  (www.salakotech.com) 
import win32gui, win32ui, win32con
import cv2
from PIL import Image
from scipy import where, asarray
from trakobject import Object
from trakdata import TrakOptions

def find_objects_as_objects(img, objects, threshold = .6, all_ = True): #Multiple objects fix		
	img_rgb = asarray(img)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

	found_objects = set()

	for obj in objects:
		img_copy = img_rgb.copy()
		template = cv2.imread(obj, 0)
		if template is None:
			continue
		w, h = template.shape[::-1]

		res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
		loc = where( res >= threshold)
		for pt in zip(*loc[::-1]):
			name = obj.split('/')[-1]
			found_objects.add(Object(name, pt, (w,h))) #Can use the first loc value or the avg of them. It is usually accurate
			break
		if not all_ and len(found_objects) > 1:
			break
	return found_objects

def find_objects_as_image(img, objects, threshold = .6, all_ = True):
	data = TrakOptions(file = r'data\debug.txt')

	img_rgb = asarray(img)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
	img_copy = img_rgb.copy()
	count = 0
	for obj in objects:
		template = cv2.imread(obj, 0)
		if template is None:
			continue
		w, h = template.shape[::-1]

		res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
		loc = where( res >= threshold)
		for pt in zip(*loc[::-1]): #pt is the topleft corner
		 	cv2.rectangle(img_copy, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

		 	n = data.get(obj)[0]
		 	if n is None:
		 		data.set(obj, [1])
		 	else:
		 		data.set(obj, [int(n) + 1])
		 	data.save()


		 	count += 1
		 	break
	 	if not all_ and count > 0:
	 		break
	return Image.fromarray(img_copy)

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
			# self.camera.set(3,1280)
			# self.camera.set(4,1024)
			self.camera.set(3,720)
			self.camera.set(4,480)
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
 		return None if im is None else Image.fromarray(im)

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

