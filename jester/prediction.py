import linecache
import math
import os

FILESIZE = 24983
NUMJOKES = 100
FILENAME = "jester-data-1.csv"
FILENAMENNC = "nearestNeighborsC.csv"
FILENAMENNIB = "nearestNeighborsIB.csv"

def main():
#    print("Collaborative Average - User 24983, Joke 100: " + str(collaborativeAverage(499, 49)))
    print("Item Based Average - User 24983, Joke 100: " + str(itemBasedAverage(499, 49)))
#    print("Collaborative Pearson Correlation - User 24983, User 24982: " + str(collaborativePearsonCorrelation(FILESIZE - 1, FILESIZE - 2)))
#    print("Item Based Pearson Correlation - Joke 99, Joke 100: " + str(itemBasedPearsonCorrelation(98, 99)))
#    print("--------------------------------------------Test Cases ^^^-------------------------------------------------------------------")
#    print("Collaborative Average - User 1, Joke 1: " + str(collaborativeAverage(0, 0)))
#    print("Item based Average - User 1, Joke 1: " + str(itemBasedAverage(0, 0)))
#    print("Collaborative Pearson Correlation - User 1, User 2: " + str(collaborativePearsonCorrelation(0, 1)))
#    print("Item Based Pearson Correlation - Joke 1, Joke 2: " + str(itemBasedPearsonCorrelation(0, 1)))
#    print("Collaborative Weighted Sum - User 1, Joke 1: " + str(collaborativeWeightedSum(0,0)))
#    print("Collaborative Adjusted Weighted Sum - User 1, Joke 1: " + str(collaborativeAdjustedWeightedSum(0,0)))
#    print("Item Based Weighted Sum - User 1, Joke 1: " + str(itemBasedWeightedSum(0,0)))
#    print("Item Based Adjusted Weighted Sum - User 1, Joke 1: " + str(itemBasedAdjustedWeightedSum(0, 0)))
#    print("Nearest Neighbors Collaborative Average - User 500, Joke 50, N 5: " + str(nearestNeighborsCollaborativeAverage(499, 49, 24982)))
    print("Nearest Neighbors Item Based Average: " + str(nearestNeighborsItemBasedAverage(499, 49, 99)))

# given the user number and joke number, find all joke ratings at joke number except at row of user
def collaborativeAverage(userNumber, itemNumber, fileName = FILENAME, fileSize = FILESIZE):
    currentUser = 0
    count = 0
    total = 0
    for i in range(0, fileSize):
        if currentUser != userNumber:
            info = linecache.getline(fileName, i + 1).split(",")
            rating = float(info[itemNumber + 1])
            if rating != 99:
                total += rating
                count += 1
        currentUser += 1
    return total/count

def collaborativeWeightedSum(userNumber, itemNumber, fileName = FILENAME, fileSize = FILESIZE): # need to add appropriate params
    normalizationSum = 0
    compSum = 0
    for i in range(0, fileSize):
        if i != userNumber:
            info = linecache.getline(fileName, i + 1).split(",")
            utilityUserI = float(info[itemNumber + 1])
            if utilityUserI != 99:
                similarity = collaborativePearsonCorrelation(userNumber, i)
                normalizationSum += abs(similarity)
                compSum += (similarity * utilityUserI)

    return compSum/normalizationSum

def collaborativeAdjustedWeightedSum(userNumber, itemNumber, fileName = FILENAME, fileSize = FILESIZE):
    normalizationSum = 0
    compSum = 0
    for i in range(0, fileSize):
        if i != userNumber:
            info = linecache.getline(fileName, i + 1).split(",")
            utilityUserI = float(info[itemNumber + 1])
            if utilityUserI != 99:
                similarity = collaborativePearsonCorrelation(userNumber, i)
                normalizationSum += abs(similarity)
                compSum += (similarity * (utilityUserI - itemBasedAverage(i, -1)))

    return (itemBasedAverage(userNumber, -1) + (compSum/normalizationSum))

