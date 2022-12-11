import utility
import session
import os
import sys
from aocd.models import Puzzle
from aocd import submit
os.environ["AOC_SESSION"] = session.AOC_SESSION

DAY = int(sys.argv[0].rsplit('/', 1)[1][3:-3])
YEAR = int(sys.argv[0].rsplit('/', 3)[1])

## INPUT STUFF
puzzle = Puzzle(year=YEAR, day=DAY)
data = puzzle.input_data
lines = utility.inputDataToLines(data)

## SAMPLE INPUT STUFF
sample = []
with open("./input.txt", encoding="utf8") as fp:
    for line in fp:
        sample.append(line.strip())

## CONVERT INPUT STRING LIST TO NUMBERS IF POSSIBLE
try:
    nums = utility.listStringToListNum(lines)
    sampleNum = utility.listStringToListNum(sample)
except:
    nums = []
    sampleNum = []

sp1 = sp2 = p1 = p2 = 0


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def getSize(self):
        return self.size

    def getName(self):
        return self.name


class Folder:
    def __init__(self, folderName, parentFolder):
        self.folderName = folderName
        self.parentFolder = parentFolder
        self.folders = []
        self.files = []

    def addFolder(self, f):
        self.folders.append(f)

    def addFile(self, f):
        self.files.append(f)

    def getSize(self):
        size = 0
        for f in self.folders:
            folderSize = f.getSize()
            size += folderSize
        for f in self.files:
            size += f.size
        return size

    def getParent(self):
        return self.parentFolder

    def getFolder(self, folderName):
        for i in self.folders:
            if i.getName() == folderName:
                return i
        return None

    def getName(self):
        return self.folderName


def sumFoldersLessThanSize(folder, limitSize=100000):
    folderQueue = [folder]
    sum = 0
    while len(folderQueue) > 0:
        curr = folderQueue.pop(0)
        for i in curr.folders:
            folderQueue.append(i)

        currSize = curr.getSize()
        if currSize <= limitSize:
            sum += currSize

    return sum


def findSmallestFolderToDelete(folder, minimumSize):
    folderQueue = [folder]
    minimumFolder = folder
    minimumFolderSize = 30000000
    while len(folderQueue) > 0:
        curr = folderQueue.pop(0)
        for i in curr.folders:
            folderQueue.append(i)

        currSize = curr.getSize()
        if currSize >= minimumSize:
            if minimumFolderSize > currSize:
                minimumFolderSize = currSize
                minimumFolder = curr

    return minimumFolderSize


def parseInput(input):
    root = Folder("/", None)

    currFolder = root
    for i in range(1, len(input)):
        splitList = input[i].split(" ")

        if splitList[0] == "$":
            if splitList[1] == "cd":
                # command of some kind, only care about cd, and only ever does "/" for first call
                folderName = splitList[2]
                if folderName == "..":
                    currFolder = currFolder.getParent()
                else:
                    currFolder = currFolder.getFolder(folderName)
        elif splitList[0] == "dir":
            if currFolder is not None:
                currFolder.addFolder(Folder(splitList[1], currFolder))
        else: # file
            if currFolder is not None:
                currFolder.addFile(File(splitList[1], int(splitList[0])))
    return root


def puzzle(input, part2=False):
    root = parseInput(input)
    if not part2:
        result = sumFoldersLessThanSize(root)
    else:
        maxSpace = 70000000
        requiredSpace = 30000000
        remainingSpace = maxSpace - root.getSize()
        requiredRemainingSpace = requiredSpace - remainingSpace
        result = findSmallestFolderToDelete(root, requiredRemainingSpace)
    return result

sp1 = puzzle(sample)
p1 = puzzle(lines)
sp2 = puzzle(sample, True)
p2 = puzzle(lines, True)

print("SP1: " + str(sp1))   # 95437
print("SP2: " + str(sp2))   # 24933642
print("P1: " + str(p1))     # 1513699
print("P2: " + str(p2))     # 7991939

if p1 != 0 and submit(p1, part="a", day=DAY, year=YEAR) is None:
    if p2 != 0:
        submit(p2, part="b", day=DAY, year=YEAR)