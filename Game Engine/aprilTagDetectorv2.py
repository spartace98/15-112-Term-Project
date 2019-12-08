# I DO NOT OWN THE APRIL TAG
# https://www.researchgate.net/figure/Examples-of-different-AprilTag-families_fig1_328188091 (april tag picture)
# DETECTION FRAMEWORK FOLLOSW THE DOCUMENTATION FOR THE APRILTYAG LIBRRARY, WHICH CAN BE FOUND FROM THE FOLLOWING SITE
# https://pypi.org/project/apriltag/
# THE DETECTOR RETRUNS A STRING OF VALUES (SOME OF INTERESTS AND OTHERS NOT)
# THE PARSER SCRIPT IS RESPONSIBLE FOR CONVERITNG THIS STRING INTO USABLE FORMAT (EG LIST), WHICH I WROTE MYSELF

import apriltag
import cv2
from parser import StringToList, ImageBinaryConverter
import numpy as np
from scipy.spatial.transform import Rotation as R

class AprilTagDetector():
    def __init__(self, image):
        ######################################
        # SETTING UP VARIABLES
        ######################################
        # assuming that the image is already grayscale
        # self.image = image
        self.imageArray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.threshold = 70
        self.camera_cal_matrix = np.array([[1.11379904e+03, 0.00000000e+00, 5.67239537e+02],
                                            [0.00000000e+00, 1.16158572e+03, 1.04091897e+02],
                                            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        options = apriltag.DetectorOptions(families='tag36h11',
                                         border=4,
                                         nthreads=4,
                                         quad_decimate=1.0,
                                         quad_blur=0.0,
                                         refine_edges=True,
                                         refine_decode=True,
                                         refine_pose=True,
                                         debug=True,
                                         quad_contours=False)
        self.StringToList = self.getResults()

    # sets up the detector and return the results in a list
    def getResults(self):
        try:
            self.converter = ImageBinaryConverter(self.threshold)
            self.detector = apriltag.Detector()
            # converts the image into black and white
            self.filteredImage = self.converter.getFilteredImage(self.imageArray)
            results = self.detector.detect(self.filteredImage)
            self.results = results[0].tostring()
            self.StringToList = StringToList(self.results)
            return self.StringToList
        except:
            return None

    def getCorners(self):
        if self.StringToList == None:
            # return "No April Tag detected!"
            return None
        STL = StringToList(self.results)
        corners = STL.getCorners()
        return corners

    def getAngles(self):
        if self.StringToList == None:
            # return "No April Tag detected!"
            return None
        STL = StringToList(self.results)
        homography = STL.getHomography()
        homography = np.array(homography)
        _, Rs, Ts, Ns = cv2.decomposeHomographyMat(homography, self.camera_cal_matrix)
        angles = []
        for rotation_matrix in Rs:
        	r = R.from_dcm(rotation_matrix)
        	angle = r.as_euler('xyz', degrees = True)
        	angles.append(angle)
        return angles


# TEST FUNCTIONS
# image_dir = "90_degrees.png"
# image = cv2.imread(image_dir, cv2.IMREAD_GRAYSCALE)
# # print(image)
# atd = AprilTagDetector(image)
# print(atd.getCorners())
# # printing z component angle
# print(atd.getAngles()[0][2])






