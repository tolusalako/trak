import cv2
from os import listdir
from scipy import where, asarray
from objects import object

def auto_thresholding(res, count, threshold): #BETA
	_max = 100000000 #where z = 0
	_min = 0
	step = 100000

	while(True):
		loc = where( res >= threshold)
		z = len(zip(*loc[::-1]))
		print threshold, z
		if z == 0:
			_max = threshold
			threshold -= step*2
			step /= 2
			continue
		elif z > count: 
			ts = threshold + step
			threshold = ts if ts < _max else _max
		elif z < count:
			ts = threshold - step
			threshold = ts if ts > _min else _min
		else:
			return loc

def find_objects(img):
	objects_path = 'objects/'

	img_rgb = asarray(img)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
	objects = [f for f in listdir(objects_path)]

	found_objects = set()
	
	for obj in objects:
		img_copy = img_rgb.copy()
		template = cv2.imread(objects_path + obj, 0)
		w, h = template.shape[::-1]

		res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

		threshold = .5
		loc = where( res >= threshold)
		# for pt in zip(*loc[::-1]): #pt is the topleft corner
		# 	cv2.rectangle(img_copy, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
		#cv2.imwrite(obj,img_copy)
		
		found_objects.add(object(obj, loc[0], (w,h))) #Can use the first loc value or the avg of them. It is usually accurate
	return found_objects

	