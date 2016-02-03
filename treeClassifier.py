# Import some files
import sys
import copy
import numpy
import random
import json

class Node:
    def __init__(self, value = 0, labels = []):
        self.attribute = value
        # This needs to hold various types of data
        #  * String or Integer means it is a leaf
        #  * Node means it is a well... node
        self.branches = {}

def calculate_entropy(probabilities):
    to_return = 0
    for probability in probabilities.values():
        if probability != 0:
            to_return += -probability * np.log2(probability);

    return to_return

def calcLoss(data, label):
	# Reset the informationLoss
	informationLoss = 0
	values = []
	for instance in data:
	    if instance[label] not in values:
	        values.append(instance[label])
	for value in values:
		# Get all the valid instances for this value
		instances = [instance for instance in data if instance[label] == value]
		# To keep track of the frequencies of each target
		frequencies = {}
		for instance in instances:
			# If the instance is already keyed, increment, else create
		    if instance[-1] in frequencies.keys():
		        frequencies[instance[-1]] += 1
		    else:
		        frequencies[instance[-1]] = 1

		# Set as percent rather than count
		for key in frequencies.keys():
		    frequencies[key] = frequencies[key] / len(instances)

		valueEntropy = 0;
		for probability in frequencies.values():
			if probability != 0:
			    valueEntropy += -probability * numpy.log2(probability);

		informationLoss += (len(instances) / len(data)) * valueEntropy
	return informationLoss;

##########################################
# Decision Tree Classifier
##########################################
class TreeClassifier:
	def __init__(self):
		self.root = Node("", [])
		self.default = 0
	def train(self, data, targets):
		# Set up the default guess
		self.default = targets[0]
		labels = list(range(len(data[0])))
		# print("Labels: ", labels)
		sendData = data.tolist()
		# print ("Data to list: ", sendData)
		tmpTargets = targets.tolist()
		# print ("Targets to list", tmpTargets)
		for i in range(len(data)):
			# print(sendData[i])
			# print(tmpTargets[i])
			sendData[i].append(tmpTargets[i])
		# print ("Data after append: ", sendData)
		self.root = self.makeTree(sendData, labels)
		# print ("Root set to: ", self.root.attribute, " and ", self.root.branches)
		# print(json.dumps(self.root, sort_keys=True, indent=4))
		self.displayTree(self.root, 0)
	def predict(self, data):
		toreturn = []
		for instance in data:
			toAppend = self.traverseTree(instance, self.root)
			# print ("Appending ", toAppend)
			toreturn.append(self.traverseTree(instance, self.root))
		return toreturn
	def traverseTree(self, instance, node):
		# print ("instance: ", instance)
		# print ("node attribute: ", node.attribute)
		# print ("node branches: ", node.branches)
		if instance[node.attribute] not in node.branches.keys():
			# print("node.branches.keys(): ", node.branches.keys())
			# print("instance[node.attribute]: ", instance[node.attribute])
			# print ("Instance[attribute] not in branch keys")
			return 0

		branch = node.branches[instance[node.attribute]]

		# see if more nodes exist or else it's a leaf
		if isinstance(branch, Node):
		    return self.traverseTree(instance, branch)
		else:
		    return node.branches[instance[node.attribute]]
	def makeTree(self, data, labels):
		node = Node();
		targets = [x[-1] for x in data]
		# print ("Data: ", data)
		# print("Labels: ", labels)
		# print ("Targets: ", [row[-1] for row in data])
		# print ("Unique Targets: ", numpy.unique(targets))
		# print ("Length of Unique Targets: ", len(numpy.unique(targets)))

		if(len(numpy.unique(targets)) == 1):
			# print ("Targets are the same: ", targets)
			return targets[0]
		elif(len(data) == 0):
			# print ("Data is empty: ", data)
			return self.default
		elif(len(labels) == 0):
			# print ("Labels empty: ", labels)
			# print ("Targets: ", targets)
			return max(set(targets), key=targets.count)
		entropyDict = {}
		# print (labels)
		for label in labels:
			entropyDict[label] = calcLoss(data, label)
		min_val = min(iter(entropyDict.values()))
		bestLabel = [k for k, v in iter(entropyDict.items()) if v == min_val][0]
		# print("Labels: ", labels)
		# print("Best Label: ", bestLabel)
		node.attribute = bestLabel
		# set up branch values
		values = []
		for instance in data:
			if instance[bestLabel] not in values:
				values.append(instance[bestLabel])
		for value in values:
			# print ("Value: ", value)
			sendData = []
			for i in range(len(data)):
				if data[i][bestLabel] == value:
					sendData.append(data[i]) 
			# print ("Labels before copy: ", labels)
			sendLabels = copy.deepcopy(labels)
			# print ("SendLabels after taken from labels: ", sendLabels)
			sendLabels.remove(bestLabel)
			# print ("SendLabel after remove: ", sendLabels)
			# print ("Sending Labels: ", sendLabels)
			# print ("Sending Data: ", sendData)
			node.branches[value] = self.makeTree(sendData, sendLabels)
		return node

	def displayTree(self, node, level):
	    indent = "    "
	    i = 0
	    while i < level:
	        indent += "    "
	        i += 1

	    if isinstance(node, Node):
	        print(indent, "Column: ", node.attribute)
	        for key, val in node.branches.items():
	            print(indent, "    Branch: ", key, ": ")
	            self.displayTree(val, level + 1)
	    else:
	        print(indent, node)






"""
ID3 (Examples, Target_Attribute, Candidate_Attributes)
    Create a Root node for the tree
    If all examples have the same value of the Target_Attribute, 
        Return the single-node tree Root with label = that value 
    If the list of Candidate_Attributes is empty,
        Return the single node tree Root,
            with label = most common value of Target_Attribute in the examples.
    Otherwise Begin
        A ← The Attribute that best classifies examples (most information gain)
        Decision Tree attribute for Root = A.
        For each possible value, v_i, of A,
            Add a new tree branch below Root, corresponding to the test A = v_i.
            Let Examples(v_i) be the subset of examples that have the value v_i for A
            If Examples(v_i) is empty,
                Below this new branch add a leaf node 
                    with label = most common target value in the examples
            Else 
                Below this new branch add the subtree 
                    ID3 (Examples(v_i), Target_Attribute, Attributes – {A})
    End
    Return Root
    """