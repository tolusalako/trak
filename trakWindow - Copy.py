import win32gui, win32ui, win32con, win32api, win32console
import time
from PIL import Image

class WindowHandler():
	def screenshot(self):
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


	def __callback(self, hwnd, lists):
		strings = lists[0]
	   	names = lists[1]
		if win32gui.IsWindowVisible(hwnd):
			window_title = win32gui.GetWindowText(hwnd)
			if any(n.lower() in window_title.lower().strip('-').strip(':').split() for n in names) and ('python' not in window_title):
				strings.append(hwnd)
		return True

	def __init__(self, names):
		self.window = None
		win_list = []  #list of all matching windows
		win32gui.EnumWindows(self.__callback, (win_list, names))  #populate list

		win_count = len(win_list)
		if win_count == 1:
			print 'Selecting ' + win32gui.GetWindowText(win_list[0]) + '.'
			self.window = win_list[0]
		else:
			print ('Error: Multiple windows found.' if win_count > 1 else 'Error: Window not found.')
	