def collaborativePearsonCorrelation(user1Number, user2Number, fileName = FILENAME):
    sumNumerator = 0
    sumDenominatorUser1 = 0
    sumDenominatorUser2 = 0
    user1 = linecache.getline(fileName, user1Number + 1).split(",") # linecache indices start with 1
    user2 = linecache.getline(fileName, user2Number + 1).split(",")
    avgUser1 = itemBasedAverage(user1Number, -1) # -1 to ensure that it does not skip any joke
    avgUser2 = itemBasedAverage(user2Number, -1)
    for i in range(1, len(user1)):
        utilityUser1 = float(user1[i])
        utilityUser2 = float(user2[i])
        if not (utilityUser1 == 99 or utilityUser2 == 99):
            compUser1 = utilityUser1 - avgUser1
            compUser2 = utilityUser2 - avgUser2
            sumNumerator += compUser1 * compUser2
            sumDenominatorUser1 += compUser1 ** 2
            sumDenominatorUser2 += compUser2 ** 2

    return sumNumerator / math.sqrt(sumDenominatorUser1 * sumDenominatorUser2)

def itemBasedAverage(userNumber, itemNumber, fileName = FILENAME):
    total = 0
    line = linecache.getline(fileName, userNumber + 1)
    info = line.split(",")
    for i in range(1, len(info)):
        if i != itemNumber + 1:
            rating = float(info[i])
            if rating != 99:
                total += rating
    return total/int(info[0])

def itemBasedWeightedSum(userNumber, itemNumber, fileName = FILENAME):
    normalizationSum = 0
    compSum = 0
    info = linecache.getline(fileName, userNumber + 1).split(",")
    for i in range(1, len(info)):
        if i != itemNumber + 1:
            utilityItemI = float(info[i])
            if utilityItemI != 99:
                similarity = itemBasedPearsonCorrelation(itemNumber, i - 1)
                normalizationSum += abs(similarity)
                compSum += (similarity * utilityItemI)

    return compSum/normalizationSum

def itemBasedAdjustedWeightedSum(userNumber, itemNumber, fileName = FILENAME):
    normalizationSum = 0
    compSum = 0
    info = linecache.getline(fileName, userNumber + 1).split(",")
    for i in range(1, len(info)):
        if i != itemNumber + 1:
            utilityItemI = float(info[i])
            if utilityItemI != 99:
                similarity = itemBasedPearsonCorrelation(itemNumber, i - 1)
                normalizationSum += abs(similarity)
                compSum += (similarity * (utilityItemI - collaborativeAverage(-1, i)))

    return (collaborativeAverage(-1, itemNumber) + (compSum/normalizationSum))

def itemBasedPearsonCorrelation(item1Number, item2Number, fileName = FILENAME, fileSize = FILESIZE):
    sumNumerator = 0
    sumDenominatorItem1 = 0
    sumDenominatorItem2 = 0
    avgItem1 = collaborativeAverage(-1, item1Number) # -1 to ensure that it does not skip any user by
    avgItem2 = collaborativeAverage(-1, item2Number)
    for i in range(0, fileSize):
        line = linecache.getline(fileName, i + 1).split(",");
        utilityItem1 = float(line[item1Number + 1])
        utilityItem2 = float(line[item2Number + 1])
        if not (utilityItem1 == 99 or utilityItem2 == 99): # if either user did not rate the joke, do not calculate

            compItem1 = utilityItem1 - avgItem1
            compItem2 = utilityItem2 - avgItem2
            sumNumerator += compItem1 * compItem2
            sumDenominatorItem1 += compItem1 ** 2
            sumDenominatorItem2 += compItem2 ** 2

    return sumNumerator / math.sqrt(sumDenominatorItem1 * sumDenominatorItem2)

