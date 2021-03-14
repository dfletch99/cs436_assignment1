import math
import csv

class DecisionTreeNode:
    def __init__(self, parent, left, right, rule, isLeaf):
        self.parent = parent
        self.left = left
        self.right = right
        self.rule = rule
        self.isLeaf = isLeaf

#takes file object, reads the raw data
#and converts it into a table for future use
def tablize(fo):
    reader = csv.reader(fo, delimiter=',')
    table = {t[0]: t[1:] for t in zip(*reader)}
    for c in table:
        table[c] = [int(num) for num in table[c]]
    return table

#calculate entropy of a certain subset of data
def calcEntropy(col):
    posCount = negCount = 0
    total = len(col) * 1.0
    for element in col:
        if element == 1:
            posCount += 1
        else:
            negCount += 1

    #handle case with no variability to not break math.log
    if posCount == 0 or negCount == 0:
        return 0

    posProb = posCount/total
    negProb = negCount/total
    return -1 * (posProb * math.log(posProb, 2) + negProb * math.log(negProb, 2))

def entropyBuild(table):
    root = DecisionTreeNode(None, None, None, None, False)
    tree = entropyHelper(table, root)

def entropyHelper(table, node):
    allFalse = True
    allTrue = True
    for num in table['Class']:
        if num == 1:
            allFalse = False
        if num == 0:
            allTrue = False

    if allFalse:
        node.left = DecisionTreeNode(node, None, None, "0", True)
    elif allTrue:
        node.left = DecisionTreeNode(node, None, None, "1", True)
    else:
        #attr = findBest(table)
        table0 = dict.fromkeys(table, [])
        table1 = dict.fromkeys(table, [])
        for num in table[attr]:
            if num == 0:
                for key in table0:
                    table0[key].append(table[key])
            else:
                for key in table1:
                    table1[key].append(table[key])
        node.left = entropyHelper(table0, node)
        node.right = entropyHelper(table1, node)
        return DecisionTreeNode(node, entropyHelper(table0, node), entropyHelper(table1, node), None, False)


def newNode(node):
    pass

def main():
    fo = open("Datasets/Dataset1/test_set.csv", "r")
    table = tablize(fo)
    fo.close()
    #tree = entropyBuild(table)


if __name__ == '__main__':
    main()
