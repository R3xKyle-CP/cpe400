import Math


int FILESIZE = 24983

---------------------------
collaborative Pearson correlation

take in indices instead of row/column
u[c] = row of user c # param
u[c'] = row of user c' # param
sumNumerator = 0
sumDenominatorUser1 = 0
sumDenominatorUser2 = 0
user1 = linecache(index of user 1).split()
user2 = linecache(index of user 2).split()
avgUser1 = collAvg(user1)
avgUser2 = collAvg(user2)
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


---------------------------
item-based Pearson correlation

take in indices
u[s] = column of joke ratings

sumNumerator = 0
sumDenominatorItem1 = 0
sumDenominatorItem2 = 0
item1 = index of item # param
item2 = index of item # param
avgItem1 = itemBAvg(item1)
avgItem2 = itemBAvg(item2) # check to see if our avg function includes the same item/user
for i in range(0, FILESIZE):
    line = linecache.getline(file, i).split(".");
    utilityItem1 = line[item1 + 1]
    utilityItem2 = line[item2 + 1]
    if not (utilityItem1 == 99 or utilityItem2 == 99):
        compItem1 = utilityItem1 - avgItem1
        compItem2 = utilityItem2 - avgItem2
        sumNumerator += compItem1 * compItem2
        sumDenominatorItem1 += compItem1 ** 2
        sumDenominatorItem2 += compItem2 ** 2

return sumNumerator / Math.sqrt(sumDenominatorItem1 * sumDenominatorItem2)


-----------------------
Collaborative weighted sum


user #index of user(c) param
item # index of item(s) param

normalizationSum = 0
compSum = 0

for i in range(0, FILESIZE):
    if i != user:
        similarity = collabSim(user, i)
        normalizationSum += Math.abs(similarity)
