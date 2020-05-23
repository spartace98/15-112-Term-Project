# 15-112 Term Project

# Introduction
For my Term Project, I was trying to push the limits of the feedback between the April Tag libraries available online and a control system. 

Without the need for a physical robot, we can test this feedback with simple tasks such as a graphics game. (Do refer to the repositiory titled Object Detection for one such example). 

However to push the limits of this feedback loop, I wrote a much more complex game which involved multiple movements and calculations at any point of detection. 

The game design also allowed me to work with camera calibration, which is an important step required for more accurate detection of objects.

# Details of the Game
My name of the game is Arcade Racer. 

Like an arcade racing game, this game allows player to physically steer the car with a wheel instead of conventional keyboard keys. 

This is done by using image recognition of the angle of rotation of the april tag wheel that I built. 

The roads and the cars are completely randomly generated. Everytime the player starts the game, it is a new road path with new cars generated at random positions on the road.

*How to run the project*
1. Preferably run the project from the terminal (command line), as new privacy settings of mac os may prevent users from directly accessing their video camera. (USE PYTHON 3!)
2. Use terminal and change directory to the Game Engine folder
3. Run the script in Game Engine folder titled fullGameMode.py. This file contains all the packages required to start and play the game

*ONLY IF YOU WANT TO CALIBRATE YOUR OWN CAMERA*
Note that different cameras have different camera calibration matrix. The user can calibrate his camera as follows. 
1. In the Camera Calibration Folder, print the checkerboard image
2. Take 5 or more photos using the same (computer) camera you will be using to play the game. Some example images are in the calibration_images folder.
3. Delete the existing images in the calibration_images folder and replace with your new images
4. Run the script titled camera_calibration.py and copy the matrix generated in your console
5. In the folder Game Engine, find the script titled aprilTagDetectorv2. There is an attribute in this script called self.camera_cal_matrix. Replace thus matrix (do not remove the numpy array conversion though)
6. The game should now run based on the calibration of your camera. 

# Conclusions/Findings
1. The python april tag library available online is sufficiently powerful to handle real time detection while performing a given task (w.r.t speed). 
2. Increasing the number of the calibration grid taken at different angles improves the accuracy of the camera calibration matrix generated, and thus provides greater accuracy in the position and dimensions of the April Tag detection.
3. The library however does not provide a measurement of depth (e.g distance between the camera and the april tag)

# Future Work
1. Using SVR to predict the depth between the camera and the April Tag
2. Better filtering of environment for easier detection of April Tag
