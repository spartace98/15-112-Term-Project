# this game handles all the top level game mode
# Citation: I am using the 15-112 coursenotes animation framework
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

from startScreenMode import StartMode
from pythonImageModule import CustomCarMode
from playScreenMode import GameMode
from gameOverMode import GameOverMode
from highScoresMode import ScoresMode
from helpMode import HelpMode
from calibration import VideoCapture
from cmu_112_graphics import *
from tkinter import *

# GAME FRAMEWORK
class AcadeDriver(ModalApp):
    def appStarted(app):
        # top level attributes
        app.finalTime = 0
        app.lastMode = None
        app.onCam = False
        app.designCar = False
        app.playerCar = None
        app.otherCars = None
        app.selfie = None
        # different modes
        app.startMode = StartMode()
        app.designMode = CustomCarMode()
        app.calibrationMode = VideoCapture()
        app.gameMode = GameMode()
        app.gameOverMode = GameOverMode()
        app.scoresMode = ScoresMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.startMode)

AcadeDriver(width = 800, height = 800)