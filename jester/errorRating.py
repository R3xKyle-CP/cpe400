import numpy as np
import math
import scipy.stats as sp
from prediction import *

FILENAME = "test.csv"
TRIALS = 20

predictionCalls = {
    {"Collaborative Average", lambda matrix, userNumber, itemNumber: average(matrix, userNumber, itemNumber)},
    {"Item Based Average", lambda matrix, userNumber, itemNumber: average(matrix.T, itemNumber, userNumber)},
    {"Collaborative Weighted Sum", lambda matrix, userNumber, itemNumber: weightedSum(matrix, userNumber, itemNumber)},
    {"Item Based Weighted Sum", lambda matrix, userNumber, itemNumber: weightedSum(matrix.T, itemNumber, userNumber)},
    {"Collaborative Adjusted Weighted Sum", lambda matrix, userNumber, itemNumber: adjustedWeightedSum(matrix, userNumber, itemNumber)},
    {"Item Based Adjusted Weighted Sum", lambda matrix, userNumber, itemNumber: adjustedWeightedSum(matrix.T, itemNumber, userNumber)}
}

def main():
    matrix = (np.loadtxt(open(FILENAME, "r"), delimiter = ","))[:,1:]
    for predictionCall in predictionCalls:
        errorData = getError(matrix, predictionCall[1])
        normalizedErrorData = normalizeData(matrix, errorData)
        meanSquaredError = meanSquaredError(errorData)
        print("Mean Absolute Error for " + predictionCall[0] + ": " + str(meanAbsoluteError(errorData)))
        print("Mean Squared Error for " + predictionCall[0] + ": " + str(meanSquaredError))
        print("Root Mean Squared Error for " + predictionCall[0] + ": " + str(math.sqrt(meanSquaredError)))
        print("Normalized Mean Absolute Error for " + predictionCall[0] + ": " + str(meanAbsoluteError(normalizedErrorData)))

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
    normalizationFactor = maxableMatrix.amax() - matrix.amin()
    return (errorData[0], errorData[1] * normalizationFactor)
