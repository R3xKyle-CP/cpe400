import numpy as np
import math
import scipy.stats as sp
from prediction import *
import random

FILENAME = "jester-data-1.csv"
SUCCESS_THRESHHOLD = 5
CN = 10
IBN = 5

predictionCalls = [
    ("collaborativeAverage", lambda matrix, userNumber, itemNumber: average(matrix, userNumber, itemNumber)),
    #("itemBasedAverage", lambda matrix, userNumber, itemNumber: average(matrix.T, itemNumber, userNumber)),
    #("collaborativeWeightedSum", lambda matrix, userNumber, itemNumber: weightedSum(matrix, userNumber, itemNumber)),
    #("itemBasedWeightedSum", lambda matrix, userNumber, itemNumber: weightedSum(matrix.T, itemNumber, userNumber)),
    #("collaborativeAdjustedWeightedSum", lambda matrix, userNumber, itemNumber: adjustedWeightedSum(matrix, userNumber, itemNumber)),
    #("itemBasedAdjustedWeightedSum", lambda matrix, userNumber, itemNumber: adjustedWeightedSum(matrix.T, itemNumber, userNumber)),
    #("nearestNeighborsCollaborativeAverage", lambda matrix, userNumber, itemNumber: nearestNeighborsAverage(matrix, CN, userNumber, itemNumber)),
    #("nearestNeighborsItemBasedAverage", lambda matrix, userNumber, itemNumber: nearestNeighborsAverage(matrix.T, IBN, itemNumber, userNumber)),
    #("nearestNeighborsCollaborativeWeightedSum", lambda matrix, userNumber, itemNumber: nearestNeighborsWeightedSum(matrix, CN, userNumber, itemNumber)),
    #("nearestNeighborsItemBasedWeightedSum", lambda matrix, userNumber, itemNumber: nearestNeighborsWeightedSum(matrix.T, IBN, itemNumber, userNumber)),
    #("nearestNeighborsCollaborativeAdjustedWeightedSum", lambda matrix, userNumber, itemNumber: nearestNeighborsAdjustedWeightedSum(matrix, CN, userNumber, itemNumber)),
    #("nearestNeighborsItemBasedAdjustedWeightedSum", lambda matrix, userNumber, itemNumber: nearestNeighborsAdjustedWeightedSum(matrix.T, IBN, itemNumber, userNumber))
]

def main():
    matrix = (np.loadtxt(open(FILENAME, "r"), delimiter = ","))[:,1:]
    for predictionCall in predictionCalls:
        fp = open(predictionCall[0] + ".csv", 'w')
        getPredictions(fp, matrix, predictionCall[1])
        fp.close()

def getPredictions(writeFile, matrix, predictionCall):
    for i in range(matrix.shape[0]):
        if i % 100 == 0:
            print(str(i))
        for j in range(matrix.shape[1]):
            actualHit = False
            predictedHit = False
            actual = matrix[i][j]
            if actual != 99:
                predicted = predictionCall(matrix, i, j)
                writeFile.write(str(predicted))
            else:
                writeFile.write("99")
            if j == matrix.shape[1] - 1:
                writeFile.write("\n")
            else:
                writeFile.write(", ")

if __name__ == "__main__":
    main()
