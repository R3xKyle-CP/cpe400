import numpy as np
import math
import scipy.stats as sp
from prediction import *
import random

FILENAME = "jester-data-1.csv"
TRIALS = 20




def main():
    CN = 10
    IBN = 5
    j = 0
    while (CN <= 50 or IBN <= 20):
        try:
            predictionCalls = [
                ("Nearest Neighbors Collaborative Average: N = " + str(CN), lambda matrix, userNumber, itemNumber: nearestNeighborsAverage(matrix, CN, userNumber, itemNumber)),
                ("Nearest Neighbors Item Based Average N = " + str(IBN), lambda matrix, userNumber, itemNumber: nearestNeighborsAverage(matrix.T, IBN, itemNumber, userNumber)),
                ("Nearest Neighbors Collaborative Weighted Sum N = " + str(CN), lambda matrix, userNumber, itemNumber: nearestNeighborsWeightedSum(matrix, CN, userNumber, itemNumber)),
                ("Nearest Neighbors Item Based Weighted Sum N = " + str(IBN), lambda matrix, userNumber, itemNumber: nearestNeighborsWeightedSum(matrix.T, IBN, itemNumber, userNumber)),
                ("Nearest Neighbors Collaborative Adjusted Weighted Sum N = " + str(CN), lambda matrix, userNumber, itemNumber: nearestNeighborsAdjustedWeightedSum(matrix, CN, userNumber, itemNumber)),
                ("Nearest Neighbors Item Based Adjusted Weighted Sum N = " + str(IBN), lambda matrix, userNumber, itemNumber: nearestNeighborsAdjustedWeightedSum(matrix.T, IBN, itemNumber, userNumber))
            ]
            matrix = (np.loadtxt(open(FILENAME, "r"), delimiter = ","))[:,1:]
            for predictionCall in predictionCalls:
                errorData = getError(matrix, predictionCall[1])
                normalizedErrorData = normalizeData(matrix, errorData)
                meansquaredError = meanSquaredError(errorData)
                print("Mean Absolute Error for " + predictionCall[0] + ": " + str(meanAbsoluteError(errorData)))
                print("Mean Squared Error for " + predictionCall[0] + ": " + str(meansquaredError))
                print("Root Mean Squared Error for " + predictionCall[0] + ": " + str(math.sqrt(meansquaredError)))
                print("Normalized Mean Absolute Error for " + predictionCall[0] + ": " + str(meanAbsoluteError(normalizedErrorData)))

            CN += 1
            IBN += 1
            j = 0
        except:
            print("Test failed for either CN = " + str(CN) + " or IBN = " + str(IBN))
            if (j == 0 or IBN > 30):
                print("Trying to increase CN by 1; now it is " + str(CN + 1))
                CN += 1
                j = 1
            elif (j == 1):
                print("Trying to increase IBN by 1; now it is " + str(IBN + 1) + "; Subtracting 1 from CN; now it is " + str(CN - 1))
                j = 2
                CN -= 1
                IBN += 1
            else:
                print("Both failed")
                j = 0
                CN += 1

def meanAbsoluteError(errorData):
    totalError = 0
    for error in errorData[0]:
        totalError += abs(error)
    return totalError / abs(errorData[1])

def meanSquaredError(errorData):
    totalError = 0
    for error in errorData[0]:
        totalError += error ** 2
    return totalError / abs(errorData[1])

def getError(matrix, predictionCall):
    errors = []
    total = 0
    for i in range(TRIALS):
        actual = 99
        while actual == 99:
            userNumber = random.randint(0, matrix.shape[0] - 1)
            itemNumber = random.randint(0, matrix.shape[1] - 1)
            actual = matrix[userNumber][itemNumber]
        predicted = predictionCall(matrix, userNumber, itemNumber)
        errors.append(predicted - actual)
        total += actual
    return (errors, total)

def normalizeData(matrix, errorData):
    maxableMatrix = np.where(matrix < 99, matrix, -99)
    normalizationFactor = np.amax(maxableMatrix) - np.amin(matrix)
    return (errorData[0], errorData[1] * normalizationFactor)


if __name__ == "__main__":
    main()
