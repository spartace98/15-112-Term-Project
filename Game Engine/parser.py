# THE DETECTOR RETRUNS A STRING OF VALUES (SOME OF INTERESTS AND OTHERS NOT)
# THE PARSER SCRIPT IS RESPONSIBLE FOR CONVERITNG THIS STRING INTO USABLE FORMAT (EG LIST), WHICH I WROTE MYSELF
# THIS FILE ALSO CONTAINS THE IMAGE FILTERING METHOD WHICH IS USED TO REMOVE CONTOURS IN THE IMAGE

# script that converts the string output to a 2d list
"""
# To do list
# figure out a way to distinct 2d list from 1d list
"""
import cv2

class StringToList(object):
	def __init__(self, string):
		self.dict = {}
		prevKey = None

		# splitting the lines by colon, to form a dictionary
		for line in string.splitlines():
			line = line.strip()
			try:
				title = line.split(":")[0].strip()
				values = line.split(":")[1].strip()
				self.dict[title] = values
				prevKey = title
			# if no colon in line, belongs to the previous dict key
			except:
				self.dict[prevKey] += "," + line

		# converting the homography in the dictionary to actual python list
		self.dict['Homography'] = self.convertToList(self.dict['Homography'][1:-1])

		# convert center and corners to list
		self.dict['Corners'] = self.convertToList(self.dict['Corners'][1:-1])
		self.dict['Center'] = self.convertToList(self.dict['Center'])[0]

	# split by comma and spaces
	def convertToList(self, string):
		# remove the trailing brackets
		# lists = self.dict['Homography'][2:-1]
		newList = []
		for array in string.split(","):
			tempList = []
			array = array[1:-1]
			for val in array.split():
				tempList.append(float(val))
			newList.append(tempList)

		# self.dict['Homography'] = newList
		return newList

	def printDict(self):
		for key, val in self.dict.items():
			print(key, val)

	def getHomography(self):
		return self.dict["Homography"]

	def getCorners(self):
		cornerList = self.dict["Corners"]
		# converting the floats to integer pixel positions
		for r in range(len(cornerList)):
			for c in range(len(cornerList[0])):
				cornerList[r][c] = int(cornerList[r][c])
		return self.dict["Corners"]

class ImageBinaryConverter(object):
	def __init__(self, thresh = 100):
		self.thresh = thresh
	
	def getFilteredImage(self, img):
		# img = cv2.imread(image_dir, cv2.IMREAD_GRAYSCALE)
		# gaussian blur the image
		img = cv2.GaussianBlur(img, (15, 15), 0)
		im_bw = cv2.threshold(img, self.thresh, 255, cv2.THRESH_BINARY)[1]
		return im_bw

# TEST FUNCTIONS

# s = """\
# Family: b'tag36h11'
# ID: 0
# Hamming error: 0
# Goodness: 0.0
# Decision margin: 124.66666412353516
# Homography: [[-7.07095468e-01  1.42105371e-16 -1.24448802e+00]
#           [-3.97843171e-16 -7.07095468e-01 -1.13700951e+00]
#           [-1.13423992e-18  1.38904329e-34 -5.65676374e-03]]
# Center: [220. 201.]
# Corners: [[ 95.  76.]
#           [345.  76.]
#           [345. 326.]
#           [ 95. 326.]]
# """

# parser = StringToList(s)
# # print(parser.dict['Homography'])
# print(parser.dict)
# # print(int('10'))


# test functions
# converter = ImageBinaryConverter()
# print(converter.getFilteredImage("images/0U.jpg"))



