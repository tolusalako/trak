import pyscreenshot as ImageGrab


def screenshot():
	im = ImageGrab.grab()
	print type(im)
 


if __name__ == '__main__':
	screenshot()