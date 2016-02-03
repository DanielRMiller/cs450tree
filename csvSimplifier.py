import numpy as np
import sys

def simplify(csv):
    # Figure out what the Columns Are
    columns = csv[0]

    # Get a list of number Columns
    numberColumnList = []
    for index, attribute in enumerate(columns):
        numberColumnList.append(index)

    # List of sets needed to change the numbers
    sets = []
    # Each index will need one of these sets
    for index in numberColumnList:
        sets.append(set())

    # Add all the possibilites (from every instance) for each column
    for instance in csv:
        for i, column in enumerate(numberColumnList):
            sets[i].add(instance[column])

    # Simplify the sets
    for i, column in enumerate(numberColumnList):
        # We assume this is a number list, let's check
        numberCol = True

        # If any value in the set is not a number then it is not a number column
        for value in sets[i]:
            if not isNumber(value):
                numberCol = False

        # If not a number column then we should not simplify (we do not know how)
        if numberCol:
            print("Number of bins of column ", i, ": ")
            numBins = input()

            # be sure to get a positive number
            while int(numBins) < 1:
                print("Bad number!\nNumber of bins of column ", i, ": ")
                numBins = input()

            cutoffs = []

            # The min and max for column
            # print (csv)
            maxNum = max(float(row[i]) for row in csv)
            minNum = min(float(row[i]) for row in csv)

            # calculate the cutoff points
            for j in range(int(numBins) - 1):
                cutoffs.append((maxNum - minNum) * ((j + 1) / int(numBins)) + minNum)

            # replace the values with bin value
            for j, instance in enumerate(csv):

                binNum = 0
                if float(instance[i]) > cutoffs[-1]:
                    binNum = len(cutoffs)

                else:
                    for k in range(len(cutoffs)):
                        if k != 0:
                            if cutoffs[k - 1] < float(instance[i]) <= cutoffs[k]:
                                binNum = k
                        else:
                            if float(instance[i]) <= cutoffs[k]:
                                binNum = k

                # replace it with the correct bin
                csv[j][i] = binNum

    # return the file
    return csv


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# This is here to ensure main is only called when
#   this file is run, not just loaded
if __name__ == "__main__":
    main(sys.argv)