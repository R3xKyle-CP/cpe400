import numpy as np
import math
import scipy.stats as sp
from prediction import *
import random

FILENAME = "jester-data-1.csv"
SUCCESS_THRESHHOLD = 2
CN = 10
IBN = 5

predictionCalls = [
    ("Collaborative Average", lambda matrix, userNumber, itemNumber: average(matrix, userNumber, itemNumber)),
    ("Item Based Average", lambda matrix, userNumber, itemNumber: average(matrix.T, itemNumber, userNumber)),
    ("Collaborative Weighted Sum", lambda matrix, userNumber, itemNumber: weightedSum(matrix, userNumber, itemNumber)),
    ("Item Based Weighted Sum", lambda matrix, userNumber, itemNumber: weightedSum(matrix.T, itemNumber, userNumber)),
    ("Collaborative Adjusted Weighted Sum", lambda matrix, userNumber, itemNumber: adjustedWeightedSum(matrix, userNumber, itemNumber)),
    ("Item Based Adjusted Weighted Sum", lambda matrix, userNumber, itemNumber: adjustedWeightedSum(matrix.T, itemNumber, userNumber)),
    ("Nearest Neighbors Collaborative Average", lambda matrix, userNumber, itemNumber: nearestNeighborsAverage(matrix, CN, userNumber, itemNumber)),
    ("Nearest Neighbors Item Based Average", lambda matrix, userNumber, itemNumber: nearestNeighborsAverage(matrix.T, IBN, itemNumber, userNumber)),
    ("Nearest Neighbors Collaborative Weighted Sum", lambda matrix, userNumber, itemNumber: nearestNeighborsWeightedSum(matrix, CN, userNumber, itemNumber)),
    ("Nearest Neighbors Item Based Weighted Sum", lambda matrix, userNumber, itemNumber: nearestNeighborsWeightedSum(matrix.T, IBN, itemNumber, userNumber)),
    ("Nearest Neighbors Collaborative Adjusted Weighted Sum", lambda matrix, userNumber, itemNumber: nearestNeighborsAdjustedWeightedSum(matrix, CN, userNumber, itemNumber)),
    ("Nearest Neighbors Item Based Adjusted Weighted Sum", lambda matrix, userNumber, itemNumber: nearestNeighborsAdjustedWeightedSum(matrix.T, IBN, itemNumber, userNumber))
]

def main():
    matrix = (np.loadtxt(open(FILENAME, "r"), delimiter = ","))[:,1:]
    for predictionCall in predictionCalls:
        hits = getHits(matrix, predictionCall[1])
        if (hits[0] + hits[1] != 0):
            print(predictionCall[0] + " Precision: " + str(hits[0] / (hits[0] + hits[1])))
        else:
            print(predictionCall[0] + " Precision: 0")
        if (hits[0] + hits[2] != 0):
            print(predictionCall[0] + " Recall: " + str(hits[0] / (hits[0] + hits[2])))
        else:
            print(predictionCall[0] + " Recall: 0")

def getHits(matrix, predictionCall):
    TP = 0
    FP = 0
    FN = 0
    for i in range(1000):
        user = random.randint(0, 24972)
        joke = random.randint(0, 99)
        while (matrix[user][joke] == 99):
            joke = random.randint(0, 99)
        actualHit = False
        predictedHit = False
        actual = matrix[user][joke]
        if actual != 99:
            predicted = predictionCall(matrix, user, joke)
            if actual >= SUCCESS_THRESHHOLD:
                actualHit = True
            if predicted >= SUCCESS_THRESHHOLD:
                predictedHit = True
            if actualHit and predictedHit:
                TP += 1
            elif actualHit and not predictedHit:
                FN += 1
            elif not actualHit and predictedHit:
                FP += 1
    #print(str(TP) + ", " + str(FP) + ", " + str(FN))
    return (TP, FP, FN)


if __name__ == "__main__":
    main()
