# import matplotlib.pyplot as plt
import cv2
from aprilTagDetectorv2 import AprilTagDetector

class DrawCorners:
	def __init__(self, corners, image):
		# image array
		self.image = image
		# corners should be a 2d list of 4 items, containing x and y coordinates
		self.corners = corners

	def drawCorners(self):
		# there are 4 corners
		for i in range(4):
			corner1 = self.corners[i]
			# draw to the first corner
			if i >= 3:
				corner2 = self.corners[0]
			else:
				corner2 = self.corners[i+1]
			# Draw a diagonal blue line with thickness of 5 px
			cv2.line(self.image, tuple(corner1), tuple(corner2), (0,255,0),20)
		# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
		# cv2.resizeWindow('image', 300,300)
		# cv2.imshow("image", self.image)
		# cv2.waitKey(0)
		return self.image


# TEST FUNCTIONS
# image_dir = "90_degrees.png"
# image = cv2.imread(image_dir)
# # print(image)
# atd = AprilTagDetector(image)
# corners = atd.getCorners()

# corners = DrawCorners(corners, image)
# print(corners.drawCorners())
