import linecache

filename = "jester-data-1.csv"

def main():
    print(collaborativeAverage(0, 0))
    print(itemBasedAverage(0, 0))

# given the user number and joke number, find all joke ratings at joke number except at row of user
def collaborativeAverage(userNumber, jokeNumber):
    currentUser = 0
    count = 0
    total = 0
    for i in range(1, FILESIZE):
        if currentUser != userNumber:
            line = linecache.getline(filename, i)
            info = line.split(",")
            rating = float(info[jokeNumber + 1])
            if rating != 99:
                total += rating
                count += 1
        currentUser += 1
    return total/count

def collaborativePearsonCorrelation(user1Number, user2Number, itemNumber):
    sumNumerator = 0
    sumDenominatorUser1 = 0
    sumDenominatorUser2 = 0
    user1 = linecache.getline(filename, user1Number + 1).split(",") # linecache indices start with 1
    user2 = linecache.getline(filename, user2Number + 1).split(",")
    avgUser1 = collaborativeAverage(user1Number, itemNumber)
    avgUser2 = collaborativeAverage(user2Number, itemNumber)
    for i in range(1, len(user1)):
        utilityUser1 = user1[i]
        utilityUser2 = user2[i]
        if not (utilityUser1 == 99 or utilityUser2 == 99):
            compUser1 = utilityUser1 - avgUser1
            compUser2 = utilityUser2 - avgUser2
            sumNumerator += compUser1 * compUser2
            sumDenominatorUser1 += compUser1 ** 2
            sumDenominatorUser2 += compUser2 ** 2

    return sumNumerator / Math.sqrt(sumDenominatorUser1 * sumDenominatorUser2)

def collaborativeWeightedSum(): # need to add appropriate params
    normalizationSum = 0
    compSum = 0

    for i in range(0, FILESIZE):
        if i != user:
            similarity = collabSim(user, i)
            normalizationSum += Math.abs(similarity)

def itemBasedAverage(userNumber, jokeNumber):
    total = 0
    line = linecache.getline(filename, userNumber + 1)
    info = line.split(",")
    for i in range(1, len(info)):
        if i != jokeNumber + 1:
            rating = float(info[i])
            if rating != 99:
                total += rating
    return total/int(info[0])

def itemBasedPearsonCorrelation(item1Number, item2Number):
    sumNumerator = 0
    sumDenominatorItem1 = 0
    sumDenominatorItem2 = 0
    for i in range(0, FILESIZE):
        line = linecache.getline(file, i).split(".");
        utilityItem1 = line[item1Number + 1]
        utilityItem2 = line[item2Number + 1]
        if not (utilityItem1 == 99 or utilityItem2 == 99):
            avgItem1 = itemBasedAverage(item1Number1, i) # check to see if our avg function includes the same item/user
            avgItem2 = itemBasedAverage(item2Number, i)
            compItem1 = utilityItem1 - avgItem1
            compItem2 = utilityItem2 - avgItem2
            sumNumerator += compItem1 * compItem2
            sumDenominatorItem1 += compItem1 ** 2
            sumDenominatorItem2 += compItem2 ** 2

    return sumNumerator / Math.sqrt(sumDenominatorItem1 * sumDenominatorItem2)


def openFile():
    try:
        file = open(filename, 'r')
    except:
        print("File failed to open.")
        exit(0)
    return file



if __name__ == "__main__":
    main()
