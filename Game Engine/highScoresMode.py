# this scipt only handles the higb score mode
# Citation: I am using the 15-112 coursenotes animation framework
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
from cmu_112_graphics import *
from tkinter import *
import os
from highScoreMonitor import HighScore

# append the player score and mode
class ScoresMode(Mode):
    def appStarted(mode):
        mode.scores = HighScore().getResults()
        mode.rows, mode.cols = mode.scores.shape

        # mode.app.lastMode = mode.app.scoresMode

    def createTable(mode, canvas):
        cellWidth, cellHeight = mode.width//6, 50
        startX, startY = mode.width//4, 150
        header = ["Name", "Time", "Date"]
        colors = ["seagreen1", "deepskyblue2", "steelblue1", "steelblue2", "steelblue3", "deepskyblue3", "dodgerblue2", "royalblue1", "royalblue2", "royalblue3", "dodgerblue3"]
        # first create the table 
        for i in range(mode.cols):
            # 11 rows, including the title
            for j in range(min(mode.rows, 10)+1):
                color = colors[j]
                x0, x1 = startX + i*cellWidth, startX + (i+1)*cellWidth
                y0, y1 = startY + j*cellHeight, startY + (j+1)*cellHeight
                canvas.create_rectangle(x0, y0, x1, y1, fill = color)
                
        # next create the header text
        for i in range(mode.cols): 
            # this is the header row
            text = header[i]
            x0, x1 = startX + i*cellWidth, startX + (i+1)*cellWidth
            y0, y1 = startY, startY + cellHeight
            cx, cy = 0.5*(x0+x1), 0.5*(y0+y1)
            canvas.create_text(cx, cy, text = text, font = "Phosphate 30 bold", fill = "purple")

        startY = startY + cellHeight
        for i in range(mode.cols):
            # 10 rows
            for j in range(min(mode.rows, 10)):
                x0, x1 = startX + i*cellWidth, startX + (i+1)*cellWidth
                y0, y1 = startY + j*cellHeight, startY + (j+1)*cellHeight
                cx, cy = 0.5*(x0+x1), 0.5*(y0+y1)
                text = mode.scores.iloc[j, i]
                if i == 1:
                    # if the text is time, convert it to minutes and seconds
                    minutes, seconds = mode.convertSecondsToMinutes(text)
                    if seconds < 10:
                        seconds = f"0{seconds}"
                    text = f"{minutes}:{seconds}"
                if j < 3:
                    font = "Phosphate 20 bold"
                    color = "firebrick3"
                else:
                    font = "Phosphate 15"
                    color = "black"
                canvas.create_text(cx, cy, text = text, font = font, fill = color)


    def convertSecondsToMinutes(mode, time):
        minutes = time//60
        seconds = time%60
        return (minutes, seconds)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'black')
        # create the scored board
        mode.createTable(canvas)

        canvas.create_text(mode.width//2, 100, text = "LEADERBOARD", fill = "hotpink", font = "Phosphate 80 italic")
        # for i in range(numScores):
        #     text = f"{names[i]} {scores[i]} {dates[i]}"
        #     canvas.create_text(startX, startY, text = text)
        #     startY += 50

        canvas.create_text(mode.width//2, mode.height - 50, text = "Press R to restart", fill = "cyan", font = "Phosphate 50 italic")

    def keyPressed(mode, event):
        if event.key == "r":
            mode.app.setActiveMode(mode.app.gameMode)
            mode.app.gameMode.appStarted()

        # elif event.key == 'h':
        #     mode.app.setActiveMode(mode.app.helpMode)

        # can only display high score in start mode
        elif event.key == "Space" and mode.app.lastMode == mode.app.startMode:
            mode.app.setActiveMode(mode.app.lastMode)





