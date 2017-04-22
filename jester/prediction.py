import linecache

def main():
    print(collaborativeAverage(0, 0))
    print(itemBasedAverage(0, 0))


def collaborative():
    print("hello")


# given the user number and joke number, find all joke ratings at joke number except at row of user
def collaborativeAverage(userNumber, jokeNumber):
    file = openFile()
    currentUser = 0
    count = 0
    total = 0
    for line in file:
        if currentUser != userNumber:
            info = line.split(",")
            rating = float(info[jokeNumber + 1])
            if rating != 99:
                total += rating
                count += 1
        currentUser += 1
    return total/count

def itemBasedAverage(userNumber, jokeNumber):
    total = 0
    line = linecache.getline("jester-data-1.csv", userNumber + 1)
    info = line.split(",")
    for i in range(1, len(info)):
        if i != jokeNumber + 1:
            rating = float(info[i])
            if rating != 99:
                total += rating
    return total/int(info[0])

def openFile():
    try:
        file = open("jester-data-1.csv", 'r')
    except:
        print("File failed to open.")
        exit(0)
    return file

if __name__ == "__main__":
    main()
