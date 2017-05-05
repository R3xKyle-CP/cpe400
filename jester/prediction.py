import numpy as np
import os
import linecache
import math
import scipy.stats as sp

FILENAME = "jester-data-1.csv"



def main():
    matrix = (np.loadtxt(open(FILENAME, "r"), delimiter = ","))[:,1:] # remove first column (the total number of jokes rated by the user)
    print(average(matrix, 3, 3)) # collab average
    print(average(matrix.T, 3, 3)) # ib average
    print(weightedSum(matrix, 3, 3)) # collab ws
    print(weightedSum(matrix.T, 3, 3)) # ib ws
    print(adjustedWeightedSum(matrix, 3, 3)) # collab aws
    print(adjustedWeightedSum(matrix.T, 3, 3)) # ib aws
    print(nearestNeighborsAverage(matrix, 50, 3, 3))
    print(nearestNeighborsAverage(matrix.T, 20, 3, 3))
    print(nearestNeighborsWeightedSum(matrix, 50, 3, 3))
    print(nearestNeighborsWeightedSum(matrix.T, 20, 3, 3))
    print(nearestNeighborsAdjustedWeightedSum(matrix, 50, 3, 3))
    print(nearestNeighborsAdjustedWeightedSum(matrix.T, 20, 3, 3))

# With our dataset, matrix argument would be transposed for item-based
def average(matrix, rowIndex, colIndex):
    count = 0
    total = 0
    for i in range(matrix.shape[0]):
        if i != rowIndex:
            rating = matrix[i][colIndex]
            if rating != 99:
                total += float(rating)
                count += 1
    return float(total/count)

# With our dataset, matrix argument would be transposed for item-based
def weightedSum(matrix, rowIndex, colIndex):
    normalizationSum = 0
    compSum = 0
    for i in range(matrix.shape[0]):
        if i != rowIndex:
            utility = float(matrix[i][colIndex])
            if utility != 99:
                #similarity = float(np.corrcoef(matrix[i], matrix[rowIndex])[0][1]) # need to add our own Pearson correlation here, ensure our answers are correct, it wont need to be indexed
                similarity = float(pearsonCorrelation(matrix, i, rowIndex))
                #print(similarity) # delete
                normalizationSum += abs(similarity)
                compSum += float(similarity * utility)

    return float(compSum/normalizationSum)

# With our dataset, matrix argument would be transposed for item-based
def adjustedWeightedSum(matrix, rowIndex, colIndex):
    normalizationSum = 0
    compSum = 0
    for i in range (matrix.shape[0]):
        if i != rowIndex:
            utility = float(matrix[i][colIndex])
            if utility != 99:
                #similarity = float(np.corrcoef(matrix[i], matrix[rowIndex])[0][1])
                similarity = float(pearsonCorrelation(matrix, i, rowIndex))
                #print(similarity) # delete
                normalizationSum += float(abs(similarity))
                compSum += float(similarity * (utility - average(matrix.T, -1, i))) # item based all items - 1 user

    return float(average(matrix.T, -1, rowIndex) + float(compSum / normalizationSum))

def getNearestNeighbors(matrix, n, rowIndex):
    nearestNeighbors = [[-2, -2] for i in range(n + 1)]
    for i in range(matrix.shape[0]):
        #similarity = float(np.corrcoef(matrix[i], matrix[rowIndex])[0][1])
        similarity = float(pearsonCorrelation(matrix, i, rowIndex))
        if similarity > float(nearestNeighbors[0][0]):
            nearestNeighbors[0][0] = similarity
            nearestNeighbors[0][1] = i
            nearestNeighbors = sorted(nearestNeighbors, key=lambda x: x[0])
    returnMatrix = matrix[[j[1] for j in nearestNeighbors]]
    return returnMatrix

def nearestNeighborsAverage(matrix, n, rowIndex, colIndex):
    nearestNeighbors = getNearestNeighbors(matrix, n, rowIndex)
    return average(nearestNeighbors, n, colIndex)

def nearestNeighborsWeightedSum(matrix, n, rowIndex, colIndex):
    nearestNeighbors = getNearestNeighbors(matrix, n, rowIndex)
    return weightedSum(nearestNeighbors, n, colIndex)

def nearestNeighborsAdjustedWeightedSum(matrix, n, rowIndex, colIndex):
    nearestNeighbors = getNearestNeighbors(matrix, n, rowIndex)
    return adjustedWeightedSum(nearestNeighbors, n, colIndex)

def pearsonCorrelation(matrix, row1Index, row2Index):
    sumNumerator = 0
    sumDenominatorRow1 = 0
    sumDenominatorRow2 = 0
    averageRow1 = average(matrix.T, -1, row1Index)
    averageRow2 = average(matrix.T, -1, row2Index)
    for i in range(matrix.shape[1]):
        utilityRow1 = matrix[row1Index][i]
        utilityRow2 = matrix[row2Index][i]
        if not (utilityRow1 == 99 or utilityRow2 == 99):
            compRow1 = utilityRow1 - averageRow1
            compRow2 = utilityRow2 - averageRow2
            sumNumerator += compRow1 * compRow2
            sumDenominatorRow1 += compRow1 ** 2
            sumDenominatorRow2 += compRow2 ** 2
    return sumNumerator / math.sqrt(sumDenominatorRow1 * sumDenominatorRow2)


if __name__ == "__main__":
    main()
