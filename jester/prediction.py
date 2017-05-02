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
    print(average(matrix, 3, 3))
    print(average(matrix.T, 3, 3))
    print(weightedSum(matrix, 3, 3))
    print(weightedSum(matrix.T, 3, 3))

def average(matrix, rowIndex, colIndex):
    count = 0
    total = 0
    for i in range(0, matrix.shape[0]):
        if i != rowIndex:
            rating = matrix[i][colIndex]
            if rating != 99:
                total += rating
                count += 1
    return total/count

def weightedSum(matrix, rowIndex, colIndex):
    normalizationSum = 0
    compSum = 0
    for i in range(0, matrix.shape[0]):
        if i != rowIndex:
            utility = matrix[i][colIndex]
            if utility != 99:
                similarity = np.corrcoef(matrix[i], matrix[rowIndex])[0][1]
                print(similarity)
                normalizationSum += abs(similarity)
                compSum += (similarity * utility)
    return float(compSum/normalizationSum)

if __name__ == "__main__":
    main()
