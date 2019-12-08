*Project Description*
My Project name is "Arcade Racer
Like an arcade racing game, this game allows player to physically steer the car with a wheel instead of conventional keyboard keys. 
This is done by using image recognition of the angle of rotation of the april tag wheel that I built. (design of april tag is however not by me)
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

*What libraries I am using that need to be installed*
1. The April Tag Library (https://pypi.org/project/apriltag/)
2. OpenCV (cv2)
3. Numpy
4. Pandas
5. 15-112 tkinter framework (tkinter, cmu_112_graphics, PIL)
6. Scipy
7. Pandas
Those that should already be installed by default
8. datetime (should be preinstalled for some computers)
9. math
10. os
11. random
12. copy

*Shortcut commands*
1. Accessing the Help Mode by pressing 'h'
2. Accessing the High Score Mode in Start Mode by pressing Spacebar
3. If the user chooses to play with camera, the camera will take a screenshot of the user to be display at the end of the game. 