def getNearestNeighborsCollaborative(userNumber, n):
    nearestNeighbors = [[-2, -1] for i in range(n)]
    numberFilled = 0
    for i in range(0, FILESIZE):
        if i != userNumber:
            info = linecache.getline(FILENAME, i + 1).split(",")
            similarity = collaborativePearsonCorrelation(userNumber, i)
            if similarity > nearestNeighbors[0][0]:
                #print("Before assigning")
                #print(nearestNeighbors)
                nearestNeighbors[0][0] = similarity
                #print("After assigning")
                #print(nearestNeighbors)
                nearestNeighbors[0][1] = i
                #print("Before sorted: ")
                #print(nearestNeighbors)
                nearestNeighbors = sorted(nearestNeighbors, key=lambda x: x[0])
                #print("After sorted: ")
                #print(nearestNeighbors)

    file = open(FILENAMENNC, 'w')
    for j in range(0, n):
        file.write(linecache.getline(FILENAME, nearestNeighbors[j][1] + 1))
    file.write(linecache.getline(FILENAME, userNumber + 1))

def getNearestNeighborsItemBased(itemNumber, n):
    nearestNeighbors = [[-2, -1] for i in range(n)]
    numberFilled = 0
    for i in range(0, NUMJOKES):
        if i != itemNumber:
            similarity = itemBasedPearsonCorrelation(itemNumber, i);
            if similarity > nearestNeighbors[0][0]:
                nearestNeighbors[0][0] = similarity
                nearestNeighbors[0][1] = i
                nearestNeighbors = sorted(nearestNeighbors, key=lambda x: x[0])

    file = open(FILENAMENNIB, 'w')
    for i in range(0, FILESIZE):
        line = linecache.getline(FILENAME, i+1)
        info = line.split(',')
        lineOut = info[0] # concat at beginning of line out once you get count of actual jokes rated.
        for j in range(0, n):
            lineOut += "," + info[nearestNeighbors[j][1]]
        lineOut += "," + info[itemNumber]
        file.write(lineOut)

def nearestNeighborsCollaborativeAverage(userNumber, itemNumber, n):
    getNearestNeighborsCollaborative(userNumber, n)
    average = collaborativeAverage(n, itemNumber, FILENAMENNC, n + 1)
    deleteFile(FILENAMENNC)
    return average

def nearestNeighborsCollaborativeWeightedSum(userNumber, itemNumber, n):
    getNearestNeighborsCollaborative(userNumber, n)
    weightedSum = collaborativeWeightedSum(n, itemNumber, FILENAMENNC, n + 1)
    deleteFile(FILENAMENNC)
    return weightedSum

def nearestNeighborsCollaborativeAdjustedWeightedSum(userNumber, itemNumber, n):
    getNearestNeighborsCollaborative(userNumber, n)
    adjustedWeightedSum = collaborativeAdjustedWeightedSum(n, itemNumber, FILENAMENNC, n + 1)
    deleteFile(FILENAMENNC)
    return adjustedWeightedSum

def nearestNeighborsItemBasedAverage(userNumber, itemNumber, n):
    getNearestNeighborsItemBased(itemNumber, n)
    average = itemBasedAverage(userNumber, n, FILENAMENNIB)
    deleteFile(FILENAMENNIB)
    return average

def nearestNeighborsItemBasedWeightedSum(userNumber, itemNumber, n):
    getNearestNeighborsItemBased(itemNumber, n)
    weightedSum = itemBasedWeightedSum(userNumber, n, FILENAMENNIB)
    deleteFile(FILENAMENNIB)
    return weightedSum

def nearestNeighborsItemBasedAdjustedWeightedSum(userNumber, itemNumber, n):
    getNearestNeighborsItemBased(itemNumber, n)
    adjustedWeightedSum = itemBasedAdjustedWeightedSum(userNumber, n, FILENAMENNIB)
    deleteFile(FILENAMENNIB)
    return adjustedWeightedSum

def deleteFile(fileName):
    try:
        os.remove(fileName)
    except:
        pass



if __name__ == "__main__":
    main()
