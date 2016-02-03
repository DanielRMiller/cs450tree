import os
import numpy
from treeClassifier import TreeClassifier
class FileError(Exception):
    """Exception raised for errors in the file input.

    Attributes:
        filename -- input file in which the error occurred
    """

    def __init__(self, filename, message):
        self.filename = filename
        self.message = message

csvFile = 'simpleIris.csv'
if os.stat(csvFile).st_size == 0:
	raise FileError(csvFile, " is empty")
csv = numpy.genfromtxt(csvFile, delimiter=",", dtype=str)
numcols = len(csv[0])
data = csv[:, :-1]
targets = csv[:,-1]
# Randomize the order of the instances in the dataset. Don't forget that you need to keep the targets matched up with the approprite instance.
# This permutation will be used for both the data and the target so it will line up correctly.
perm = numpy.random.permutation(len(data))

data = data[perm]
targets = targets[perm]
# Split the data into two sets: a training set (70%) and a testing set (30%)
# Index of where to split (we want this to be an integer)
index = int(round(perm.size*.3))
test = perm[:index]
train = perm[index:]
# Instantiate your new classifier
classifier = TreeClassifier()
# "Train" it with data
# print ("Test Data: ", data[train])
classifier.train(data[train], targets[train], True)
# print ("Root: ", classifier.root.attribute)
# Make "Predictions" on the test data
predictions = classifier.predict(data[test])
# Reset correct answers
correct = 0
# Count the answers that we got right
for (prediction, actual) in zip(predictions, test):
	if prediction == targets[actual]:
		correct += 1
#Determine the accuracy of your classifier's predictions (reported as percentage)
print (correct/test.size*100)