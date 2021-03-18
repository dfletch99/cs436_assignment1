from __future__ import print_function
import math
import csv
import sys

class DecisionTreeNode:
    def __init__(self, parent, left, right, rule, isLeaf):
        self.parent = parent
        self.left = left
        self.right = right
        self.rule = rule
        self.isLeaf = isLeaf

    def printOut(self, depth=0):
        if not self.isLeaf:
            if depth != 0:
                print()
            for i in range(depth):
                print('| ', end='')
            print(self.rule + " = 0 : ", end='')
            self.left.printOut(depth+1)
            print()
            for i in range(depth):
                print('| ', end='')
            print(self.rule + " = 1 : ", end='')
            self.right.printOut(depth+1)
        else:
            if self.parent is not None:
                print(self.rule, end='')
            else:
                print(self.rule)

#takes file object, reads the raw data
#and converts it into a table for future use
def tablize(fo):
    reader = csv.reader(fo, delimiter=',')
    table = {t[0]: t[1:] for t in zip(*reader)}
    for c in table:
        table[c] = [int(num) for num in table[c]]
    return table

def entropyFormula(posProb, negProb):
    # handle case with no variability to not break math.log
    if posProb == 0 or negProb == 0:
        return 0
    return -1 * (posProb * math.log(posProb, 2) + negProb * math.log(negProb, 2))

def impurityFormula(posCount, negCount):
    total = (posCount+negCount) * 1.0
    return (posCount * negCount) / (total*total)

#calculate entropy of a certain subset of data
def calcEntropyOrImpurity(table, col):
    posCount = 0
    negCount = 0
    #convert to float for more accurate calculations
    total = len(table[col]) * 1.0

    #calc simple class variability
    if col == 'Class':
        for num in table[col]:
            if num == 0:
                negCount += 1
            else:
                posCount += 1

        posProb = posCount / total
        negProb = negCount / total
        if int(sys.argv[5]) == 0:
            return entropyFormula(posProb, negProb)
        elif int(sys.argv[5]) == 1:
            return impurityFormula(posCount, negCount)
    #sum entropy for each 0 and 1 class of col
    else:
        posVals = {col: [], 'Class': []}
        negVals = {col: [], 'Class': []}
        #posCount is the # of rows in posVals that have Class 1, and negCount is the same for negVals
        for i in range(len(table[col])):
            if table[col][i] == 1:
                posVals[col].append(1)
                posVals['Class'].append(table['Class'][i])
                if table['Class'][i] == 1:
                    posCount += 1
            else:
                negVals[col].append(0)
                negVals['Class'].append(table['Class'][i])
                if table['Class'][i] == 1:
                    negCount += 1
        posLen = len(posVals[col])
        negLen = len(negVals[col])
        if posLen == 0 or negLen == 0:
            return 0
        if int(sys.argv[5]) == 0:
            posEnt = entropyFormula(posCount/(posLen*1.0), (posLen-posCount)/(posLen*1.0))
            negEnt = entropyFormula(negCount/(negLen*1.0), (negLen-negCount)/(negLen*1.0))
            return (posLen/total * posEnt) + (negLen/total * negEnt)
        elif int(sys.argv[5]) == 1:
            posVI = impurityFormula(posCount, posLen - posCount)
            negVI = impurityFormula(negCount, negLen - negCount)
            return (posLen/total * posVI) + (negLen/total * negVI)

def build(table):
    root = DecisionTreeNode(None, None, None, None, False)
    buildHelper(table, root)
    return root

def buildHelper(table, node):
    allFalse = True
    allTrue = True
    if table['Class'].count(0) > 0:
        allTrue = False
    if table['Class'].count(1) > 0:
        allFalse = False

    if allFalse:
        node.isLeaf = True
        node.rule = "0"
        return
    elif allTrue:
        node.isLeaf = True
        node.rule = "1"
        return
    elif len(table) == 1:
        node.isLeaf = True
        node.rule = "0" if table['Class'].count(0) > table['Class'].count(1) else "1"
        return

    else:
        attr = findBest(table)
        node.rule = attr
        table0 = {k: [] for k in table}
        table1 = {k: [] for k in table}
        #remove selected attribute for future depths
        del table0[attr]
        del table1[attr]
        i = 0
        for key in table[attr]:
            if key == 0:
                for a in table0:
                    table0[a].append(table[a][i])
            if key == 1:
                for a in table1:
                    table1[a].append(table[a][i])
            i += 1
        node.left = DecisionTreeNode(node, None, None, "", False)
        node.right = DecisionTreeNode(node, None, None, "", False)
        buildHelper(table0, node.left)
        buildHelper(table1, node.right)
        return

