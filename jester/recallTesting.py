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
        print(predictionCall[0] + " AveragePrecision: " + str(hits[1] / hits[2]) + " AverageRecall: " + str(hits[0] / hits[2]))

def getHits(matrix, predictionCall):
    totalRecall = 0
    totalPrecision = 0
    nums = 100
    for i in range(100):
        TP = 0
        FP = 0
        FN = 0
        count = 0
        user = random.randint(0, 24972)
        for j in range(100):
            if matrix[user][j] != 99:
                actualHit = False
                predictedHit = False
                actual = matrix[user][j]
                if actual != 99:
                    predicted = predictionCall(matrix, user, j)
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
                    count += 1
        if count == 0:
            nums -= 1
        else:
            if TP == 0:
                recall = 0
                precision = 0
            else:
                recall = TP / (TP + FN)
                precision = TP / (TP + FP)
            print("User: {0:d} Recall: {1:.3f} Precision {2:.3f}".format(user, recall, precision))
            totalRecall += recall
            totalPrecision += precision

    return (totalRecall, totalPrecision, nums)


if __name__ == "__main__":
    main()
