import numpy as np
import os
import linecache
import math
import scipy.stats as sp

FILESIZE = 24983
NUMJOKES = 100
FILENAME = "test.csv"



def main():
    matrix = (np.loadtxt(open(FILENAME, "r"), delimiter = ","))[:,1:]
    #print(average(matrix, 3, 3)) # collab average
    #print(average(matrix.T, 3, 3)) # ib average
    #print(weightedSum(matrix, 3, 3)) # collab ws
    #print(weightedSum(matrix.T, 3, 3)) # ib ws
    print(adjustedWeightedSum(matrix, 3, 3)) # collab aws
    #print(adjustedWeightedSum(matrix.T, 3, 3)) # ib aws

def average(matrix, rowIndex, colIndex):
    count = 0
    total = 0
    for i in range(0, matrix.shape[0]):
        if i != rowIndex:
            rating = matrix[i][colIndex]
            if rating != 99:
                total += float(rating)
                count += 1
    return float(total/count)

def weightedSum(matrix, rowIndex, colIndex):
    normalizationSum = 0
    compSum = 0
    for i in range(0, matrix.shape[0]):
        if i != rowIndex:
            utility = float(matrix[i][colIndex])
            if utility != 99:
                similarity = float(np.corrcoef(matrix[i], matrix[rowIndex])[0][1]) # need to add our own Pearson correlation here, ensure our answers are correct, it wont need to be indexed
                print(similarity) # delete
                normalizationSum += abs(similarity)
                compSum += float(similarity * utility)

    return float(compSum/normalizationSum)

def adjustedWeightedSum(matrix, rowIndex, colIndex):
    normalizationSum = 0
    compSum = 0
    for i in range (0, matrix.shape[0]):
        if i != rowIndex:
            utility = float(matrix[i][colIndex])
            similarity = float(np.corrcoef(matrix[i], matrix[rowIndex])[0][1])
            print(similarity) # delete
            normalizationSum += float(abs(similarity))
            compSum += float(similarity * (utility - average(matrix.T, -1, i))) # item based all items - 1 user

    return float(average(matrix.T, -1, rowIndex) + float(compSum / normalizationSum))

if __name__ == "__main__":
    main()