def findBest(table):
    retAttr = ''
    if int(sys.argv[5]) == 0:
        totalEntropy = calcEntropyOrImpurity(table, 'Class')
        maxGain = 0
        for attr in table:
            if attr != 'Class':
                entropy = calcEntropyOrImpurity(table, attr)
                if (totalEntropy - entropy) >= maxGain:
                    maxGain = (totalEntropy - entropy)
                    retAttr = attr
    elif int(sys.argv[5]) == 1:
        totalImpurity = calcEntropyOrImpurity(table, 'Class')
        maxGain = 0
        for attr in table:
            if attr != 'Class':
                impurity = calcEntropyOrImpurity(table, attr)
                if (totalImpurity - impurity) >= maxGain:
                    maxGain = (totalImpurity - impurity)
                    retAttr = attr
    else:
        print("ERROR: Invalid heuristic - must be 0 or 1")
        exit(1)
    return retAttr

def predict(row, node):
    while not node.isLeaf:
        attr = node.rule
        if row[attr][0] == 0:
            node = node.left
        else:
            node = node.right
    return int(node.rule)

def main():
    if len(sys.argv) != 6:
        usage()

    #used only for submitting assignment
    #results = open("results.txt", "a")

    #first arg should be training set file
    train = open(sys.argv[1], "r")
    trainTable = tablize(train)
    nRows = len(trainTable['Class'])
    train.close()

    #build the decision tree based on the training data
    tree = build(trainTable)

    #second arg should be validation set file
    validate = open(sys.argv[2], "r")
    valTable = tablize(validate)

    #third arg should be test set file
    test = open(sys.argv[3], "r")
    testTable = tablize(test)

    #for calculating accuracy
    nRightTrain = 0.0
    nRightVal = 0.0
    nRightTest = 0.0
    for n in range(nRows):
        trainRow = {k: [trainTable[k][n]] for k in trainTable}
        valRow = {k: [valTable[k][n]] for k in valTable}
        testRow = {k: [testTable[k][n]] for k in testTable}
        del trainRow['Class']
        del valRow['Class']
        del testRow['Class']

        if trainTable['Class'][n] == predict(trainRow, tree):
            nRightTrain += 1
        if valTable['Class'][n] == predict(valRow, tree):
            nRightVal += 1
        if testTable['Class'][n] == predict(testRow, tree):
            nRightTest += 1
    trainAcc = nRightTrain / nRows
    valAcc = nRightVal / nRows
    testAcc = nRightTest / nRows

    printAcc(trainAcc, valAcc, testAcc, 3)
    #used for outputting to results.txt, not needed for testing
    '''results.write("D1\n")
    results.write("H1 NP train\t" + str(round(trainAcc, 3)))
    results.write("\nH1 NP valid\t" + str(round(valAcc, 3)))
    results.write("\nH1 NP test\t" + str(round(testAcc, 3)) + "\n")
    results.close()'''

    if sys.argv[4] == "yes":
        tree.printOut()
        print()

def printAcc(trainAcc, valAcc, testAcc, roundoff=3):
    print("Accuracy:")
    print("Train :" + str(round(trainAcc, roundoff)))
    print("Validate :" + str(round(valAcc, roundoff)))
    print("Test :" + str(round(testAcc, roundoff)))

def usage():
    print("USAGE: " + sys.argv[0] + " {training-file} {validation-file} {test-file} {print?} {heurisitc}")
    print("{print?} should be \"yes\" or \"no\"")
    print("{heuristic} should be \"0\" for entropy or \"1\" for variance impurity")
    exit(1)


if __name__ == '__main__':
    main()
