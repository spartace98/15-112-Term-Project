"""
TECH DEMO FOR MATPLOTLIB PYTPLOT
TECH DEMO FOR NUMPY AND PANDAS DATAFRAME
TECH DEMO FOR UPLOADS
"""
import os
import numpy as np
import pandas as pd

class HighScore(object):
	def __init__(self):
		self.fileName = "highscores.txt"
		self.existingScores = pd.read_csv(self.fileName)
		self.maxEntries = 20
		
	def addNewEntry(self, newName, newScore, newDate):
		newEntry = pd.DataFrame({"Name":[newName], \
			"Score":[newScore], "Date":[newDate]})
		self.existingScores = self.existingScores.append(newEntry)
		self.existingScores = self.existingScores.sort_values("Score", ascending = True)
		self.existingScores.reset_index(drop = True, inplace=True)

	def getResults(self):
		self.existingScores = self.existingScores.sort_values("Score", ascending = True)
		return self.existingScores

	def saveResults(self):
		# only saves the top (self.maxEntries) highscores
		scores = self.existingScores[:self.maxEntries]
		filepath = os.getcwd()
		path = os.path.join(filepath, self.fileName)
		print(scores)
		pd.DataFrame.to_csv(scores, path, sep = ",", index = False)

# scores = HighScore()
# # GET CURRENT RESULTS
# print(scores.getResults())
# print()
# scores.addNewEntry("Grace", 500, "Nov 20")
# print(scores.getResults())
# scores.saveResults()


