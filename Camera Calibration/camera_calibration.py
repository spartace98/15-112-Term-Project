"""
code extracted from 
https://medium.com/analytics-vidhya/camera-calibration-with-opencv-f324679c6eb7
checkerboard image extracted from 
https://stackoverflow.com/questions/17665912/findchessboardcorners-fails-for-calibration-image

"""
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# directories of calibration images
current_dir = os.getcwd()
calibration_image_dir = os.path.join(current_dir, "calibration_images")
# print(calibration_image_dir)

# prepare object points
nx = 7 # number of inside corners in x
ny = 7 # number of inside corners in y

# Arrays to store object points and image points from all the images
objpoints = [] # 3D points in real world space
imgpoints = [] # 2D points in image plane

# Prepare obj points, like (0, 0, 0), (1, 0, 0), (2, 0, 0)....., (7, 5, 0)
objp = np.zeros((7*7,3), np.float32)
# print(np.mgrid[0:7,0:7].T.shape)
objp[:,:2] =  np.mgrid[0:7,0:7].T.reshape(-1,2) # x,y coordinates 
# print(type(objp))

print('reading images...')
# making a list of calibration images
for image_dir in os.listdir(calibration_image_dir):
	if image_dir.endswith('jpg'):
		try:
			path = os.path.join(calibration_image_dir, image_dir)
			img = cv2.imread(path)
			
			# Convert to grayscale
			gray = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
			# plt.imshow(img)
			# plt.show()

			# Find the chessboard corners
			ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

			# print(ret)
			# print(corners)
			if ret == True:
				# Draw and display the corners
				# cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
				# plt.imshow(img)
				# plt.show()
				imgpoints.append(corners)
				objpoints.append(objp)
				# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1:], None, None)

		except:
			print("error file detected:", image_dir)

		# print(image_dir)

# print(len(imgpoints))

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1:], None, None)
print("Copy and Paste the matrix below!")
print()
print(mtx)



